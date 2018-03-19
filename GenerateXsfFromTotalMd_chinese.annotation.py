#!/usr/bin/python
#encoding=utf-8
import os
import re
import shutil
import time
import copy
from optparse import OptionParser
"""
This was used to automaticly produce *.xsf file
Current path must have OUTCAR file
"""
__author__ = "Guanjie Wang"
__email__ = "wangguanjie@buaa.edu.cn"
__date__ = "Oct. 1, 2017"

def new_vasp2force(OUTCARpath,number,gogal_path):
    f = open(OUTCARpath, 'r')
    data = []
    max_types = 1
    # 为了获得所有OUTCAR的configure、types和atoms
    data.append(_scan_outcar_file(f))
    configures = number
    f.close()
    #控制类型
    max_types = max(max_types, len(data[-1][1]))
    #控制原子数
    natoms = sum(data[-1][2])
    #对每一个进行下面操作
    count = 0
    #对元素种类操作
    numbers=['0','1','2']
    f = open(OUTCARpath, 'r')
    #调用这一步的时候就会写入文件
    total_number = _process_outcar_file_v5(OUTCARpath, f , natoms, count,data,max_types,configures,numbers,gogal_path)
    f.close()
    return natoms,total_number
def _scan_outcar_file(file_handle):
    # first try TOTAL-FORCE
    configs = 0
    atom_types = []
    titel = []
    ipt = []
    potcar = []
    for line in file_handle:
        if line.startswith('|'):
            continue
        if 'TOTAL-FORCE' in line:
            configs += 1
        if 'VRHFIN' in line:
            atom_types.append(line.split()[1].replace('=','').replace(':',''))
        if 'TITEL' in line:
            titel.append(line.split()[3][0:2])
        if 'ions per type' in line:
            ipt = [int(s) for s in line.split()[4:]]
        if 'POTCAR' in line:
            potcar.append(line.split()[2][0:2])
        if atom_types and ipt:
            return [configs, atom_types, ipt]
        if potcar and ipt:
            return [configs,potcar,ipt]
    exit('Could not determine atom types in file OUTCAR')
def _process_outcar_file_v5(OUTCARpath,f, natoms, count,data,max_types,configs,numbers,gogal_path):
    total_number = 0
    final_list = []
    #循环OUTCAR
    line = f.readline()
    while line != '':
        line = f.readline()
        #迭代开始
        if 'Iteration' in line:
            energy = 0
            box_x = []
            box_y = []
            box_z = []
            stress = []
            atom_data = []
       #获取晶胞cell信息
        if 'VOLUME and BASIS' in line:
            for do in range(5):
                line = f.readline()
            box_x = [float(s) for s in line.replace('-',' -').split()[0:3]]
            line = f.readline()
            box_y = [float(s) for s in line.replace('-',' -').split()[0:3]]
            line = f.readline()
            box_z = [float(s) for s in line.replace('-',' -').split()[0:3]]
        #获得压强信息
        if 'in kB' in line:
            stress = [float(s)/1602 for s in line.split()[2:8]]
        #获得力学信息
        if 'TOTAL-FORCE' in line:
            count += 1
            line = f.readline()
            adata = [0] * 7
            for num in range(len(data[-1][2])):
                for k in range(data[-1][2][num]):
                    line = [float(s) for s in f.readline().split()[0:6]]
                    if not 1:
                        adata[0] = int(types[data[-1][1][num]])
                    else:
                        adata[0] = int(num)
                    adata[1] = float(line[0])
                    adata[2] = float(line[1])
                    adata[3] = float(line[2])
                    adata[4] = float(line[3])
                    adata[5] = float(line[4])
                    adata[6] = float(line[5])
                    atom_data.append(copy.copy(adata))
        #获得能量信息
        if 'energy  without' in line:
            #可以修改能量
            energy = float(line.split()[6])
            #获得能量信息之后表示本次迭代结束，开始输出
            if str(count) in configs:
                total_number += 1
                penult_list = []
                a1 = "#N %s 1" % natoms
                a2 = "#C"
                if not 1:
                    print(" %s" % numbers[0])
                    for j in range(1, max_types):
                        print(' %s' % numbers[j])
                else:
                    a2 += " %s" % data[-1][1][0]
                    for j in range(1, max_types):
                        a2 += ' %s' % data[-1][1][j]
                a3 = "## force file generated from file {0} config {1}".format(OUTCARpath, count)
                a4 = "#X {0:13.8f} {1:13.8f} {2:13.8f}".format(box_x[0], box_x[1], box_x[2])
                a5 = "#Y {0:13.8f} {1:13.8f} {2:13.8f}".format(box_y[0], box_y[1], box_y[2])
                a6 = "#Z {0:13.8f} {1:13.8f} {2:13.8f}".format(box_z[0], box_z[1], box_z[2])
                weight = 1.0
                a7 = "#W {0:f}".format(weight)
                a8 = "#E {0:.10f}".format(energy)
                a9 = '#S'
                if stress:
                    for num in range(6):
                        a9 += ' {0:8.7g}'.format(stress[num])
                a10 = "#F"
                penult_list.append(a1)
                penult_list.append(a2)
                penult_list.append(a3)
                penult_list.append(a4)
                penult_list.append(a5)
                penult_list.append(a6)
                penult_list.append(a7)
                penult_list.append(a8)
                penult_list.append(a9)
                penult_list.append(a10)
                for adata in atom_data:
                    b ="{0} {1:11.7g} {2:11.7g} {3:11.7g} {4:11.7g} {5:11.7g} {6:11.7g}".format(
                        adata[0], adata[1], adata[2], adata[3], adata[4], adata[5], adata[6])
                    penult_list.append(b)
                final_list.append(penult_list)
                _write_generate(gogal_path,count,penult_list,str(energy))
                if total_number /100.0 == 0:
                    print("Have writen {0} xsf files".format(total_number))
                if str(count) == configs[-1]:
                    break

    if len(final_list) == len(configs):
        final_dict = dict(zip(configs,final_list))
        return total_number
    else:
        print("\033[0;33mWaring!!! Breaking!!! Beyond range")
        print("Waring: total configure are {0}, but you input were {1}".format(count,configs[-1]))
        print("\033[0;36mHave writen {0} xsf files\033[0m".format(total_number))
        return total_number
def _write_generate(gogal_path,count,force_list,ene_str):
    content = []
    name = str(count).zfill(5) + '.xsf'  #写个5位字符串，不足的补充0
    name_path = os.path.join(gogal_path, name)
    print('The present task is \033[0;32m{0}\033[0m th.'.format(count))
    three_main_line = _get_line(force_list)
    fir = ene_str.replace(' ', '')
    firstline = '#total energy = ' + fir + ' eV' + '\n'
    content.append(firstline)
    secondline = '\n'
    content.append(secondline)
    thirdline = 'CRYSTAL\n'
    content.append(thirdline)
    fourthline = 'PRIMVEC\n'
    content.append(fourthline)
    fifthline = three_main_line[0]
    content.append(fifthline)
    sixthline = 'PRIMCOORD\n'
    content.append(sixthline)
    seventhline = three_main_line[1]
    content.append(seventhline)
    eighthline = three_main_line[2]
    content.append(eighthline)
    for x in range(0, len(content)):
        if not isinstance(content[x], list):
            open(name_path, 'a').write(content[x])
        else:
            for m in range(0, len(content[x])):
                open(name_path, 'a').write(content[x][m])
#该函数严格依赖vasp2force生成的force文件
def _get_line(force_list):
    line = force_list
    atomic_coordinate = []
    position_force = []
    seven = ''
    number = 0
    #得到X,Y,Z的坐标，返回列表
    for i in range(0,len(line)):
        if i == 0:
            atomic_num  = re.findall(r'\d+',line[i])
            seven = atomic_num[0]+' '+atomic_num[1]+'\n'
        elif i == 1:
            elements = re.findall(r'#C(.*)',line[i])[0].split()
        elif i >= 3 and i <=5:
            fif = re.findall(r'#[A-Z](.*)',line[i])
            atomic_coordinate.append(fif[0]+'\n')
        elif len(re.findall(r'F',line[i])) >0:
            number = i+1
            break
    #将0,1,2 替换为元素符号，最多支持三个元素
    #并将所有的每一行返回一个列表
    for x in range(number,len(line)):
        every_line = line[x].split()
        if every_line[0] == '0':
            line[x] = line[x].replace('0',elements[0],1)
        elif every_line[0] == '1':
            line[x] = line[x].replace('1',elements[1],1)
        elif every_line[0] == '2':
            line[x] = line[x].replace('2',elements[2],1)
        position_force.append(line[x]+'\n')
    #print('Atomic position and force total are %d rows. This shoule equal to atomic numbers '%len(position_force))
    return atomic_coordinate,seven,position_force

def get_path(work_path):
    work_file = os.listdir(work_path)
    for i in work_file:
        if re.findall(r'OUTCAR',i):
            outcarpath = os.path.join(work_path,i)
            break
    if outcarpath:
        gogal_path = os.path.join(work_path,'gogal')
        if os.path.exists(gogal_path):
            print("The gogal path exits. Deleted")
            time.sleep(1)
            rm = 'yes'
            if rm == 'yes':
                shutil.rmtree(gogal_path)
                os.mkdir(gogal_path)
            else:
                exit("Can't delete exit force!!! So the script must stop")
        else:
            os.mkdir(gogal_path)
        return outcarpath,gogal_path
    else:
        exit("wrong! Don't find OUTCAR file")
def get_num(star,stop,space):
    return [str(x) for x in range(int(star),int(stop)+1,int(space))]
def parse_option():
    usage = "%prog -n arg1  eg:%prog -n 1,50000,10"
    parse = OptionParser(usage)
    parse.add_option('-n','--number',action='store',type='string',dest='num',default='1,50000,10',
                     help='''input star,stop,space number 
                     \033[0;32meg: -n 1,50,5\033[0m means from 1 to 50 interval 5
                     default: star=1,stop=50000,space=10''',metavar='inter number')
    (option,args) = parse.parse_args()
    star,stop,space = option.num.split(',')
    try:
        return int(star),int(stop),int(space)
    except ValueError:
        exit('\033[0;31mValueError: please input inter number\033[0m')
def readme():
    print(('-'*60).center(90))
    _pri_center('This was used to automaticly produce *.xsf')
    _pri_center("\033[0;35mNecessary\033[0m: VASP's OUTCAR file",69)
    _pri_center('All *.XSF were stored in gogal file')
    _pri_center('You can use -n input start stop and space to control')
    print(('-'*60).center(90))
def _pri_center(content,num=58):
    print(' ' * 15 + '|' + content.center(num, ' ') + '|' + ' ' * 15)
def tail(filenumbers,alltime,gogalpath):
    print(('-' * 60).center(90))
    _pri_center('Congratulation!!!!!')
    _pri_center('You have successfully make \033[0;36m### %d ###\033[0m XSF files '% filenumbers,69)
    _pri_center('*.XSF stored in gogal file')
    _pri_center('\033[0;32mTime used was {0} s\033[0m'.format(alltime),69)
    print(('-' * 60).center(90))
def main(path):
    startime = time.time()
    readme()
    star, stop, space = parse_option()
    OUTCARpath,gogal_path = get_path(path)
    control_number = get_num(star,stop,space)
    natoms,filenumbers = new_vasp2force(OUTCARpath,control_number,gogal_path)
    alltime = time.time() - startime
    tail(filenumbers,alltime,gogal_path)
if __name__ == "__main__":
    path = os.getcwd()
    main(path)

