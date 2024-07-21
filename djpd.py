#!/usr/bin/python
# -*- coding:utf-8 -*-
#SchoolAssist  Copyright (C) 2024  gohj99
#南宁中考全自动择校工具 等级比较模块

# 等级列表
dj_list = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'E']

#等级比较
#需要提供s1和s2
#s1等级高或等于于s2，返回True
#s1等级低于s2，返回False
def djbj(s1_ys, s2_ys):
    s1 = s1_ys
    s2 = s2_ys
    #检测总分
    s1_zf = s1[:s1.find('（')]
    s1 = s1[s1.find('（') + 1 :]
    s2_zf = s2[:s2.find('（')]
    s2 = s2[s2.find('（') + 1 :]
    if dj_list.index(s1_zf) != dj_list.index(s2_zf):
        if dj_list.index(s1_zf) < dj_list.index(s2_zf):return True
        return False
    #总分相等，便利检测等级
    for dj in dj_list:
        #检测s1等级
        temp1 = s1.find(dj)
        if temp1 != -1:
            s1_qtdj = s1[temp1 - 1:temp1]
            s1 = s1[temp1 + 1 :]
            try:s1_qtdj = int(s1_qtdj)
            except Exception as e:s1_qtdj = 1
        else:s1_qtdj = 0
        #检测s2等级
        temp2 = s2.find(dj)
        if temp2 != -1:
            s2_qtdj = s2[temp2 - 1:temp2]
            s2 = s2[temp2 + 1 :]
            try:s2_qtdj = int(s2_qtdj)
            except Exception as e:s2_qtdj = 1
        else:s2_qtdj = 0
        #对比s1、s2等级
        if s1_qtdj != s2_qtdj:
            if s1_qtdj > s2_qtdj:return True
            return False
    return True

#等级识别
def main(s1):
    #检测总分
    s1_zf = s1[:s1.find('（')]
    s1 = s1[s1.find('（') + 1 :]
    print('你的总分等级：' + s1_zf)
    #print(s1)
    #检测A+个数
    temp = s1.find('A+')
    if temp != -1:
        s1_AA = s1[temp - 1:temp]
        s1 = s1[temp + 2 :]
        try:s1_AA = int(s1_AA)
        except Exception as e:s1_AA = 1
    else:s1_AA = 0
    print('你的A+个数：' + str(s1_AA))
    
    #检测A个数
    temp = s1.find('A')
    if temp != -1:
        s1_A = s1[temp - 1:temp]
        s1 = s1[temp + 1 :]
        try:s1_A = int(s1_A)
        except Exception as e:s1_A = 1
    else:s1_A = 0
    print('你的A个数：' + str(s1_A))
    
    #检测B+个数
    temp = s1.find('B+')
    if temp != -1:
        s1_BB = s1[temp - 1:temp]
        s1 = s1[temp + 2 :]
        try:s1_BB = int(s1_BB)
        except Exception as e:s1_BB = 1
    else:s1_BB = 0
    print('你的B+个数：' + str(s1_BB))
    
    #检测B个数
    temp = s1.find('B')
    if temp != -1:
        s1_B = s1[temp - 1:temp]
        s1 = s1[temp + 1 :]
        try:s1_B = int(s1_B)
        except Exception as e:s1_B = 1
    else:s1_B = 0
    print('你的B个数：' + str(s1_B))
    
    #检测C+个数
    temp = s1.find('C+')
    if temp != -1:
        s1_CC = s1[temp - 1:temp]
        s1 = s1[temp + 2 :]
        try:s1_CC = int(s1_CC)
        except Exception as e:s1_CC = 1
    else:s1_CC = 0
    print('你的C+个数：' + str(s1_CC))
    
    #检测C个数
    temp = s1.find('C')
    if temp != -1:
        s1_C = s1[temp - 1:temp]
        s1 = s1[temp + 1 :]
        try:s1_C = int(s1_C)
        except Exception as e:s1_C = 1
    else:s1_C = 0
    print('你的C个数：' + str(s1_C))

    #检测D个数
    temp = s1.find('D')
    if temp != -1:
        s1_D = s1[temp - 1:temp]
        s1 = s1[temp + 1 :]
        try:s1_D = int(s1_D)
        except Exception as e:s1_D = 1
    else:s1_D = 0
    print('你的D个数：' + str(s1_D))

    #检测E个数
    temp = s1.find('E')
    if temp != -1:
        s1_E = s1[temp - 1:temp]
        s1 = s1[temp + 1 :]
        try:s1_E = int(s1_E)
        except Exception as e:s1_E = 1
    else:s1_E = 0
    print('你的E个数：' + str(s1_E))

#等级检测
def djjc(s1_ys, s2_ys):
    s1 = s1_ys
    s2 = s2_ys
    #检测总分
    s1_zf = s1[:s1.find('（')]
    s1 = s1[s1.find('（') + 1 :]
    s2_zf = s2[:s2.find('（')]
    s2 = s2[s2.find('（') + 1 :]
    if dj_list.index(s1_zf) != dj_list.index(s2_zf):
        if dj_list.index(s1_zf) < dj_list.index(s2_zf):return s1_ys
        return s2_ys
    #总分相等，便利检测等级
    for dj in dj_list:
        #检测s1等级
        temp1 = s1.find(dj)
        if temp1 != -1:
            s1_qtdj = s1[temp1 - 1:temp1]
            s1 = s1[temp1 + 1 :]
            try:s1_qtdj = int(s1_qtdj)
            except Exception as e:s1_qtdj = 1
        else:s1_qtdj = 0
        #检测s2等级
        temp2 = s2.find(dj)
        if temp2 != -1:
            s2_qtdj = s2[temp2 - 1:temp2]
            s2 = s2[temp2 + 1 :]
            try:s2_qtdj = int(s2_qtdj)
            except Exception as e:s2_qtdj = 1
        else:s2_qtdj = 0
        #对比s1、s2等级
        if s1_qtdj != s2_qtdj:
            if s1_qtdj > s2_qtdj:return s1_ys
            return s2_ys
    return s1_ys

if __name__ == "__main__":
    main('A+（A+AB+BC+C）')
    print(djbj('A（1A+2A1B+1B1C+）', 'A（2A+1A1B+1B1C+）'))
