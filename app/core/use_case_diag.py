import os

from flask import jsonify

from ..util import trueReturn, falseReturn

def findStr(file, str_):
    count = 0
    for line in file:
        time = str(line).count(str_)
        count += time
    return count

def getActorandUseCase(file_name):
    #查找执行者
    actor_count = findStr(file_name, "<o:Actor Id")
    #查找用例
    use_case_count = findStr(file_name, "<o:UseCase Id")

    print('Actor count: ', actor_count)
    print('Use case count: ', use_case_count)
    json_data = {
        'actor_count': actor_count,
        'use_case_count': use_case_count
    }
    return trueReturn(json_data, 'ok')

if __name__ == '__main__':
    file_name = "D:\diagram\CCMS.oom"
    getActorandUseCase(file_name)