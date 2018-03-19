#!/usr/bin/python
#encoding=utf-8
import os
import re
import shutil
from optparse import OptionParser
try:
    import ase.io
except ModuleNotFoundError:
    print('''Please use 'pip install ase' to install ase module''')
    exit()
"""
You can use -t 1 convert one poscar with cartesian coordinate to fraction coordinate
You can use -t 2 convert one poscar with fraction coordinate to cartesian coordinate
You also can convert many poscar to gogal posacar, use -m filepath
All gogal poscar was saved in convert_poscar file
Example:
    Default: ConvertCoordinate.py #now path must have one 'POSCAR' file and will change one poscar to fraction poscar
    ConvertCoordinate.py -m all_pocar_path -t 1 #change many poscar to fraction poscar 
    ConvertCoordinate.py -m all_pocar_path -t 2 #change many poscar to cartesian poscar
    ConvertCoordinate.py -t 1                   #change one poscar to fraction poscar like ConvertCoordinate.py
    ConvertCoordinate.py -t 2                   #change one poscar to cartesian poscar 
"""
__author__ = "Guanjie Wang"
__email__ = "wangguanjie@buaa.edu.cn"
__date__ = "Jan 18, 2018"

def convert_fration_to_cartesian(poscar_path,gogal_path):
    a = ase.io.read(poscar_path, format='vasp')
    ase.io.write(gogal_path, a, format='vasp', direct=False)
    _change_style(gogal_path)

def convert_cartesian_to_fraction(poscar_path,gogal_path):
    a = ase.io.read(poscar_path, format='vasp')
    ase.io.write(gogal_path, a, format='vasp', direct=True)
    _change_style(gogal_path)

def get_structure_path(structure_path):
    path = list(os.walk(structure_path))
    file_path = []
    for i in range(len(path)):
        for m in range(len(path[i][2])):
            if re.findall(r'POSCAR', path[i][2][m]):
                file_path.append(os.path.join(path[i][0], path[i][2][m]))
    num = str(len(file_path))
    return num, file_path

def _remove_path(path):
    if os.path.exists(path):
        print('{0} exists, Removed!!!'.format(path))
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)

def _change_style(gogal_file_name):
    f = open(gogal_file_name,'r')
    content = f.readlines()
    f.close()
    os.remove(gogal_file_name)
    final = []

    def _style_each_line(line_list):
        space = '  '
        return space + line_list[0] + space + line_list[1] + space + line_list[2] + '\n'

    for i in range(len(content)):
        if i == 0:
            a6 = '  '+'  '.join(content[i].split()) +'\n'
        if content[i].startswith(' ') and '.' in content[i] and i != 1:
            position =  content[i].split()
            final_position = ['%.8f'%round(float(b),8) for b in position]
            final.append(_style_each_line(final_position))
        else:
            final.append(content[i])
    final.insert(5,a6)
    for m in final:
        open(gogal_file_name,'a').write(m)


def option_parser():
    usage = '%prog [option]-n arg1 [option]-f arg2' \
            'eg: ConvertCoordinate.py -m all_pocar_path -t 2'
    parser = OptionParser(usage)
    parser.add_option('-m','--many_path',action='store',default='1',
                      help='''if you have many poscar, put them in one total file and input total file name
                           Default was one poscar''')
    parser.add_option('-t','--task',default='1',help='1: convert cartesian to fraction'
                                                     '2: convert fraction to cartesian'
                                                     'Default was 1')
    (option,args) = parser.parse_args()

    if option.many_path == '1':
        return 'POSCAR',option.task
    else:
        return option.many_path,option.task

def main():
    filepath, task = option_parser()
    if filepath != 'POSCAR':
        num,file_path = get_structure_path(filepath)
        print('total poscar was {0}'.format(num))
        gogal_path = os.path.join(os.getcwd(),'convert_poscar')
        _remove_path(gogal_path)
        for i in file_path:
            if task == '1':
                each_gogal_path = os.path.join(gogal_path, i.split('\\')[-1] + '_fraction')
                convert_cartesian_to_fraction(i,each_gogal_path)
            else:
                each_gogal_path = os.path.join(gogal_path, i.split('\\')[-1] + '_cartesian')
                convert_fration_to_cartesian(i,each_gogal_path)
    else:
        if task == '1':
            convert_cartesian_to_fraction('POSCAR', 'POSCAR_fraction')
        else:
            convert_fration_to_cartesian('POSCAR','POSCAR_cartesian')

if __name__ == "__main__":
    main()