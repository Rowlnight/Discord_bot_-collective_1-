#use before the asinc

import os

dir = os.path.abspath(os.curdir)

def VS_error():
    with open(dir + '\\data\\text\\answers\\VC_error.txt', 'r', encoding="utf-8") as file:
        result = file.read().split('\n')
    return result

def get_list_of_the_unclear_answers():
    with open(dir + '\\data\\text\\answers\\unclear.txt', 'r', encoding="utf-8") as file:
        result = file.read().split('\n')
    return result
  

