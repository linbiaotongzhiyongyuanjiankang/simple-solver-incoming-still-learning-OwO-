from numpy import *
from math import *
import sys, os, sympy, codecs
from tkinter import *
import tkinter as tk
from tkinter import filedialog as fdlog

root = tk.Tk()
root.withdraw()

def infile():
    global inpad
    path = fdlog.askopenfilename()
    try:
        infile = codecs.open(path, 'r', encoding='utf-8')
        inpad = infile
    except:
        print('文件编码应为utf-8，请更改编码。\n')

    indata = inpad.readlines()
    time = 0
    line = indata[time].strip('\r\n')
    temps = line.split(' ', line.count(' '))
    num = int(temps[0])
    point = int(temps[1])

    m = list(range(num))
    mm = zeros((point * 2, point * 2))
    uv = zeros(point * 2)
    forces = [0] * (point * 2)
    angle = zeros(num)
    length = zeros(num)
    num1 = zeros(num)
    num2 = zeros(num)

    time = time + 1

    for i in range(num):
        line = indata[time].strip('\r\n')
        temps = line.split(' ', line.count(' '))
        angle[i] = float(temps[2])
        length[i] = eval(temps[3])
        num1[i] = int(temps[0])
        num2[i] = int(temps[1])
        m[i] = mat(angle[i], length[i])
        # print(m[i],end='\n')#输出刚度矩阵
        m[i] = rebig(m[i], num1[i], num2[i], point)
        # print(m[i],end='\n')#输出扩阶后的刚度矩阵
        time = time + 1

    for i in range(num):
        mm = mm + m[i]
    # print(mm,end='\n')#输出总刚度矩阵
    for i in range(point):
        line = indata[time].strip('\r\n')
        temps = line.split(' ', line.count(' '))

        uv[i * 2] = float(temps[0])
        uv[i * 2 + 1] = float(temps[1])
        forces[i * 2] = for_num(temps[2])
        forces[i * 2 + 1] = for_num(temps[3])
        time = time + 1
    inpad.close()
    location = get_location_in_list(uv.tolist(), 0)
    mms = delete(mm, [location], axis=1)
    mms = delete(mms, [location], axis=0)
    if linalg.det(mms) < 0.00000000001:
        print('输入数据出错', end='\n')
        os._exit(0)
    forces_delete = delete(forces, [location], axis=0)

    uv = add_add(point, uv, ((mms.I).dot(forces_delete.T)).T, location)
    bar_force(angle, uv, length, num1, num2, num)
    uv = matrix(uv)
    forces = (mm.dot(uv.T))

    with open('计算结果.txt', 'a') as f:
        f.write('各结点力为：\n')
        for i in range(point):
            f.write('结点%d力：' % (i + 1))
            f.write(str(forces[2 * i, 0]))
            f.write('  ,  ')
            f.write(str(forces[2 * i + 1, 0]))
            f.write('\n')
        f.write('\n各结点位移为：\n')
        for i in range(point):
            f.write('结点%d位移：L/EA(' % (i + 1))
            f.write(str(uv[0, 2 * i], ))
            f.write('  ,  ')
            f.write(str(uv[0, 2 * i + 1]))
            f.write(')\n')
        f.close()
    # for i in range(point):
    # print('结点%d力：'%(i+1),forces[2*i,0],',',forces[2*i+1,0],end='\n')
    # for i in range(point):
    # print('结点%d位移：L/EA('%(i+1),uv[0,2*i],',',uv[0,2*i+1],end=')\n')

    print('计算完成，结果保存在"计算结果.txt"\n')
