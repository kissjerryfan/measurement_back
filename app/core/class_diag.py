import os
from xml.dom.minidom import parseString
from flask import jsonify
from ..util import trueReturn, falseReturn

results = {}
# 对应name的id
n2id = {}
# 各类关系
tbe = []
names = []
DITs = {}


def readXML(file_name):
    for i in range(len(file_name)):
        file_name[i] = str(file_name[i], 'UTF-8')
    file = ''.join(file_name)
    # print(file)
    domTree = parseString(file)
    # 文档根元素
    rootNode = domTree.documentElement
    classes = rootNode.getElementsByTagName("packagedElement")

    # 三种关系会直接出现：实现、关联、依赖
    for single in classes:
        name = single.getAttribute("name")
        id = single.getAttribute("xmi:id")
        type = single.getAttribute("xmi:type")[4:]
        n2id[id] = name

    for single in classes:
        temp = {}
        type = single.getAttribute("xmi:type")[4:]
        id = single.getAttribute("xmi:id")
        if type == "Association":
            # 关联，包括聚合和组合
            ends = single.getElementsByTagName("ownedEnd")
            begin = ends[0].getAttribute("type")
            end = ends[1].getAttribute("type")
        elif type == "Dependency":
            # 依赖
            end = single.getAttribute("supplier")
            begin = single.getAttribute("client")
        elif type == "InterfaceRealization":
            # 实现
            end = single.getAttribute("supplier")
            begin = single.getAttribute("client")
        else:
            continue
        temp["type"] = type
        temp["begin"] = n2id[begin]
        temp["end"] = n2id[end]
        tbe.append(temp)

    for single in classes:
        type = single.getAttribute("xmi:type")[4:]
        name = single.getAttribute("name")
        id = single.getAttribute("xmi:id")
        if type == "Class" or type == "Interface":
            operations = single.getElementsByTagName("ownedOperation")
            attributes = single.getElementsByTagName("ownedAttribute")
            sclass = {}
            sclass['name'] = name
            sclass['type'] = type

            names.append(name)

            dads = single.getElementsByTagName("generalization")
            for dad in dads:
                if dad.hasAttribute("general"):
                    base_id = dad.getAttribute("general")
                    temp = {}
                    temp["type"] = "Generalization"
                    temp["begin"] = n2id[id]
                    temp["end"] = n2id[base_id]
                    tbe.append(temp)

            sattr = []
            for attr in attributes:
                attr_name = attr.getAttribute("name")
                attr_type = n2id[attr.getAttribute("type")]
                sattr.append(attr_type + "-" + attr_name)
            sclass['attributes'] = sattr

            sopera = []
            for opera in operations:
                opera_name = opera.getAttribute("name")

                temp = {}
                temp['name'] = opera_name
                temp1 = []
                opera_params = opera.getElementsByTagName("ownedParameter")
                for param in opera_params:
                    if param.getAttribute("direction") == "return":
                        temp['type'] = n2id[param.getAttribute("type")]
                    else:
                        sparam = n2id[param.getAttribute("type")] + "-" + param.getAttribute("name")
                        temp1.append(sparam)
                temp['params'] = temp1
                sopera.append(temp)
            sclass['operations'] = sopera

            results[name] = sclass
    print(names)


def searchNOOandNOA(name):
    value = 0
    noa = 0
    for stbe in tbe:
        if stbe['type'] == 'Generalization':
            if stbe['begin'] == name:
                son = results[name]['operations']
                dad_name = stbe['end']
                dad = results[dad_name]['operations']  # 找到爹了
                for sdad in dad:
                    if sdad in son:
                        value = value + 1
                noa = len(son) - value
    return value, noa


def searchDepth(name):
    value = DITs[name]
    if value != 0:
        DITs[name] = value

    for stbe in tbe:
        if stbe['type'] == 'Generalization':
            if stbe['begin'] == name:
                base_name = stbe['end']
                searchDepth(base_name)
                num = DITs[base_name]
                value = max(value, num + 1)
    DITs[name] = value


def getData(file_name):
    readXML(file_name)
    for name in names:
        DITs[name] = 0

    NOCs = {}
    for name in names:
        NOCs[name] = 0

    CBOs = {}
    for name in names:
        CBOs[name] = 0

    for stbe in tbe:
        type = stbe['type']
        begin = stbe['begin']
        end = stbe['end']

        searchDepth(begin)

        # 符合继承
        if type == "Generalization":
            NOCs[end] = NOCs[end] + 1
        # 符合耦合
        if type != "Generalization":
            CBOs[end] = CBOs[end] + 1
            CBOs[begin] = CBOs[begin] + 1

    json = []
    for name in names:
        result = results[name]
        temp = {}
        temp['name'] = name
        temp['CS'] = len(result['attributes']) + len(result['operations'])
        NOO, NOA = searchNOOandNOA(name)
        temp['NOO'] = NOO
        temp['NOA'] = NOA
        temp['DIT'] = DITs[name]
        temp['NOC'] = NOCs[name]
        temp['CBO'] = CBOs[name]
        json.append(temp)
    print(names)
    results.clear()
    #对应name的id
    n2id.clear()
    #各类关系
    tbe.clear()
    names.clear()
    DITs.clear()
    return trueReturn(json, 'ok')


if __name__ == '__main__':
    file_name = 'D:/Study/大三下/软件度量及应用/实验/1.xml'
    getData(file_name)
