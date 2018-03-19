#!/usr/bin/python
#encoding=utf-8
import os
import re
"""
Single atom energy default was 0 eV, you can manually change in generate.in file
Structure path should contain all you need .xsf file
Support python3.*
"""

__author__ = "Guanjie Wang"
__email__ = "wangguanjie@buaa.edu.cn"
__date__ = "Oct. 1, 2017"

def readme():
    print(('-'*60).center(90))
    _pri_center('This was used to generate generate.in file')
    _pri_center('\033[0;35mNecessary\033[0m: File path which include all xsf files')
    _pri_center('The *.fingerprint file must in now path')
    print(('-'*60).center(90))

def tail():
    print(('-' * 60).center(90))
    _pri_center('You have successfully produce generate.in files ')
    print(('-' * 60).center(90))

def _pri_center(content):
    print(' ' * 15 + '|' + content.center(58, ' ') + '|' + ' ' * 15)

def finger_path_and_element(gogalpath):
    path = os.listdir(gogalpath)
    element_and_fingername = {}
    for i in range(0, len(path)):
        if len(re.findall(r'fingerprint.stp', path[i])) > 0:
            f = open(os.path.join(gogalpath,path[i]))
            content = f.readlines()
            for m in content:
                if re.findall(r'ATOM(.*)',m):
                    element = str(re.findall(r'ATOM(.*)',m)[0]).strip()
                    element_and_fingername[element] = path[i]
                    break
            f.close()
    if len(element_and_fingername) <= 0:
        exit("Current path lack of *.fingerprint files ")
    return element_and_fingername

def get_output():
    n = input('Please input output name:')
    firstline = 'OUTPUT'+'  '+ n +'\n'
    return firstline,'\n'

def get_types(element):
    firstline = 'TYPES\n'
    ele_energy = {}
    for i in element:
        ele_energy[i] = '0'
    return firstline,ele_energy,'\n'

def get_setups(element__and_fingername):
    firstline = 'SETUPS\n'
    return firstline,element__and_fingername,'\n'

def get_structure_path(structure_path):
    path = list(os.walk(structure_path))
    file_path = []
    for i in range(len(path)):
        for m in range(len(path[i][2])):
            if re.findall(r'.xsf',path[i][2][m]):
                file_path.append(os.path.join(path[i][0],path[i][2][m])+'\n')
    firstline = 'FILES\n'
    num = str(len(file_path)) + '\n'
    return firstline,num,file_path

def all_together(output,types,setups,path):
    #output
    total_content = []
    total_content.extend(output)
    #tpyes
    name_ene = [keys+'  '+values+'\n' for keys,values in types[1].items()]
    name_ene.insert(0,types[0])
    name_ene.insert(1,str(len(types[1])) + '\n')
    name_ene.append(types[-1])
    total_content.extend(name_ene)
    #setups
    name = [keys + '  ' + values + '\n' for keys, values in setups[1].items()]
    name.insert(0, setups[0])
    name.append(setups[-1])
    total_content.extend(name)
    #path
    file_path = [path[0],path[1]]
    file_path.extend(path[2])
    total_content.extend(file_path)
    return total_content

def write(gogalpath,total_content):
    path = os.path.join(gogalpath, 'generate.in')
    if os.path.exists(path):
        os.remove(path)
    for i in total_content:
        open(path,'a').write(i)

def main(structurepath,gogalpath):
    readme()
    element_and_fingername = finger_path_and_element(gogalpath)
    element = list(element_and_fingername.keys())
    output = get_output()
    types = get_types(element)
    setups = get_setups(element_and_fingername)
    path = get_structure_path(structurepath)
    all_content = all_together(output,types,setups,path)
    write(gogalpath,all_content)
    tail()

if __name__ == "__main__":
    structurepath = r'your path'     #change this path
    gogalpath = os.getcwd()
    main(structurepath,gogalpath)