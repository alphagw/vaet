#!/usr/bin/python
#encoding=utf-8
# writed by WGJ

import re
import os
import time
import sys

'''
提取XDATACAR中数据分解为单个的POSCAR
'''
def readme():
    print('#'*90)
    print('#'*90)
    print('This script used for automaticly generate XSF format file for periodic structure'.center(90,' '))
    print('You must have XDATCAR in current path'.center(90,' '))
    print("\033[0;31m Waring!!!\033[0;35m Never change format of XDATCAR\033[0m ".center(90,' '))
    print('#' * 90)
    print('#' * 90)

def control():
    print('Please input number which you want to begin：')
    star =  raw_input()
    print('Please input number which you want to stop：')
    stop =  raw_input()
    print('Please input number which you want to space：')
    space = raw_input()
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


def get_timestep_and_linenumber(general_line,atoms):
    path = get_path()
    catch = r'Direct configuration=(.*)'
    f = open(path)
    number = f.readlines()
    timestep_all = []
    linenumber = []

    for i in range(int(general_line), len(number),(int(atoms)+1)):
        timestep = re.findall(catch, number[i])
        if len(timestep) > 0:
            timestep_all.append(timestep[0].replace(' ', ''))
            linenumber.append(i)
        else:
            print('\033[0;31m Waring!!! \033[0;35m The script is breakdown \033[0m')
            exit()

    Configuration = len(timestep_all)
    print("\033[0;32m The XDATCAR has {0} configures\033[0m".format(Configuration))
    step_ene = dict(zip(timestep_all, linenumber))
    return step_ene

def get_gogal_timestep(headline, atoms):
    all_timestep = get_timestep_and_linenumber(headline, atoms)
    gogalnumber = get_num()
    wrong_configure = []
    record = []
    gogalline = []
    for i in range(len(gogalnumber)):
        if gogalnumber[i] in all_timestep.keys():
            line = all_timestep[gogalnumber[i]]
            gogalline.append(line)
        else:
            print('The XDATCAR file do not have \033[0;31m Direct configuration= {0} \033[0m timestep configure'.format(gogalnumber[i]))
            wrong_configure.append(gogalnumber[i])
            record.append(i)
            continue

    for m in range(len(record)):
        del gogalnumber[record[m]]
    step_ene = dict(zip(gogalnumber,gogalline))
    return step_ene

def _remove_path(path):
    if os.path.exists(path):
        os.remove(path)
        print(' \033[0;31m!!!!! This file "{0}" exists, removed\033[0;m'.format(path.split('\\')[-1]))

def write_poscar(headline,atoms):
    #获得路径打开文件内容
    path = get_path()
    f = open(path)
    number = f.readlines()
    #得到时间步长
    GogalTimeStep = get_gogal_timestep(headline,atoms)
    timestep = list(GogalTimeStep.keys())

    for xx in range(len(timestep)):
        #创建时间步相对应的文件
        nowpath = os.path.dirname(path)  # 脚本当前运行的目录
        file_name = os.path.join(nowpath, 'POSCAR'+timestep[xx])
        _remove_path(file_name)
        # 加上POSCAR开始的7行文件
        for a in range(0,int(headline)):
            open(file_name, 'a').write(number[a])

        # 写入每一个configuration的结构
        starline = int(GogalTimeStep[timestep[xx]])
        stopline = starline + int(atoms) + 1
        for i in range(starline,stopline):
            open(file_name, 'a').write(number[i])

    f.close()

# def get_data(general_line,atoms,setnumber):
# #获取每一行数据返回列表
#     path = get_path()
#     catch = r'Direct configuration=(.*)'
#     f = open(path)
#     number = f.readlines()
#
#
#
#
#
#
# # 初始化startline 和 file_name值
#     for i in range(0,len(number)):
#         timestep = re.findall(catch, number[i])
#         startline = 0
#         file_name = ''
#         if len(timestep) > 0 :
#             timestep = timestep[0].strip()
#             startline = i+1                  #第一行的startline开始行数
#             file_name = timestep + '/POSCAR'    #此时时间步对应的名字
#             break
#
#
# #获得从configuration开始的所有结构
#     for i in range(0,len(number)):
#         timestep = re.findall(catch, number[i])
#         timestep = timestep[0].strip()
#         if (len(timestep) > 0) & (timestep in setnumber):
#             nowpath = os.path.dirname(path) #脚本当前运行的目录
#             filepath = os.path.join(nowpath,timestep)
#             os.mkdir(filepath)
#             file_name = filepath+'/POSCAR'
#             #加上POSCAR开始的7行文件
#             for a in range(0, len(number)):
#                 if a < general_line :
#                     open(file_name, 'a').write(number[a] + '\n')
#             startline = i+1
#         #写入每一个configuration的结构
#             if i >= startline-1 and i < startline+atoms:
#                 open(file_name,'a').write(number[i]+'\n')
#                 continue
#     f.close()

#获取当前路径,返回当前路径下的XDATCAR路径
def get_path():
    ppp = os.popen('pwd').read().replace('\n', '')
    ath = os.listdir(ppp)
    path = ''
    for i in range(len(ath)):
        if len(re.findall('XDATCAR',ath[i])) > 0:
            path = os.path.join(ppp,ath[i])
            break
    if len(path) > 0:
        pass
    else:
        print("Don't have XDATCAR")
        exit()
    return path

def get_number_of_atome_and_headline():
    atoms = 0
    path = get_path()
    f = open(path)
    contents = f.readlines()
    position = []    #用于删除在提取原子个数中的空格
    for m in range(len(contents)):
        #在第6行寻找原子个数
        if m == 6:
            content = contents[m].strip().split(' ')
            for i in range(len(content)):
                if len(content[i]) == 0:
                    position.append(i)
            for m in range(len(position)):
                del content[position[m]]
            if len(content) == 2:
                atoms = str(int(content[0]) + int(content[1]))
        #找到头文件在哪几行
        if re.findall(r'Direct configuration=(.*)',contents[m]):
            if atoms != 0:
                f.close()
                return str(m),atoms
            else:
                print("Don't find \033[0;31m atoms \033[0m in 7th line of XDATCAR, Please ensure the XDATCAR file is right")
                exit()

#主函数
def run_ene():
    start = time.time()
    readme()
    headline, atoms = get_number_of_atome_and_headline()  # 获得头文件的行数以及原子个数
    write_poscar(headline,atoms)
    totaltime = time.time()-start
    print("Total Running Time：\033[0;36m {0} s，\033[0;35m {1} h \033[0m ".format(totaltime,totaltime/3600))

if __name__ == '__main__':
    run_ene()
