#!/usr/bin/python
#encoding=utf-8

import os
import re
import time

"""
This was used to deal predict data
You must set predict xsf path
TODO:
    according to predict.in path to get DFT energy
"""
__author__ = "Guanjie Wang"
__email__ = "wangguanjie@buaa.edu.cn"
__date__ = "Jan 17, 2018"

def readme():
    print(('-'*60).center(90))
    _pri_center('Two files was needed in current path')
    _pri_center('1. structure file which named ###.gogal')
    _pri_center('2. predict file which named mpredict.out')
    print(('-'*60).center(90))

def pri(content):
    print('*' * 90)
    print(content)

def _pri_center(content, num=58):
    print(' ' * 15 + '|' + content.center(num, ' ') + '|' + ' ' * 15)

def tail(alltime):
    print(('-'*60).center(90))
    _pri_center('Congratulation!!!!!')
    _pri_center('You have successfully get predict.energy files ')
    _pri_center('Total uesd time was {0}s, {1}h '.format(alltime,alltime/3600))
    print(('-'*60).center(90))

#获得预测的XSF文件总路径和predict.out路径
def get_path(gogalpath):
    path = os.getcwd()
    files = os.listdir(path)
    gogal_path = gogalpath
    pre_path = []
    for i in range(len(files)):
        if len(re.findall(r'gogal',files[i])) > 0:
            #gogal_path = os.path.join(path,files[i])
            pass
        elif len(re.findall(r'predict.out',files[i])) > 0:
            pre_path = os.path.join(path,files[i])
        if len(pre_path) > 0:
            return path,gogal_path,pre_path
    print('Please ensure the two file was exist!!!')
    exit()

# 输入总的路径，获得所有预测结构文件路径，所有XSF文件存放格式同generate过程，必须用含有关键词'gogal'的命名方式来命名
def find_structure_path(structure_path):
    path = list(os.walk(structure_path))
    file_path = []
    for i in range(len(path)):
        for m in range(len(path[i][2])):
            if re.findall(r'.xsf',path[i][2][m]):
                file_path.append(os.path.join(path[i][0],path[i][2][m]))
    firstline = 'FILES\n'
    num = str(len(file_path)) + '\n'
    return firstline,num,file_path

#获得DFT中的能量和文件名称
def grep_DFT_XSF_energy(gogalpath):
    energy = []
    atomnumber = []
    for i in range(len(gogalpath)):
        f = open(gogalpath[i],'r')
        b = f.readlines()
        f.close()
        for m in range(len(b)):
            if len(re.findall(r'#total',b[m])) > 0:
                e = re.findall(r'#total energy =(.*)eV',b[m])[0].replace(' ','')
                energy.append(e)
            if len(re.findall(r'PRIMCOORD',b[m]))> 0 and m < len(b)-3:
                xxx = re.findall(r'(.*)1',b[m+1])[0].replace(' ','')
                atomnumber.append(xxx)
        if len(energy)>0 and len(atomnumber)>0:
            pass
        else:
            print("Don't find DFT energy and atom number, Maybe the\033[0;31m XSF\033[0m file was wrong")
            exit()
    PathE = dict(zip(gogalpath,energy))
    ENum = dict(zip(energy,atomnumber))
    return PathE,ENum #第一个字典：路径对应能量；第二个字典，能量对应原子个数
#获取predict.out中所有有用信息
def grep_predict_energy(predictPath):
    f = open(predictPath,'r')
    content = f.readlines()
    f.close()
    start_line = 0
    StrucNum = []
    FileName = []
    AtomNum = []
    CohesiveEne = []
    TotalEne = []
    Force = []
    MaxForce = []
    MaxForceNum = []
    RmsForce = []
    StrucNum_filename = []
    #找到evaluatino开始的行
    for i in range(len(content)):
        if len(re.findall(r'Energy evaluation',content[i])) > 0:
            start_line = i
            break
    if start_line == 0:
        print('\033[0;31mWrong:\033[0mThe predict.out file do not have the content of predict\033[0m')
        exit()
    for m in range(start_line,len(content)):
        #结构序数
        struc_num =contrast_len('Structure number','',content[m])
        appen_value_to_list(struc_num,StrucNum)
        #文件路径
        #file_name =contrast_len('File name','',content[m])
        file_name = re.findall(r'File name(.*)',content[m])
        if len(file_name) > 0:
            ccccc = str(file_name[0].replace(':', '').strip())
            if len(ccccc) > 0:
                appen_value_to_list(ccccc,FileName)
                strucnum_filename = '--' + ccccc.split('/')[-1].replace('.xsf', '')
                appen_value_to_list(strucnum_filename, StrucNum_filename)
            else:
                appen_value_to_list(content[m+1].strip(),FileName)
                strucnum_filename = '--' + content[m+1].split('/')[-1].replace('.xsf', '')
                appen_value_to_list(strucnum_filename, StrucNum_filename)

        #原子个数
        atom_number =contrast_len('Number of atoms','',content[m])
        appen_value_to_list(atom_number,AtomNum)
        #结合能
        cohesive_ene =contrast_len('Cohesive energy','',content[m])
        cohesive_ene =cohesive_ene.replace('eV','').strip()
        appen_value_to_list(cohesive_ene,CohesiveEne)
        #总能
        total_ene =contrast_len('Total energy','',content[m])
        appen_value_to_list(total_ene,TotalEne)
        #平均作用力
        force =contrast_len('Mean absolute force','',content[m])
        appen_value_to_list(force,Force)
        #最大的作用力
        max_force =contrast_len('Maximum force','',content[m])
        appen_value_to_list(max_force,MaxForce)
        #最大作用力作用在哪个原子上
        max_force_num =contrast_len('The maximum force is acting on atom','',content[m])
        max_force_num = max_force_num.replace('.','')
        appen_value_to_list(max_force_num,MaxForceNum)
        #Root mean square force 力的均方根
        rms_force = contrast_len('RMS force','',content[m])
        appen_value_to_list(rms_force,RmsForce)
    print(len(StrucNum),len(FileName),len(AtomNum),len(CohesiveEne),len(TotalEne),len(Force),len(MaxForce),len(MaxForceNum),len(RmsForce),len(StrucNum_filename))
    if len(StrucNum) ==len(FileName) == len(AtomNum) ==len(CohesiveEne) ==len(TotalEne) ==len(Force) ==len(MaxForce) ==len(MaxForceNum) ==len(RmsForce) ==len(StrucNum_filename) !=0 :
        return StrucNum,FileName,AtomNum,CohesiveEne,TotalEne,Force,MaxForce,MaxForceNum,RmsForce,StrucNum_filename
    else:
        print("\033[0;31mWrong!!! The script was breakdown,Maybe predict.out was wrong")
        exit()
#写入所有信息，用来画图或者比较
def write_all_info(path,gogalpath,predictpath):
    filename = 'predict.allnformation'
    __path = os.path.join(path, filename)
    if os.path.exists(__path):
        os.remove(__path)
        print('The {0} file is exist. Removed!'.format(filename))
    writing = []
    first, second, third, fourth ,five= write_all_head_line()

    writing.append(first + '\n')
    writing.append(second + '\n')
    writing.append(third + '\n')
    writing.append(fourth + '\n')
    writing.append(five + '\n')
    PathEne,ENum = grep_DFT_XSF_energy(gogalpath)
    StrucNum,FileName,AtomNum,CohesiveEne,TotEne,Force,MaxForce,MaxForceNum,RmsForce,StrucNum_filename =grep_predict_energy(predictpath)
    for i in range(len(StrucNum)):
        filepath= FileName[i]
        DFT_ene = PathEne[filepath]
        DFT_AtomNum = ENum[DFT_ene]
        if int(DFT_AtomNum) == int(AtomNum[i]):
            information1 =StringCenter(StrucNum[i],5) + StringCenter(StrucNum_filename[i],9) + XA + StringCenter(AtomNum[i],5) + XA + StringCenter(DFT_ene,16) + XA + StringCenter(CohesiveEne[i],16)+ XA
            information2 =StringCenter(Force[i],38) + XA + StringCenter(MaxForce[i],39) + XA + StringCenter(MaxForceNum[i],5) + XA + StringCenter(RmsForce[i],10) + XA
            information3 = StringCenter(FileName[i],60) + XA
            information = information1+information2+information3
            writing.append(information + '\n')
        else:
            print("Wrong: The scripy is breakdown")
            exit()
    for m in range(len(writing)):
        open(__path,'a').write(writing[m])
def write_ene_info(path, gogalpath, predictpath):
    filename = 'predict.enenrgy'
    __path = os.path.join(path, filename)
    if os.path.exists(__path):
        os.remove(__path)
        print('The {0} file is exist. Removed!'.format(filename))
    writing = []
    first, second,third,fourth= write_ene_head_line()
    writing.append(first+'\n')
    writing.append(second+'\n')
    writing.append(third + '\n')
    writing.append(fourth + '\n')
    PathEne, ENum = grep_DFT_XSF_energy(gogalpath)
    StrucNum, FileName, AtomNum, CohesiveEne, TotEne, Force, MaxForce, MaxForceNum, RmsForce,StrucNum_filename = grep_predict_energy(
        predictpath)
    for i in range(len(StrucNum)):
        filepath = FileName[i]
        DFT_ene = PathEne[filepath]
        DFT_AtomNum = ENum[DFT_ene]
        if int(DFT_AtomNum) == int(AtomNum[i]):
            information =StringCenter(StrucNum[i],5) +StringCenter(StrucNum_filename[i],9) +XA + StringCenter(AtomNum[i],5) + XA + StringCenter(DFT_ene,16) + XA + StringCenter(CohesiveEne[i],16)+ XA
            writing.append(information+'\n')
        else:
            print("Wrong: The scripy is breakdown")
            exit()
    for m in range(len(writing)):
        open(__path, 'a').write(writing[m])


def write_ene(path, gogalpath, predictpath):
    filename = 'predict.enenrgy'
    __path = os.path.join(path, filename)
    if os.path.exists(__path):
        os.remove(__path)
        print('The {0} file is exist. Removed!'.format(filename))
    writing = []
    PathEne, ENum = grep_DFT_XSF_energy(gogalpath)
    StrucNum, FileName, AtomNum, CohesiveEne, TotEne, Force, MaxForce, MaxForceNum, RmsForce, StrucNum_filename = grep_predict_energy(
        predictpath)
    for i in range(len(StrucNum)):
        filepath = FileName[i]
        DFT_ene = PathEne[filepath]
        DFT_AtomNum = ENum[DFT_ene]
        if int(DFT_AtomNum) == int(AtomNum[i]):
            information = StringCenter(AtomNum[i], 5) + '   ' + StringCenter(DFT_ene, 16) + '   ' + StringCenter(CohesiveEne[i], 16)
            writing.append(information + '\n')
        else:
            print("Wrong: The scripy is breakdown")
            exit()
    for m in range(len(writing)):
        open(__path, 'a').write(writing[m])

def write_force_info(path, gogalpath, predictpath):
    filename = 'predict.force'
    __path = os.path.join(path, filename)
    if os.path.exists(__path):
        os.remove(__path)
        print('The {0} file is exist. Removed!'.format(filename))
    writing = []
    first, second, third ,fourth= write_force_head_line()
    writing.append(first + '\n')
    writing.append(second + '\n')
    writing.append(third + '\n')
    writing.append(fourth+'\n')
    PathEne, ENum = grep_DFT_XSF_energy(gogalpath)
    StrucNum, FileName, AtomNum, CohesiveEne, TotEne, Force, MaxForce, MaxForceNum, RmsForce,StrucNum_filename = grep_predict_energy(
        predictpath)
    for i in range(len(StrucNum)):
        filepath = FileName[i]
        DFT_ene = PathEne[filepath]
        DFT_AtomNum = ENum[DFT_ene]
        if int(DFT_AtomNum) == int(AtomNum[i]):
            information = StringCenter(StrucNum[i],5) +StringCenter(StrucNum_filename[i],9)+ XA + StringCenter(AtomNum[i],5) + XA+ StringCenter(Force[i],38) + XA + StringCenter(MaxForce[i],39) + XA + StringCenter(MaxForceNum[i],5) + XA + StringCenter(RmsForce[i],10) + XA
            writing.append(information + '\n')
        else:
            print("Wrong: The scripy is breakdown")
            exit()
    for m in range(len(writing)):
        open(__path, 'a').write(writing[m])
'''
以下函数为内部函数，不允许修改，不允许调用，否则会breakdown.
'''
def write_all_head_line():
    a = StringCenter('No.', 14)
    b = StringCenter('Atoms', 5)
    b2 = StringCenter('Energy',33)
    b3 = StringCenter('Force(eV/Angstrom)',95)
    c = StringCenter('DFT(eV)', 16)
    d = StringCenter('ANN(eV)', 16)
    e = StringCenter('Mean Absolute Foce', 38)
    f = StringCenter('Max Force', 39)
    g = StringCenter('MFNo.', 5)
    h = StringCenter(' RMS Force', 10)
    i = StringCenter('File Path',60)

    num1 = 211
    first_line = "All predict information {0}".format(time.strftime("%Y-%m-%d %H:%M:%S")).center(num1, ' ') +XA
    second_line = '-'*(num1+1)
    third_line = StringCenter(' ',20) + XA+ b2 + XA  + b3 + XA +StringCenter(' ',60)+ XA# 203
    fourth_line1 = a + XA + b + XA + c +XA +d + XA
    fourth_line2 = e +XA+f+XA+g+XA + h+XA
    fourth_line3 = i + XA
    fourth_line = fourth_line1 + fourth_line2 + fourth_line3
    fiveth_line = second_line

    return first_line,second_line,third_line,fourth_line,fiveth_line
def write_ene_head_line():
    a = StringCenter('No.',14)
    b = StringCenter('Atoms',5)
    c = StringCenter('DFT(eV)',16)
    d = StringCenter('ANN(eV)',16)   #cohensive energy
    number = 54
    first_line = "Predict energy {0}".format(time.strftime("%Y-%m-%d %H:%M:%S")).center(number, ' ')+XA
    secondline = "-"*(number+1)
    thirdline = a + XA + b + XA + c +XA + d+XA
    fourthline = secondline
    return first_line,secondline,thirdline,fourthline
def write_force_head_line():
    a = StringCenter('No.',14)
    b = StringCenter('Atoms',5)
    c = StringCenter('Mean Absolute Foce',38)
    d = StringCenter('Max Force',39)   #cohensive energy
    e = StringCenter('MFNo.',5)
    f = StringCenter(' RMS Force',10)
    number = 116
    first_line = "Predict Force Unit: eV/Angstrom {0}".format(time.strftime("%Y-%m-%d %H:%M:%S")).center(116, ' ')+XA
    secondline = "-"*(number+1)
    thirdline = a + XA + b + XA + c +XA + d+XA+ e+XA+ f+XA
    fourthline = secondline
    return first_line,secondline,thirdline,fourthline
def appen_value_to_list(value,list_num):
    if len(value) > 0:
        list_num.append(value)
def contrast_len(keystar_sentence,keyend_sentence,content):
    valus = re.findall(r'{0}(.*){1}'.format(keystar_sentence,keyend_sentence), content)
    if len(valus)>0:
        valus = valus[0].replace(':', '').strip()
        return str(valus)
    else:
        return ''
def StringCenter(content,width=20):
    return content.center(width, ' ')
XA = "|"

#主函数
def RunMain(gogalpath):
    start = time.time()
    readme()
    path,_sPath,_predictPath = get_path(gogalpath)
    _configurePath = find_structure_path(_sPath)[2]
    write_ene_info(path,_configurePath,_predictPath)
    write_ene(path, _configurePath, _predictPath)
    write_all_info(path,_configurePath,_predictPath)
    write_force_info(path,_configurePath,_predictPath)
    alltime = time.time() - start
    tail(alltime)

if __name__ == '__main__':
    gogalpath = 'Your path'
    RunMain(gogalpath)
