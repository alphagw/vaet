#!/usr/bin/python
#encoding=utf-8
import os
import re
import shutil
from optparse import OptionParser
try:
    from ase.io.trajectory import Trajectory
    from ase.io import read, write
    from ase import Atoms
except ModuleNotFoundError:
    print('''Please use 'pip install ase' to install ase module''')
    exit()
"""
used to get poscar from ***.traj file which generated from ASE MD
Example:
    ReadAseTrajectory.py -n 1,10,1
"""
__author__ = "Guanjie Wang"
__email__ = "wangguanjie@buaa.edu.cn"
__date__ = "Jan , 2018"

def readme():
    print(('-'*60).center(90))
    _pri_center('This was used to get poscar from ASE MD *.traj ')
    _pri_center('You can use -n to control the number of POSCAR ')
    print(('-'*60).center(90))

def _pri_center(content,num=58):
    print(' ' * 15 + '|' + content.center(num, ' ') + '|' + ' ' * 15)

def get_path():
    nowpath = os.getcwd()
    for i in os.listdir(nowpath):
        if re.findall(r'.traj',i):
            return os.path.join(nowpath,i)

def _get_num(star,stop,space):
    return [x for x in range(int(star),int(stop)+1,int(space))]

def _remove_path(path):
    if os.path.exists(path):
        print('{0} exists, Removed!!!'.format(path))
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)

def read_trajectory(option_number):
    path = get_path()
    traj = Trajectory(path)
    gogal_path = os.path.join(os.getcwd(),'read_traj_poscar')
    _remove_path(gogal_path)

    if option_number == 'all':
        star,stop,space =(1,len(traj),1)
    else:
        star, stop, space = [int(a) for a in option_number.split(',')]
    if stop > len(traj):
        stop = len(traj)
    num = _get_num(star,stop,space)

    for i in num:
        atoms = traj[i-1]
        name = os.path.join(gogal_path,'POSCAR'+str(i))
        write(name,atoms,format='vasp',direct=True)
        _change_style(name)

def _change_style(gogal_file_name):
    '''This was used to convert vasp4 to vasp5 format'''
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
    usage = '%prog [option]-n arg1'
    parser = OptionParser(usage)
    parser.add_option('-n','--number',default='all',help='contorl number,defaule was all,eg:1,16,2')
    (option,args) = parser.parse_args()
    return option.number

if __name__ == "__main__":
    readme()
    option_number = option_parser()
    read_trajectory(option_number)