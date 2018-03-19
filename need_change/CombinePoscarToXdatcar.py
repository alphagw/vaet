#!/usr/bin/python
#encoding=utf-8

import re
import os
import time
from optparse import OptionParser

"""
According to ASE module combine POSCAR to XDATCAR 
All poscar need put in a file named combine***
If you want to continue write,please use -c number
If you want to write new, don't need anything parameter
Revise 106 line to adapt different POSCAR version(vasp4: set 7,vasp 5: set 8)

Example:
    CombinePoscarToXdatcar.py -c 178
"""
__author__ = "Guanjie Wang"
__email__ = "wangguanjie@buaa.edu.cn"
__date__ = "Jan 18, 2018"

def readme():
    print(('-'*60).center(90))
    _pri_center('This was used to combine POSCAR to XDATCAR')
    _pri_center('All poscar was put in a file named combine***')
    print(('-'*60).center(90))

def _pri_center(content,num=58):
    print(' ' * 15 + '|' + content.center(num, ' ') + '|' + ' ' * 15)

def pri(content):
    print('*' * 90)
    print(content)

def tail(alltime):
    print(('-'*60).center(90))
    _pri_center('Uesd time was {0:.6f}s, {1:.6f}h'.format(alltime,alltime/3600))
    print(('-'*60).center(90))

def _get_path():
    nowpath = os.getcwd()
    files = os.listdir(nowpath)
    combine_path = ''
    for i in range(len(files)):
        combine_file = r'combine'
        if len(re.findall(combine_file,files[i])) > 0:
            combine_path = os.path.join(nowpath,files[i])
            break
    if len(combine_path) != 0:
        return nowpath, combine_path
    else:
        pri(" Current path don't have combine.out file")
        exit()

def _get_all_poscar():
    combine_path = _get_path()[1]
    if os.path.exists(combine_path):
        path = list(os.walk(combine_path))
        file_path = []
        for i in range(len(path)):
            for m in range(len(path[i][2])):
                if re.findall(r'POSCAR', path[i][2][m]):
                    file_path.append(os.path.join(path[i][0], path[i][2][m]))
        num = str(len(file_path))
        print('Total poscar was {0}'.format(num))
        return file_path
    else:
        pri("Don't find POSCAR file")
        exit()

def _get_head_file(head_path):
    head = []
    f = open(head_path)
    content = f.readlines()
    for i in range(0,7):
        head.append(content[i])
    f.close()
    return head

def _remove_path(path):
    if os.path.exists(path):
        print('{0} exists, Removed!!!'.format(path))
        os.remove(path)

def _write_content(gogal_path, content):
    for i in range(len(content)):
        open(gogal_path, 'a').write(content[i])

def write_file_content(num,control):
    POSCAR_path = _get_all_poscar()
    head = _get_head_file(POSCAR_path[0])
    gogal_path = os.path.join(os.getcwd(),"XDATCAR")
    if control:
        pass
    else:
        _remove_path(gogal_path)
        _write_content(gogal_path,head)
    for i in range(len(POSCAR_path)):
        content = []
        constant = "Direct configuration=  " + str(num) + '\n'
        content.append(constant)
        f = open(POSCAR_path[i])
        c = f.readlines()
        f.close()
        for m in range(8,len(c)):
            content.append("  "+c[m])
        #pri("Current task were {0} ".format(i))
        _write_content(gogal_path,content)
        num += 1

def option_parser():
    usage = '%prog [option] [arg1]' \
            'eg: CombinePoscarToXdatcar.py -c continue'
    parser = OptionParser(usage)
    parser.add_option('-c','--cont',action='store',
                      help='''if you want to continue write, please input the first number''')
    (option,args) = parser.parse_args()
    if option.cont:
        return True,option.cont
    else:
        return False,'1'

def RunMain():
    start = time.time()
    readme()
    control, number = option_parser()
    write_file_content(int(number),control)
    alltime = time.time() - start
    tail(alltime)

if __name__ == '__main__':
    RunMain()
