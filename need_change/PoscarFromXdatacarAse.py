#!/usr/bin/python
#encoding=utf-8
import os
import shutil
from optparse import OptionParser
try:
    import ase.io
except ModuleNotFoundError:
    print('''Please use 'pip install ase' to install ase module''')
    exit()
"""
According to ASE module split XDATCAR to POSCAR 
python 2.* have bug, so used python 3.*
if you only have python2.* or you don't have ASE module. Please use PoscarFromXdatcar_noASE.py
All file saved in split_xdatcar file 
Example :
    PoscarFromXdatacarAse.py -n 1,100,10 -f 2

TODO:
    change style. For each row on its
"""
__author__ = "Guanjie Wang"
__email__ = "wangguanjie@buaa.edu.cn"
__date__ = "Jan 18, 2018"


def split_xdatcar(F_or_T,option_number):
    all_configure = ase.io.read('XDATCAR', index=':')
    if option_number == 'all':
        star,stop,space =(1,len(all_configure),1)
    else:
        star, stop, space = [int(a) for a in option_number.split(',')]
    if stop > len(all_configure):
        print('wrong,out of range,total steps was {0}'.format(len(all_configure)))
        exit()
    else:
        number = _get_num(star,stop,space)
        print('total configure was {0}'.format(len(number)))
    gogal_file_path = os.path.join(os.getcwd(),'split_xdatcar')
    _remove_path(gogal_file_path)
    for i in number:
        gogal_file_name =os.path.join(gogal_file_path, 'POSCAR' + str(i))
        ase.io.write(gogal_file_name,all_configure[i-1],format='vasp',direct=F_or_T)
        _change_style(gogal_file_name)

def readme():
    print(('-'*60).center(90))
    _pri_center('This was used to split XDATCAR to POSCAR')
    _pri_center('Now path must have XDATCAR')
    _pri_center('The version of python 2.* have bug,so only used python 3.*')
    _pri_center("if you only have python2.* or you don't have ASE module.")
    _pri_center("Please use PoscarFromXdatcar_noASE.py")
    print(('-'*60).center(90))

def _remove_path(path):
    if os.path.exists(path):
        print('{0} exists, Removed!!!'.format(path))
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)

def _pri_center(content,num=58):
    print(' ' * 15 + '|' + content.center(num, ' ') + '|' + ' ' * 15)

def _get_num(star,stop,space):
    return [x for x in range(int(star),int(stop)+1,int(space))]

def _change_style(gogal_file_name):
    f = open(gogal_file_name,'r')
    content = f.readlines()
    f.close()
    os.remove(gogal_file_name)
    final = []
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

def _style_each_line(line_list):
    space = '  '
    return space + line_list[0] + space + line_list[1] + space + line_list[2] +'\n'

def option_parser():
    usage = '%prog [option] [arg1] [option] [arg2]' \
            'ReadAseTrajectory.py -f 1 -n 1,16,2'
    parser = OptionParser(usage)
    parser.add_option('-f','--F_or_T',action='store',default='1',
                      help='''Choose Fraction or Cartesian, 1:represent Fraction, 2:represent Cartesian
                           Default was 1''')
    parser.add_option('-n','--number',default='all',help='contorl number,defaule was all,eg:1,16,2')
    (option,args) = parser.parse_args()
    if option.F_or_T == '1':
        return True,option.number
    else:
        return False,option.number

if __name__ == "__main__":
    false_or_true,option_number = option_parser()
    readme()
    split_xdatcar(false_or_true,option_number)