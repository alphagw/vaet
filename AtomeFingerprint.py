#!/usr/bin/python
#encoding=utf-8
import os
import re
"""
This was used to Used to generate atomtype fingerprint
"""
__author__ = "Guanjie Wang"
__email__ = "wangguanjie@buaa.edu.cn"
__date__ = "Oct. 1, 2017"

def readme():
    print(('-'*60).center(90))
    _pri_center('This was used to Used to generate atomtype fingerprint')
    _pri_center('Only uesed for Two type of atoms, not for Three')
    print(('-'*60).center(90))

def tail():
    print(('-' * 60).center(90))
    _pri_center('Congratulation!!!!!')
    _pri_center('You have successfully produce fingerprint files ')
    print(('-' * 60).center(90))

def pri(content):
    print('*' * 90)
    print(content)

def _pri_center(content):
    print(' ' * 15 + '|' + content.center(58, ' ') + '|' + ' ' * 15)

def get_DESCR():
    pri('Please input text describes the structural fingerprint setup')
    txt = input()
    firstline = 'DESCR\n'
    secondline = '  ' +txt+'\n'
    thirdline = 'END DESCR\n'
    return [firstline,secondline,thirdline,'\n']

def get_Atom_ENV_RMIN(type):
    atom = 'ATOM'+' '+type +'\n'
    pri('Please input the atomic species in the enviroment of the central atom')
    print('If the number of atomic more than 1, separated by the space bar')
    atom_type = input()
    env = [x + '\n' for x in atom_type.split()]
    firstline_env = 'ENV' +'  ' + str(len(env)) +'\n'
    env.insert(0,firstline_env)
    #写入RMIN部分
    pri('Please input the minimal allowed distance between two atoms which unit used in XSF file')
    rmin_distance = input()
    rmin = 'RMIN'+' '+str(rmin_distance)+'d0\n'
    return atom,'\n',env,'\n',rmin,'\n'

def get_function(atoms):
    function = []
    firstlin_func = 'FUNCTIONS type=Behler2011' + '\n'
    function.append(firstlin_func)
    pri("Please input 'eta for distance' , separated by space bar ")
    num3  = input()
    pri("Please input 'Rs for distance' , separated by space bar ")
    num7 = input()
    pri("Please input 'eta for angle', separated by space bar ")
    num4 = input()
    pri("Please input 'zeta for angle', separated by space bar ")
    num5 = input()
    pri("Please input the cutoff distance 'Rc', separated by space bar ")
    num6 = input()
    atom = [x.replace('\n','') for x in atoms]
    distance_eta = num3.split()
    angle_eta = num4.split()
    zeta = num5.split()
    Rc = num6.split()
    Rs = num7.split()
    lamb = ['-1.0','1.0']
    #判断原子个数
    if len(atom) == 2:
        for r in range(len(Rc)):
            for s in range(len(Rs)):
                for i in range(len(distance_eta)):
                    for j in range(len(atom)):
                        function.append('G=2 type2='+atom[j]+'  eta='+distance_eta[i]+'  Rs='+ Rs[s] + '  Rc='+Rc[r] + '\n')
        for ar in range(len(Rc)):
            for z in range(len(zeta)):
                for l in range(len(lamb)):
                    for e in range(len(angle_eta)):
                        function.append('G=4 type2='+atom[0]+'  type3='+atom[0]+'  eta='+angle_eta[e]+'  lambda='+lamb[l]+'  zeta='+zeta[z]+'  Rc='+Rc[ar] +'\n')
                        function.append('G=4 type2='+atom[0]+'  type3='+atom[1]+'  eta='+angle_eta[e]+'  lambda='+lamb[l]+'  zeta='+zeta[z]+'  Rc='+Rc[ar] +'\n')
                        function.append('G=4 type2='+atom[1]+'  type3='+atom[1]+'  eta='+angle_eta[e]+'  lambda='+lamb[l]+'  zeta='+zeta[z]+'  Rc='+Rc[ar] +'\n')
        num_distance_func = len(distance_eta)*2*len(Rc)*len(Rs)
        num_angle_func = len(zeta)*len(lamb)*len(angle_eta)*3*len(Rc)
        pri("total distance function are {0}".format(num_distance_func))
        pri("total angle function are {0}".format(num_angle_func))

        secondline_fuc = str(num_distance_func + num_angle_func) + '\n'
        function.insert(1,secondline_fuc)
    elif len(atom) == 3:
        pri("暂时不支持三个原子的对称函数，还没有想好")
        exit()
    else:
        pri('The number is too large or too small, must was 2 atoms')
        exit()
    return function

def write_file(path,descr,atom,function):
    if os.path.exists(path):
        pri("The file is exist, delete ")
        os.remove(path)
    for d in descr:
        open(path,'a').write(d)
    for t in range(0,len(atom)):
        if isinstance(atom[t],list):
            for tt in range(0,len(atom[t])):
                open(path,'a').write(atom[t][tt])
        else:
            open(path,'a').write(atom[t])
    for f in function:
        open(path,'a').write(f)

def _remove_path(path):
    if os.path.exists(path):
        os.remove(path)
        print(' \033[0;31m!!!!! This file "{0}" exists, removed\033[0;m'.format(path.split('\\')[-1]))

def main(path):
    readme()
    pri('Please input atom type: ')
    ele_type = input()
    workpath = os.path.join(path, ele_type + '_fingerprint.stp')
    _remove_path(workpath)
    DESCR = get_DESCR()
    Atom_ENV_RMIN = get_Atom_ENV_RMIN(ele_type)
    atoms = Atom_ENV_RMIN[2][1:]
    Function = get_function(atoms)
    write_file(workpath, DESCR, Atom_ENV_RMIN, Function)
    tail()

if __name__ == "__main__":
    path = os.getcwd()
    main(path)