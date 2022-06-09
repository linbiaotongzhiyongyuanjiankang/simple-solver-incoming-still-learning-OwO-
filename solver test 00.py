import numpy as np
import torch as torch
import pandas as pd
import sys
import os
import sympy
import codecs

'''for i in element'''

E = 1000000
A = 6400
length = 1000
Idle = 128000
lngto = 1 / length

dln = E * A / length
dthe = 12 * E * Idle / length ** 3
dtht = 4 * E * Idle / length
dtho = 6 * E * Idle / length ** 2
dtha = 2 * E * Idle / length

iEK = torch.tensor([[dln, 0, 0, -dln, 0, 0],  # 定义单元刚度矩阵
                    [0, dthe, dtho, 0, -dthe, dtho],
                    [0, dtho, dtht, 0, -dtho, dtha],
                    [-dln, 0, 0, dln, 0, 0],
                    [0, -dthe, -dtho, 0, dthe, -dtho],
                    [0, dtho, dtha, 0, -dtho, dtht]])

iEH = torch.tensor([[-1, 0, 0],  # 定义单元平衡矩阵
                    [0, lngto, lngto],
                    [0, 1, 0],
                    [1, 0, 0],
                    [0, -lngto, -lngto],
                    [0, 0, 1]])

iEG = iEH.t()  # 定义单元几何矩阵

iEA = torch.tensor([[dln, 0, 0],  # 单元刚度本构
                    [0, dtht, dtha],
                    [0, dtha, dtht]])

iEB = iEA.t()   # 定义单元柔度矩阵



print(iEK)
