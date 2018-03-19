#!/usr/bin/python
#encoding=utf-8

import re
import os
import time
from optparse import OptionParser

"""
This was used to deal train.out data
You must choose the number of task
"""
__author__ = "Guanjie Wang"
__email__ = "wangguanjie@buaa.edu.cn"
__date__ = "Jan 17, 2018"

def readme():
    print(('-'*60).center(90))
    _pri_center('This was used to get data from train process')
    _pri_center('Two task:'+' '*35)
    _pri_center('1: get simple train energy data' + ' '*(44-len('1: get simple train energy data')))
    _pri_center('2: split continues file to each one file'+ ' '*(44-len('2: split continues file to each one file')))
    _pri_center('You can use -h read help'+ ' '*(44-len('you can use -h read help')))
    _pri_center('Example:'+ ' '*36)
    _pri_center('   TrainErrorData.py -t 1 train.out'+ ' '*(44-len('   TrainErrorData.py -t 1 train.out')))
    print(('-'*60).center(90))

def _pri_center(content,num=58):
    print(' ' * 15 + '|' + content.center(num, ' ') + '|' + ' ' * 15)

def _remove_path(path):
    if os.path.exists(path):
        os.remove(path)
        print('{0} ******* This file path exists, removed'.format(path))

def pri(content):
    print('*' * 90)
    print(content)

def tail(alltime):
    print(('-'*60).center(90))
    _pri_center('Congratulation!!!!!')
    _pri_center('You have successfully get ANN data files ')
    _pri_center('Total uesd time was\033[0;32m {0}s, {1}h\033[0m'.format(alltime,alltime/3600))
    print(('-'*60).center(90))

def get_path(train_file):
    nowpath = os.getcwd()
    # os.path.dirname(nowpath) # Gets the parent directory of the folder where the current file is located
    files = os.listdir(nowpath)
    train_path = ''
    for i in range(len(files)):
        if len(re.findall(train_file,files[i])) > 0:
            train_path = os.path.join(nowpath,files[i])
            break
    if len(train_path) != 0:
        return nowpath, train_path
    else:
        pri(" Current path don't have {0} file".format(train_file))
        exit()

def Return_number(train_file):
    path,train_path = get_path(train_file)
    f = open(train_path,'r')
    content = f.readlines()
    f.close()
    total_list  = []
    name = []
    line_number = []
    now = 0
    for i in range(len(content)):
        if len(re.findall(r'Training process started',content[i])) > 0:
            now += 1
            name.append('Training process started')
            line_number.append(i)
        elif len(re.findall(r'Networks',content[i])) > 0:
            name.append('Networks')
            line_number.append(i)
        elif len(re.findall(r'Storing networks',content[i])) > 0:
            name.append('Networks stop')
            line_number.append(i-2)
        elif len(re.findall(r'Training process',content[i])) > 0:
            name.append('Training process')
            line_number.append(i)
            if len(name) == len(line_number) != 0:
                file_number = dict(zip(name, line_number))
                try:
                    b = file_number['Training data done']
                except KeyError:
                    file_number['Neural Network training done'] = len(content)
                    file_number['Training data done'] = len(content)
                total_list.append(file_number)
                name = []
                line_number = []
        #It is possible to terminate before the calculation is complete, and there will not be the following two keywords, so the number of lines for the last behavior is default
        elif len(re.findall(r'Storing final energies',content[i])) > 0:
            total_list[-1]['Training data done'] = i-2
            # name.append('Training data done')
            # line_number.append(i-2)
        elif len(re.findall(r'Neural Network training done',content[i])) > 0:
            total_list[-1]['Neural Network training done'] = i
            # name.append('Neural Network training done')
            # line_number.append(i)
        else:
            pass
    print('The file have {0} process'.format(now))
    return total_list

def write_data(task,content,train_file):
    path,train_path = get_path(train_file)
    f = open(train_path)
    c = f.readlines()
    f.close()
    for i in range(len(content)):
        Networks_line = content[i]['Networks']
        for n in range(Networks_line,Networks_line+10):
            if len(re.findall(r'Number of layers(.*)',c[n])) > 0:
                layers  = re.findall(r'Number of layers(.*)',c[n])[0].replace(' ','').replace(':','')
                break
        if len(layers) > 0:
            if task == 1:
                start_line = content[i]['Training process']
                gogal_name = 'train_' + layers + '_simpledata.out'
                gogal_path = os.path.join(path, gogal_name)
                _remove_path(gogal_path)
                stop_line = content[i]['Training data done']
            if task == 2:
                start_line = content[i]['Training process started']
                gogal_name = 'train_' + layers + '_split.out'
                gogal_path = os.path.join(path, gogal_name)
                _remove_path(gogal_path)
                stop_line = content[i]['Neural Network training done'] + 2
            for m in range(start_line,stop_line):
                open(gogal_path,'a').write(c[m])
        else:
            print("Don't find the information about layers")
            exit()

def RunMain():
    readme()
    usage = '''%prog -t args filename
        eg: TrainErrorData.py -t 2 train.out'''
    parser = OptionParser(usage)
    parser.add_option('-t', '--task', help='choose task number. 1: simple 2: split', default=1)
    option, args = parser.parse_args()
    start = time.time()
    if len(args) > 0:
        content = Return_number(args[0])
        write_data(task=int(option.task),content=content,train_file=args[0])
        alltime = time.time() - start
        tail(alltime)
    else:
        print(parser.usage.replace('%prog','TrainErrorData.py'))
        exit()

if __name__ == '__main__':
    RunMain()