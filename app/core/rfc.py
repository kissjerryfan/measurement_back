import xml.dom.minidom as xmldom
import os
from ..util import trueReturn, falseReturn

# RFC,interaction用于存储时序图里的事件
RFC = []
RS = []
RFCObjectName = []
interaction = []

def getRFC(fileName):
    ##########################时序图#######################
    xmlfilepath = os.path.abspath(fileName)
    SXobj = xmldom.parse(xmlfilepath)
    # 得到元素对象
    SXelementobj = SXobj.documentElement
    SXelement = SXelementobj.getElementsByTagName("packagedElement")
    for i in range(len(SXelement)):
        if SXelement[i].getAttribute("xmi:type") == "uml:Actor" or SXelement[i].getAttribute("xmi:type") == "uml:InstanceSpecification":
            RFCObjectName.append(SXelement[i].getAttribute("name"))
            RFC.append(0)
        if SXelement[i].getAttribute("xmi:type") == "uml:Interaction":
            interaction.append(SXelement[i])
    # 得到了时序图中的所有事件的内容后开始计算每个类调用的方法的集合
    for i in range(len(interaction)):
        lifeLine = []
        coverList = []
        msgList = []
        lifeLine = interaction[i].getElementsByTagName("lifeline")
        for j in range(len(lifeLine)):
            if (lifeLine[j].getAttribute("name") in RFCObjectName):
                # 二维动态数组,存储每个类的每一条线的id
                coverList.append("")
                coverList[len(coverList) - 1]=(lifeLine[j].getAttribute("coveredBy").split(" "))
        msgList = interaction[i].getElementsByTagName("message")
        # 排除自己运行的情况
        for j in range(len(msgList)):
            # 要排除返回消息的线
            if msgList[j].getAttribute("messageSort") != "reply":
                sender = msgList[j].getAttribute("sendEvent")
                receiver = msgList[j].getAttribute("receiveEvent")
                sendIndex = 0
                receiveIndex = 0
                for k in range(len(coverList)):
                    if sender in coverList[k]:
                        sendIndex = k
                    if receiver in coverList[k]:
                        receiveIndex = k
                # 非自调用的情况下
                if sendIndex != receiveIndex:
                    RFC[sendIndex] = RFC[sendIndex] + 1
    for i in range(1,len(RFC)):
        RFC[len(RFC) - i - 1] = RFC[len(RFC) - i] +  RFC[len(RFC) - i - 1]

    print ("------------------------------------------")
    for i in range(len(RFC)):
      print("类",RFCObjectName[i].ljust(15),"的RFC值为：", RFC[i])

    json = []

    for i in range(len(RFC)):
        temp = {}
        temp['name'] = RFCObjectName[i].ljust(15)
        temp['RFC'] = RFC[i]
        json.append(temp)
    # print(json)
    return trueReturn(json, 'ok')

if __name__ == '__main__':
    file_name = "sx.xml"
    getRFC(file_name)