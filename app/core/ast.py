import javalang
from javalang.tree import ClassDeclaration, MethodDeclaration, StatementExpression, MethodInvocation,\
    ForStatement, IfStatement, MemberReference, BlockStatement, EnhancedForControl, BinaryOperation,\
    FieldDeclaration, LocalVariableDeclaration, Assignment, TryStatement, CatchClause, This


class Context:

    def __init__(self) -> None:
        self.attrs = []


class Queue(list):

    def __init__(self):
        super().__init__()
    
    def enter(self, item):
        self.append(item)
    
    def dequeue(self):
        return self.pop(0)
    
    def is_empty(self):
        return len(self) <= 0


class Stack(list):

    def __init__(self):
        super().__init__()
    
    def push(self, item):
        self.append(item)
    
    def pop(self):
        return super().pop(-1)
    
    def is_empty(self):
        return len(self) <= 0


class Qualifier:

    def __init__(self, member: str) -> None:
        self.member: str = member
    
    def get(self):
        return self.member.split('.')[0]


def analyze_method(method: MethodDeclaration, ctx: Context):
    """
    StatementExpression: 语句表达式，如方法调用等
        MethodInvocation: 方法调用
        Assignment: 变量赋值
    LocalVariableDeclaration: 变量声明与赋值
    """

    def add_ref(ref):
        nonlocal data, ctx, inner
        if ref in ctx.attrs and ref not in inner:
            data['reference'].add(str(ref))

    data = {
        'reference': set(),
        'call': set()
    }
    # 解决方法：堆栈+队列，用堆栈管理一系列队列
    # 内部属性
    inner = []
    for statement in method.body:
        queue = Queue()
        queue.enter(statement)

        while queue.is_empty() is False:
            item = queue.dequeue()
            if isinstance(item, MethodInvocation):
                data['call'].add(str('' if item.qualifier is None else item.qualifier) + '.' + str(item.member))
                if item.qualifier is not None:
                    queue.enter(Qualifier(item.qualifier))
                for arg in item.arguments:
                    queue.enter(arg)
                for sel in [] if item.selectors is None else item.selectors:
                    queue.enter(sel)
            elif isinstance(item, MemberReference):
                add_ref(item.member)
            elif isinstance(item, StatementExpression):
                expression = item.expression
                queue.enter(expression)
            elif isinstance(item, ForStatement):
                queue.enter(item.body)
                if isinstance(item.control, EnhancedForControl):
                    queue.enter(item.control.iterable)
            elif isinstance(item, BlockStatement):
                for state in item.statements:
                    queue.enter(state)
            elif isinstance(item, IfStatement):
                queue.enter(item.condition)
                queue.enter(item.then_statement)
                queue.enter(item.else_statement)
            elif isinstance(item, BinaryOperation):
                queue.enter(item.operandl)
                queue.enter(item.operandr)
            elif isinstance(item, LocalVariableDeclaration):
                for dec in item.declarators:
                    inner.append(dec.name)
            elif isinstance(item, Assignment):
                queue.enter(item.expressionl)
                queue.enter(item.value)
            elif isinstance(item, TryStatement):
                for block in item.block:
                    queue.enter(block)
                for catch in item.catches:
                    queue.enter(catch)
            elif isinstance(item, CatchClause):
                for block in item.block:
                    queue.enter(block)
            elif isinstance(item, This):
                for selector in item.selectors:
                    queue.enter(selector)
            elif isinstance(item, Qualifier):
                add_ref(item.get())
    return data


def analyze_lcom(method: dict):
    items = method.items()
    lcom = 0
    for index, (key, value) in enumerate(items):
        for (in_key, in_value) in list(items)[index + 1:]:
            if len(value['reference'].intersection(in_value['reference'])) <= 0:
                lcom += 1
            else:
                lcom = max(0, lcom - 1)
    return lcom


def analyze_rfc(method: dict):
    rfc = 0
    for key, value in method.items():
        rfc += len(value['call'])
    return rfc + len(method)


def analyze(file):
    queue = Queue()

    unit = javalang.parse.parse(file)
    classes = []
    # java文件下所有定义的根类（不包括内部类）
    for type in unit.types:
        type: ClassDeclaration
        # 数据结构: 对象，类名（包括嵌套结构以及内部类，比如内部类A.B.C）
        queue.enter((type, type.name))
    
    while queue.is_empty() is False:
        item, name = queue.dequeue()
        if isinstance(item, ClassDeclaration):
            ctx = Context()
            method = {}
            # 如果是个类，里面可能有方法或者内部类
            # 获取所有类属性
            for body in item.body:
                if isinstance(body, FieldDeclaration):
                    for var in body.declarators:
                        ctx.attrs.append(var.name)
            # 如果是个类，那么把这个类的所有方法度量一遍
            for body in item.body:
                if isinstance(body, MethodDeclaration):
                    method_data = analyze_method(body, ctx)
                    method[body.name] = method_data
            
            _method = {}
            for key, value in method.items():
                _method[key] = {
                    'reference': list(value['reference']),
                    'call': list(value['call'])
                }
            classes.append({
                'raw': _method,
                'lcom': analyze_lcom(method),
                'rfc': analyze_rfc(method),
                'classname': name
            })
        elif isinstance(item, MethodDeclaration):
            # 如果是个方法，里面可能有内部类
            # 如果是个方法，那么直接看里面有没有类的声明，这样不会漏掉内部类
            pass
    return classes
