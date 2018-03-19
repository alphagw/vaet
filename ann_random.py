#!/usr/bin/env python
#encoding=utf-8
import numpy as np
import os
from optparse import OptionParser
"""
Now path must have generate.all_xsf which was total xsf file 
You can use ann_random.py 300 to random generate 300 data in generate.in
You can change the file name by yourself
"""
__author__ = "Guanjie Wang"
__email__ = "wangguanjie@buaa.edu.cn"
__date__ = "Jan 22, 2018"

def read(filename,number):
    f = open(filename,'r')
    lines = f.readlines()
    f.close()
    a = np.random.randint(13,len(lines),number)
    head = lines[:12]
    head.append(str(len(a)) + '\n')
    for i in a:
        head.append(lines[i])
    return head
def write(filename,content):
    f = open(filename,'a')
    for i in content:
        f.write(i)
    f.close()

def parse_option():
    usage = "%prog arg1  eg:%prog 3000"
    parse = OptionParser(usage)
    (option,args) = parse.parse_args()
    print('The number of random XSF file was {0}'.format(int(args[0])))
    return int(args[0])

def _remove_path(path):
    if os.path.exists(path):
        os.remove(path)
        print('******* " {0}" file path exists, removed'.format(path))

if __name__ == '__main__':
    filename = 'generate.all_xsf'
    number = parse_option()
    gogalname = 'generate.in'
    
    head = read(filename,number)
    _remove_path(gogalname)
    write(gogalname,head)
