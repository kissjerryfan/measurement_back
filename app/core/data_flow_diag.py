import os
from ..util import trueReturn, falseReturn

def findStr(file, str_):
    count = 0
    for line in file:
        line = str(line)
        time = line.count(str_)
        count += time
    return count


def getMcCabe(file_name):
    # 查找开始节点数
    start_count = findStr(file_name, "<o:Start Id")
    # 查找终止节点数
    end_count = findStr(file_name, "<o:End Id")
    # 查找操作数
    oper_count = findStr(file_name, "<o:Activity Id")
    # 查找判断数
    dec_count = findStr(file_name, "<o:Decision Id")
    # 查找边数
    flow_count = findStr(file_name, "<o:ActivityFlow Id")

    # 计算圈复杂度，分别为边数-节点数+2及判断数+1
    McCabe_2 = flow_count - (oper_count + dec_count + start_count + end_count) + 2
    McCabe_3 = dec_count + 1

    print(McCabe_2, McCabe_3)
    # 验证
    if (McCabe_2 == McCabe_3):
        print('McCabe:', McCabe_2)
        return trueReturn(McCabe_2, 'ok')
    else:
        print('Wrong input!')
        return falseReturn(None, 'wrong input image!')


if __name__ == '__main__':
    file_name = "D:\diagram\ControlFlowDiagram.oom"
    getMcCabe(file_name)