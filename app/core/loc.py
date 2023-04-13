import re
import os
from ..util import trueReturn, falseReturn

def getLCOM(file_name):
    dkh = 0
    loc = 0
    for i in range(len(file_name)):
        file_name[i] = str(file_name[i], 'UTF-8')
    file = ''.join(file_name)
    lines = file.split('\n')  # 一次性读取一个文件,并用换行分割每一行
    for i in lines:
        print(i)
    row_count = blank_count = note_count = code_count = 0
    row_count += len(lines)
    instanceFlag = True
    flag = False
    functionBegin = False
    funcName = []
    funcInstanceList = []
    instance = []
    inst = []
    for line in lines:
        if line.strip() == '':
            blank_count += 1
            continue
        noteline = re.match(r'^/(.*)|^\*(.*)|(.*)\*/$', line.strip(), flags=0)  # 匹配以/、/*、*开头 或*/结尾的注释行
        if noteline is None:  # 匹配为代码行
            code_count += 1
        else:
            note_count += 1
        # 找到类开始的地方，提取类中的实例变量
        if flag:
            # 找到函数开始的地方
            if "{" in line:
                instanceFlag = False
                dkh = dkh + 1
                if not functionBegin:
                    functionBegin = True
                    name = line.split("(")[0].split(" ")
                    funcName.append(name[len(name) - 1])
            if "}" in line:
                dkh = dkh - 1
            if dkh > 0:
                # 在当前函数范围内，寻找是否使用了某个实例
                for i in range(len(instance)):
                    if instance[i] in line and not (instance[i] in inst):
                        inst.append(instance[i])
            if functionBegin and dkh == 0:
                functionBegin = False
                funcInstanceList.append(inst)
                inst = []
            if instanceFlag:
                if not ("{" in line) and not ("}" in line):
                    line = line.replace(";", "")
                    list = line.split(" ")
                    if not list[len(list) - 1].replace("\n", "") == "\t":
                        instance.append(list[len(list) - 1].replace("\n", ""))
        # 找到文件中类开始的地方
        if "class" in line:
            line = line.replace("{", "")
            list = line.split(" ")
            index = list.index("class") + 1
            print("当前类名为：",list[index])
            flag = True
    print("源程序总行数:", row_count)
    print("代码行数:", code_count, ",占", round(code_count / row_count * 100, 2), "%")
    print("注释行数:", note_count, ",占", round(note_count / row_count * 100, 2), "%")
    print("空白行数:", blank_count, ",占", round(blank_count / row_count * 100, 2), "%")
    data = {}
    data['PLOC']= row_count
    data['LLOC'] = code_count + 1
    data['NCLOC'] = code_count + 1 -note_count
    data['CLOC'] = note_count
    print(data)
    return trueReturn(data, 'ok')



if __name__ == '__main__':
    file_name = "Member.java"
    getLCOM(file_name)