#!/usr/bin/python
#encoding=utf-8
import re
import os
import time
'''
这个脚本可以设置起始数字，终止数字及间隔，并且具体时间步根据poscar名字命名数字
不建议使用这个脚本，尽量使用CombinePoscarToXdatcar.py
'''
def readme():
    print('*'*90)
    print('\033[1m用来将多个POSCAR合成一个vasp MD过程产生的XDATCAR格式\033[0m')
    print('\033[1m存放所有POSCAR的文件必须以combine为关键词命名\033[0m')
    print('\033[1mPOSCAR 的命名必须是POSCAR序号 eg：POSCAR103\033[0m')
    print('*'*90)

def pri(content):
    print('*' * 90)
    print(content)

def tail(alltime):
    print('*' * 90)
    print('Total uesd time was\033[0;32m {0}s, {1}h\033[0m'.format(alltime,alltime/3600).center(90, ' '))
    print('*' * 90)

def get_path():
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

def control():
    print('Please input number which you want to begin：')
    star =  input()
    print('Please input number which you want to stop：')
    stop =  input()
    print('Please input number which you want to space：')
    space = input()
    if star.isdigit() and stop.isdigit() and space.isdigit():
        pass
    else:
        print('Please input number or digit !!!!!!!')
        exit()
    return star,stop,space

def get_num():
    star,stop,space = control()
    number  = [str(x) for x in range(int(star),int(stop)+1,int(space))]
    return number

def get_all_poscar():
    combine_path = get_path()[1]
    POSCAR_path = []
    number = []
    if os.path.isdir(combine_path):
        content = os.listdir(combine_path)
        for i in range(len(content)):
            if len(re.findall(r'POSCAR',content[i])) > 0:
                num = re.findall(r'POSCAR(.*)',content[i])
                try:
                    num = int(num[0])
                except ValueError:
                    print("\033[0;31m Waring: POSCAR name is wrong\033[0m")
                number.append(str(num))
                POSCAR_path.append(os.path.join(combine_path,content[i]))
    else:
        pri("Don't find POSCAR file")
        exit()
    poscar_path = dict(zip(number,POSCAR_path))
    return POSCAR_path,poscar_path

def line_split(content):
    gogal_content = []
    content.replace('\n','').strip().split(' ','')
    for i in range(len(content)):
        if len(content[i]) != 0:
            gogal_content.append(content[i])
    return gogal_content

def get_head_file(POSCAR_path,gogal_path):
    head_path = POSCAR_path
    head = []
    f = open(head_path)
    content = f.readlines()
    f.close()
    for i in range(0,6):
        head.append(content[i])
    head.insert(-1,"  " + content[0])
    if os.path.exists(gogal_path):
        pri("\033[0;31mWrong!!! The XDATCAR has exist. Please remove\033[0m")
        exit()
    else:
        write_content(gogal_path,head)

def get_file_content(poscar_path_dict,gogal_path):
    content = []
    num = get_num()
    pri("Total POSCAR was {0}".format(len(num)))
    constant = "Direct configuration=  "
    shu = 0
    for n in range(len(num)):
        shu += 1
        try:
            POSCAR_path = poscar_path_dict[num[n]]
        except KeyError:
            pri(" \033[0;31m KeyError: The file named \033[0;35mPOSCAR{0}\033[0;31m was not found\033[0m".format(num[n]))
            pri("Total has written POSCAR were \033[0;32m{0}\033[0m".format(shu-1))
            exit()
        constant = constant + num[n] + '\n'
        content.append(constant)
        f = open(POSCAR_path)
        c = f.readlines()
        for m in range(8,len(c)):
            content.append("  "+c[m])
        pri("Current were \033[0;32mPOSCAR{0}\033[0m".format(num[n]))
        write_content(gogal_path,content)
        content = []
        constant = 'Direct configuration=  '
        f.close()
    pri("Total write were {0}".format(len(num)))

def write_content(gogal_path, content):
    for i in range(len(content)):
        open(gogal_path, 'a').write(content[i])

def _remove_path(path):
    if os.path.exists(path):
        print('!!!!!!!!!!!!!!!!!!!! {0} exists, Removed!!!'.format(path))
        os.remove(path)

def choose(num,nowpath,POSCAR_path,dict_pocar_path):
    gogal_path = os.path.join(nowpath,'XDATCAR')
    if int(num) == 1:
        _remove_path(gogal_path)
        get_head_file(POSCAR_path[0], gogal_path)
        get_file_content(dict_pocar_path, gogal_path)
    elif int(num) == 2:
        get_file_content(dict_pocar_path, gogal_path)
    else:
        pri(" please set num !!! ")
        exit()

def RunMain():
    start = time.time()
    readme()
    nowpath = get_path()[0]
    POSCAR_path, dict_pocar_path= get_all_poscar()
    '''num=1 write XDATCAR from initial
       num=2 write XDATCAR continue'''
    num = 1
    choose(num,nowpath,POSCAR_path,dict_pocar_path)
    alltime = time.time() - start
    tail(alltime)

if __name__ == '__main__':
    RunMain()
