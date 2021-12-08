# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 15:40:46 2021

@author: 1
"""

##### （一）	第二套模型：当第一阶段模型输出结果为基于历史价格定价时

# 开始
from pyomo.environ import *

model = AbstractModel()

###### 集合
model.I = Set()  #中标运输订单i的集合（公路运输转铁路运输的情况）
model.E = Set()  #中标运输订单e的集合（铁路运输转公路运输的情况）
model.J = Set()  #既有运输订单j的集合
model.K = Set()  #既有运输订单j可用车辆k的集合
model.R = Set()  #中标运输订单i和e的备选运行线路r的集合
model.N = Set()  #中标运输订单i和e的集装箱的集合
model.T = Set()  #列车到达时刻表的集合


###### 参数  公路运输转铁路运输
# Cir 选择路线r时，中标运输订单i的单位运输成本
model.Cir = Param(model.I, model.R)
# dir 选择路线r时，中标运输订单i的单位运输距离
model.dir = Param(model.I, model.R)
# vir 选择路线r时，中标运输订单i的单位运输速度
model.vir = Param(model.I, model.R)
# dji 从既有运输订单j的终点到运输订单i的起点的空车行驶距离
model.dji = Param(model.J, model.I)
# tdkj  运输订单j的卡车k到达终点的时刻
model.tdkj = Param(model.K, model.J)
# Nkj 既有运输订单j的车辆数
model.Nkj = Param(model.K, model.J)
# Ni 中标运输订单i的集装箱
model.Ni = Param(model.I)
# bia 中标运输订单i的单位报价
model.bia = Param(model.I)
# dvi 中标运输订单i的平均运输距离
model.dvi = Param(model.I)
# Trni 列车运行时刻表
model.Trni = Param(model.T, model.I)
# clni 铁路端时间窗的下限
model.clni = Param(model.I)
# cuni 铁路端时间窗的上限
model.cuni = Param(model.I)
# cln2kji 下一班次列车出发的铁路端时间窗的下限
model.cln2i = Param(model.I)
# mi 去货主处提货的时间窗下限
model.mi = Param(model.I)
# ni 去货主处提货的时间窗上限
model.ni = Param(model.I)
# tlci 在客户处装货或卸货的时间
model.tlci = Param(model.I)
# tskji 在铁路场站的免费堆存时间
model.tskjir = Param(model.K, model.J, model.I,model.R)
# Qoi 运输订单i所到的铁路场站的其他货物重量
model.Qoi = Param(model.I)
# Qi 运输订单i所到的铁路场站的运能
model.Qi = Param(model.I)
# qi 运输订单i所到的铁路场站的列车运力
model.qi = Param(model.I)

###### 参数  铁路运输转公路运输
# Te 运输订单e的列车到达时刻
model.Te = Param(model.E) 
# Cer 选择路线r时，中标运输订单e的单位运输成本
model.Cer = Param(model.E, model.R)
# der 选择路线r时，中标运输订单e的单位运输距离
model.der = Param(model.E, model.R)
# ver 选择路线r时，中标运输订单e的单位运输速度
model.ver = Param(model.E, model.R)
# dje 从既有运输订单j的终点到运输订单e的起点的空车行驶距离
model.dje = Param(model.J, model.E)
# Ne 中标运输订单e的集装箱
model.Ne = Param(model.E)
# bea 中标运输订单e的单位报价
model.bea = Param(model.E)
# dve 中标运输订单e的平均运输距离
model.dve = Param(model.E)

# pe 去铁路场站处提货的时间窗下限
model.pe = Param(model.E)
# qe 去铁路场站处提货的时间窗上限
model.qe = Param(model.E)
# ae 去货主处提货的时间窗下限
model.ae = Param(model.E)
# be 去货主处提货的时间窗上限
model.be = Param(model.E)
# tlrkje 在客户处装货或卸货的时间
model.tlre = Param(model.E)

#顾客满意度
model.x1 = Param(model.E)
model.x2 = Param(model.E)
model.x3 = Param(model.E)
model.x4 = Param(model.E)

###### 变量  公路运输转铁路运输
# xkjir 卡车K从既有运输订单j的终点运往中标运输订单i的起点且选择线路r运输集装箱
model.xkjir = Var(model.K, model.J, model.I, model.R, domain=Binary)

# tir 选择路线r时，中标运输订单i的单位运输时间
model.tir = Var(model.I, model.R, domain=NonNegativeReals)
# tji 从既有运输订单j的终点到运输订单i的起点的空车行驶时间
model.tji = Var(model.J, model.I, domain=NonNegativeReals)
# mkji 在计算卡车到达货主处的辅助变量
model.mkji = Var(model.K, model.J, model.I, domain=Binary, initialize=0) 
# zi 在计算卡车到达货主处的辅助变量
model.Zi = Var(model.I, domain=NonNegativeReals, initialize=0)

# y1kji 惩罚成本处的辅助变量
model.y1kji = Var(model.K, model.J, model.I, domain=Binary, initialize=0)
# d1kji 仓储成本处的辅助变量
model.d1kjir = Var(model.K, model.J, model.I, model.R, domain=Binary, initialize=0)
# d2kji 仓储成本处的辅助变量
model.d2kjir = Var(model.K, model.J, model.I, model.R, domain=Binary, initialize=0)
# d3kji 仓储成本处的辅助变量
model.d3kjir = Var(model.K, model.J, model.I, model.R, domain=Binary, initialize=0)
# gi 仓储成本处的辅助变量
model.gi = Var(model.K, model.J, model.I, model.R, domain=Binary, initialize=0)

# Dkjir 总储存成本
model.Dkjir = Var(model.K, model.J, model.I, model.R, domain=NonNegativeReals, initialize=0)
model.D2kjir = Var(model.K, model.J, model.I, model.R, domain=NonNegativeReals, initialize=0)
# fkjir 总惩罚成本
model.fkjir = Var(model.K, model.J, model.I, model.R, domain=NonNegativeReals, initialize=0)
# tckji  卡车k到达货主处的时刻 
model.tckji = Var(model.K, model.J, model.I, domain=NonNegativeReals, initialize=0)
# tmkjir  卡车k到达运输订单i的铁路场站的时刻
model.tmkjir = Var(model.K,model.J, model.I, model.R, domain=NonNegativeReals, initialize=0)
# tekji  卡车k到达运输订单i的终点的时刻
model.tekji = Var(model.K, model.J, model.I, domain=NonNegativeReals, initialize=0)

###### 变量  铁路运输转公路运输
# xkjer 卡车K将运输订单e的集装箱从起点运往终点所选择的线路
model.xkjer = Var(model.K, model.J, model.E, model.R, domain=Binary) 
# ter 选择路线r时，中标运输订单e的单位运输时间 
model.ter = Var(model.E, model.R, domain=NonNegativeReals, initialize=0)
# tkje 从既有运输订单j的终点到运输订单e的起点的空车行驶时间   
model.tje = Var(model.J, model.E, domain=NonNegativeReals, initialize=0)

# tmkje  卡车k到达运输订单e的铁路场站的时刻
model.tmkje = Var(model.K, model.J, model.E, domain=NonNegativeReals, initialize=0) 
# mkje 在计算卡车到达铁路场站处的辅助变量
model.mkje = Var(model.K, model.J, model.E, domain=Binary, initialize=0)
# zkje 在计算卡车到达铁路场站处的辅助变量
model.Ze = Var(model.E, domain=NonNegativeReals, initialize=0)
# y1kje 仓储成本处的辅助变量
model.y1kje = Var(model.K, model.J, model.E, domain=Binary, initialize=0)
# y2kjer 货主处惩罚成本处的辅助变量
model.y2kjer = Var(model.K, model.J, model.E, model.R, domain=Binary, initialize=0)
# y3kjer 货主处惩罚成本处的辅助变量
model.y3kjer = Var(model.K, model.J, model.E, model.R, domain=Binary, initialize=0)
# y4kjer 到达货主处的辅助变量
model.y4kjer = Var(model.K, model.J, model.E, model.R, domain=Binary, initialize=0)
# y5kjer 到达货主处的辅助变量
model.y5kjer = Var(model.K, model.J, model.E, model.R, domain=Binary, initialize=0)
# y6kjer 到达货主处的辅助变量
model.y6kjer = Var(model.K, model.J, model.E, model.R, domain=Binary, initialize=0)
# y7kjer 到达货主处的辅助变量
model.y7kjer = Var(model.K, model.J, model.E, model.R, domain=Binary, initialize=0)
model.y8kjer = Var(model.K, model.J, model.E, model.R, domain=Binary, initialize=0) 
#构造连续变量
model.m1kjer = Var(model.K, model.J, model.E, model.R, domain=NonNegativeReals, initialize=0)
model.m2kjer = Var(model.K, model.J, model.E, model.R, domain=NonNegativeReals, initialize=0)
model.m3kjer = Var(model.K, model.J, model.E, model.R, domain=NonNegativeReals, initialize=0)
model.m4kjer = Var(model.K, model.J, model.E, model.R, domain=NonNegativeReals, initialize=0)



# Dkjer 总储存成本
model.Dkjer = Var(model.K, model.J, model.E, model.R, domain=NonNegativeReals, initialize=0)
# fkjer 总惩罚成本
model.fkjer = Var(model.K, model.J, model.E, model.R, domain=NonNegativeReals, initialize=0)
# tckei  卡车k到达运输订单e的铁路场站的时刻
model.tckei = Var(model.K, model.J, model.E, domain=NonNegativeReals, initialize=0)
# tmkjer  卡车k到达运输订单e的铁路场站的时刻
model.tmkjer = Var(model.K, model.J, model.E, model.R, domain=NonNegativeReals, initialize=0)
# tekjer  卡车k到达运输订单e的终点的时刻
model.tekjer = Var(model.K, model.J, model.E, model.R, domain=NonNegativeReals, initialize=0)
# Stekjer 客户满意度
model.Stekjer = Var(model.K, model.J, model.E, model.R, domain=NonNegativeReals, initialize=0)

# C0 承运人的空车定位成本
C0 = 5
# v0 空车行驶速度
v0 = 85
# ts 在铁路场站的免费堆存时间
ts = 1
# st 在铁路场站的单位存储成本
st = 5
# sc 在客户处的单位存储成本
sc = 5
# f 单位惩罚成本
f = 8
# ta 单位时间价值成本
ta = 2

# h 时间满意度的约束值
h = 0.5

# 客户的容忍时间节点
#x1 = 16
#x2 = 17
#x3 = 18
#x4 = 19

# M无限大
LargeNumber = 100000


# 目标函数（求最大值）
def Obj(model):
    return  sum(model.bia[i] * model.dvi[i] * model.Ni[i] for i in model.I) - \
           sum(model.xkjir[k, j, i, r] * model.Cir[i,r]  * model.dir[i,r] for i in model.I for r in model.R for j in model.J for k in model.K) - \
           sum(model.xkjir[k, j, i, r] * model.dji[j,i] * C0 for i in model.I for j in model.J for k in model.K for r in model.R) - \
           sum(model.Dkjir[k,j,i,r] for i in model.I for r in model.R for j in model.J for k in model.K) - sum(model.D2kjir[k,j,i,r] for i in model.I for r in model.R for j in model.J for k in model.K)-sum(model.fkjir[k,j,i,r] for i in model.I for r in model.R for j in model.J for k in model.K) \
           - sum(model.xkjir[k, j, i, r] * ta * (model.ni[i] - model.tdkj[k,j]) for i in model.I for j in model.J for k in model.K for r in model.R) +\
           sum(model.bea[e] * model.dve[e] * model.Ne[e] for e in model.E) - \
           sum(model.xkjer[k, j, e, r] * model.Cer[e,r]  * model.der[e, r] for e in model.E for r in model.R for j in model.J for k in model.K) - \
           sum(model.xkjer[k, j, e, r] * model.dje[j,e] * C0 for e in model.E for j in model.J for k in model.K for r in model.R) - \
           sum(model.Dkjer[k, j, e, r] for e in model.E for r in model.R for j in model.J for k in model.K) -  sum(model.fkjer[k, j, e, r] for e in model.E for r in model.R for j in model.J for k in model.K ) \
           - sum(model.xkjer[k, j, e, r] * ta * (model.qe[e] - model.tdkj[k,j]) for e in model.E for j in model.J for k in model.K for r in model.R)


model.Obj = Objective(rule=Obj, sense=maximize) 

# 约束，每个a后面的数字对应模型文本中的约束编号
########公路运输转铁路运输的情况 
## 路途运输时间    改
def a24(model, i, r):
    return model.tir[i, r] == model.dir[i, r] / model.vir[i, r] 
model.a24 = Constraint(model.I, model.R, rule=a24)

## 空车定位时间    改 
def a25(model, j, i):
    return model.tji[j, i] == model.dji[j, i] / v0 
model.a25 = Constraint(model.J, model.I, rule=a25) 

# 车辆调配数=集装箱数量，所有车辆只能服务一个运输订单且只能利用一次
def a26(model, k, j, i, r):  
    return  sum(model.xkjir[k, j, i, r] for k in model.K for j in model.J for r in model.R) == model.Ni[i]
model.a26 = Constraint(model.K, model.J, model.I, model.R, rule=a26)
def a27(model, k, j, i, r, e):  
    return  sum(model.xkjir[k, j, i, r] for i in model.I for r in model.R) + sum(model.xkjer[k, j, e, r] for e in model.E for r in model.R) <= 1
model.a27 = Constraint(model.K, model.J, model.I, model.R, model.E,rule=a27)

# 既有运输订单j的卡车到达中标运输订单i的货主处的时刻为：该卡车完成上一批运输订单的时刻 + 空车定位时间 
# todo 部分xkjir为0时tckji不为0，导致后续计算出错

def a28(model, k, j, i, r): 
    return LargeNumber * (1 - model.xkjir[k, j, i, r]) + model.tdkj[k,j] + model.tji[j, i] >= model.tckji[k, j, i]
model.a28 = Constraint(model.K, model.J, model.I, model.R, rule=a28)
def a28_1(model, k, j, i, r):
    return model.tdkj[k,j] + model.tji[j, i] <= model.tckji[k, j, i] + LargeNumber * (1 - model.xkjir[k, j, i, r])
model.a28_1 = Constraint(model.K, model.J, model.I, model.R, rule=a28_1)


#当从两个及以上地方调配卡车时，找到卡车到达货主处的最晚时间为： 一个订单对应一个最晚时刻！改！！！
# todo 可能需要加上xkjir的约束？
def a29_1(model, k, j, i,r): 
    return  model.Zi[i] >= model.tckji[k, j, i] 
model.a29_1 = Constraint(model.K, model.J, model.I, model.R, rule=a29_1)

def a29_2(model, k, j, i,r): 
    return  model.tckji[k, j, i] >= model.Zi[i] - LargeNumber *  (1 - model.mkji[k,j,i]) 
model.a29_2 = Constraint(model.K, model.J, model.I, model.R, rule=a29_2)

def a29_3(model, k, j, i): 
    return  sum(model.mkji[k, j,i] for k in model.K for j in model.J) == 1    
model.a29_3 = Constraint(model.K, model.J, model.I, rule=a29_3) 


#惩罚成本  维度问题 
def a30_1(model, k, j, i):
    return model.Zi[i] <= model.ni[i] + LargeNumber * model.y1kji[k, j, i]
model.a30_1 = Constraint(model.K, model.J, model.I, rule=a30_1)

def a30_2(model, k, j, i, r):
    return - model.y1kji[k, j, i] * LargeNumber <= model.fkjir[k, j, i, r] 
model.a30_2 = Constraint(model.K, model.J, model.I, model.R, rule=a30_2)

def a30_3(model, k, j, i, r):
    return model.fkjir[k, j, i, r] <= model.y1kji[k, j, i] * LargeNumber 
model.a30_3 = Constraint(model.K, model.J, model.I, model.R, rule=a30_3)

def a30_4(model, k, j, i, r):
    return - model.xkjir[k, j, i, r] * LargeNumber <= model.fkjir[k, j, i, r]  
model.a30_4 = Constraint(model.K, model.J, model.I, model.R, rule=a30_4)

def a30_5(model, k, j, i, r):
    return model.fkjir[k, j, i, r] <= model.xkjir[k, j, i, r] * LargeNumber
model.a30_5 = Constraint(model.K, model.J, model.I, model.R, rule=a30_5)

def a30_6(model, k, j, i, r):
    return LargeNumber * (1 - model.y1kji[k, j, i]) + model.Zi[i] >= model.ni[i]
model.a30_6 = Constraint(model.K, model.J, model.I, model.R, rule=a30_6)

def a30_7(model,k, j, i, r):
    return - LargeNumber * (2 - model.y1kji[k, j, i] - model.xkjir[k, j, i, r]) <= model.fkjir[k, j, i, r] - (model.Zi[i] - model.ni[i]) * f
model.a30_7 = Constraint(model.K, model.J, model.I, model.R, rule=a30_7)

def a30_8(model, k, j, i, r):
    return model.fkjir[k, j, i, r] - (model.Zi[i] - model.ni[i]) * f <= LargeNumber * (2 - model.y1kji[k, j, i] - model.xkjir[k, j, i, r])
model.a30_8 = Constraint(model.K, model.J, model.I, model.R, rule=a30_8)

## 卡车到达铁路场站的时刻为：卡车到达货主处的最晚时刻 + 货物装车时间 + 运输时间     
def a32_1(model, k, j, i, r):   
    return  model.tmkjir[k,j,i, r] == model.Zi[i] + model.tlci[i] + model.tir[i, r]
model.a32_1 = Constraint(model.K, model.J, model.I, model.R, rule=a32_1)

# 卡车到达铁路场站的每一个集装箱的仓储成本   # 构造0-1变量和大M 
def a33_1(model, k, j, i, r):
    return  model.tmkjir[k,j,i, r] <= model.clni[i] - ts + LargeNumber * (1-model.d1kjir[k,j, i, r])
model.a33_1 = Constraint(model.K, model.J, model.I, model.R, rule=a33_1)

def a33_11(model, k, j, i, r):
    return - model.xkjir[k, j, i, r] * LargeNumber <= model.Dkjir[k, j, i, r]   
model.a33_11 = Constraint(model.K, model.J, model.I, model.R, rule=a33_11)
def a33_12(model, k, j, i, r):
    return model.Dkjir[k, j, i, r] <= model.xkjir[k, j, i, r] * LargeNumber
model.a33_12 = Constraint(model.K, model.J, model.I, model.R, rule=a33_12)
def a33_13(model, k, j, i, r):
    return - LargeNumber * (2- model.xkjir[k, j, i, r]-model.d1kjir[k,j, i, r]) <= model.Dkjir[k,j,i,r] - (model.clni[i] - model.tmkjir[k,j,i, r] - ts) * st 
model.a33_13 = Constraint(model.K, model.J, model.I, model.R, rule=a33_13)

def a33_14(model, k, j, i, r):
    return model.Dkjir[k,j,i,r] - (model.clni[i] - model.tmkjir[k,j,i, r] - ts) * st   <= LargeNumber *  (2- model.xkjir[k, j, i, r]-model.d1kjir[k,j, i, r])
model.a33_14 = Constraint(model.K, model.J, model.I, model.R, rule=a33_14)


def a33_2(model, k, j, i, r):
    return  model.clni[i] - ts - LargeNumber * model.d1kjir[k,j, i, r] <= model.tmkjir[k,j,i, r]
model.a33_2 = Constraint(model.K, model.J, model.I, model.R, rule=a33_2)

def a33_21(model, k, j, i, r):
    return  model.tmkjir[k,j,i, r] <= model.cuni[i] + LargeNumber * model.d1kjir[k,j, i, r]
model.a33_21 = Constraint(model.K, model.J, model.I, model.R, rule=a33_21)

def a33_22(model, k, j, i, r):
    return - LargeNumber * model.d1kjir[k,j, i, r] <= model.Dkjir[k,j,i,r]
model.a33_22 = Constraint(model.K, model.J, model.I, model.R, rule=a33_22)

def a33_23(model, k, j, i, r):
    return model.Dkjir[k, j,i,r] <= LargeNumber * model.d1kjir[k,j, i, r]
model.a33_23 = Constraint(model.K, model.J, model.I, model.R, rule=a33_23)


def a33_3(model, k, j, i, r ):
    return  model.cuni[i] - LargeNumber * ( 1 - model.d2kjir[k,j, i, r]) <= model.tmkjir[k,j,i, r]
model.a33_3 = Constraint(model.K, model.J, model.I, model.R, rule=a33_3)

def a33_31(model, k, j, i, r):
    return  model.tmkjir[k,j,i, r] <= model.cln2i[i] - ts + LargeNumber * ( 1 - model.d2kjir[k,j, i, r])
model.a33_31 = Constraint(model.K, model.J, model.I, model.R, rule=a33_31)
def a33_34(model, k, j, i, r):
    return - model.xkjir[k, j, i, r] * LargeNumber <= model.Dkjir[k, j, i, r]  
model.a33_34 = Constraint(model.K, model.J, model.I, model.R, rule=a33_34)

def a33_35(model, k, j, i, r):
    return model.Dkjir[k, j, i, r] <= model.xkjir[k, j, i, r] * LargeNumber
model.a33_35 = Constraint(model.K, model.J, model.I, model.R, rule=a33_35)
def a33_36(model, k, j, i, r):
    return - LargeNumber * (2-model.xkjir[k, j, i, r] - model.d2kjir[k,j, i, r]) <= model.Dkjir[k,j,i,r] - (model.cln2i[i] - model.tmkjir[k,j,i, r] - ts) * st 
model.a33_36 = Constraint(model.K, model.J, model.I, model.R, rule=a33_36)

def a33_37(model, k, j, i, r):
    return model.Dkjir[k,j,i,r] - (model.cln2i[i] - model.tmkjir[k,j,i, r] - ts) * st  <= LargeNumber * (2 - model.xkjir[k, j, i, r]  - model.d2kjir[k,j, i, r] )
model.a33_37 = Constraint(model.K, model.J, model.I, model.R, rule=a33_37)


#货物的容量不能超过可用列车车厢的容量（满足铁路运力要求） 
def a34_1(model, k, j, i, r):
    return model.qi[i] * model.Ni[i] + model.Qoi[i] <= model.Qi[i] + LargeNumber * model.gi[k,j,i,r] 
model.a34_1 = Constraint(model.K, model.J, model.I, model.R, rule=a34_1)

def a34_2(model, k, j, i, r):
    return - model.gi[k,j,i,r] * LargeNumber <= model.D2kjir[k,j,i,r]  
model.a34_2 = Constraint(model.K, model.J, model.I, model.R, rule=a34_2)

def a34_3(model, k, j, i, r):
    return model.D2kjir[k,j,i,r] <= model.gi[k,j,i,r] * LargeNumber 
model.a34_3 = Constraint(model.K, model.J, model.I, model.R, rule=a34_3)

def a34_6(model, k, j, i, r):
    return LargeNumber * (1 - model.gi[k,j,i,r]) + model.qi[i] * model.Ni[i] + model.Qoi[i] >= model.Qi[i]
model.a34_6 = Constraint(model.K, model.J, model.I, model.R, rule=a34_6)

def a34_4(model, k, j, i, r):
    return - model.xkjir[k, j, i, r] * LargeNumber <= model.D2kjir[k, j, i, r]
model.a34_4 = Constraint(model.K, model.J, model.I, model.R, rule=a34_4)

def a34_5(model, k, j, i, r ):
    return model.D2kjir[k, j, i, r] <= model.xkjir[k, j, i, r] * LargeNumber
model.a34_5 = Constraint(model.K, model.J, model.I, model.R, rule=a34_5)
def a34_7(model,k, j, i, r):
    return - LargeNumber * (2 - model.gi[k,j,i,r]-model.xkjir[k, j, i, r]) <= model.D2kjir[k,j,i,r] - (model.cln2i[i] - model.tmkjir[k,j, i, r] - ts) * st 
model.a34_7 = Constraint(model.K, model.J, model.I, model.R, rule=a34_7)

def a34_8(model, k, j, i, r):
    return model.D2kjir[k,j,i,r] - (model.cln2i[i] - model.tmkjir[k,j, i, r] - ts) * st  <= LargeNumber * (2 - model.gi[k,j,i,r]-model.xkjir[k, j, i, r])
model.a34_8 = Constraint(model.K, model.J, model.I, model.R, rule=a34_8)

 

############铁路运输转公路运输的情况
## 路途运输时间   改
def a35(model, e, r):
    return model.ter[e, r] == model.der[e, r] / model.ver[e, r] 
model.a35 = Constraint(model.E, model.R, rule=a35)

## 空车定位时间   改
def a36(model,j, e):
    return model.tje[j, e] == model.dje[j, e] / v0 
model.a36 = Constraint(model.J, model.E, rule=a36)

# 车辆调配数=集装箱数量   
def a37(model, k, j, e, r):  
    return  sum(model.xkjer[k, j, e, r] for k in model.K for j in model.J for r in model.R) == model.Ne[e] 
model.a37 = Constraint(model.K, model.J, model.E, model.R, rule=a37)

# 既有运输订单j的卡车到达中标运输订单e的货主处的时刻为：该卡车完成上一批运输订单的时刻 + 空车定位时间   
def a38(model, k, j, e, r):
    return LargeNumber * (1 - model.xkjer[k, j, e, r]) + model.tdkj[k,j] + model.tje[j, e] >= model.tmkje[k, j, e]
model.a38 = Constraint(model.K, model.J, model.E, model.R, rule=a38)
def a38_1(model, k, j, e, r):
    return model.tdkj[k,j] + model.tje[j, e] <= model.tmkje[k, j, e] + LargeNumber * (1 - model.xkjer[k, j, e, r])
model.a38_1 = Constraint(model.K, model.J, model.E, model.R, rule=a38_1)

#当从两个及以上地方调配卡车时，找到卡车到达铁路场站处的最晚时间为：  一个运输订单对应一个最晚时间 
def a39_1(model, k, j, e): 
    return  model.Ze[e] >= model.tmkje[k, j, e]
model.a39_1 = Constraint(model.K, model.J, model.E, rule=a39_1)

def a39_2(model, k, j, e): 
    return  model.tmkje[k,j, e] >= model.Ze[e] - LargeNumber *  (1 - model.mkje[k, j, e]) 
model.a39_2 = Constraint(model.K, model.J, model.E, rule=a39_2)

def a39_3(model, k, j, e): 
    return  sum(model.mkje[k, j, e] for k in model.K for j in model.J) == 1    
model.a39_3 = Constraint(model.K, model.J, model.E, rule=a39_3) 


# 到处铁路场站处的仓储成本
def a40_1(model, k, j, e):
    return model.Ze[e] <= model.qe[e] + LargeNumber * model.y1kje[k,j, e]
model.a40_1 = Constraint(model.K, model.J, model.E, rule=a40_1)

def a40_2(model, k, j, e, r):
    return - model.y1kje[k,j, e] * LargeNumber <= model.Dkjer[k, j, e, r] 
model.a40_2 = Constraint(model.K, model.J, model.E, model.R, rule=a40_2)

def a40_3(model, k, j, e, r):
    return model.Dkjer[k, j, e, r] <= model.y1kje[k,j, e] * LargeNumber 
model.a40_3 = Constraint(model.K, model.J, model.E, model.R, rule=a40_3)

def a40_6(model, k, j, e, r):
    return LargeNumber * (1 - model.y1kje[k,j, e]) + model.Ze[e] >= model.qe[e] + ts
model.a40_6 = Constraint(model.K, model.J, model.E, model.R, rule=a40_6)
def a40_4(model, k, j, e, r):
    return - model.xkjer[k, j, e, r] * LargeNumber <= model.Dkjer[k, j, e, r]  
model.a40_4 = Constraint(model.K, model.J, model.E, model.R, rule=a40_4)

def a40_5(model, k, j, e, r):
    return model.Dkjer[k, j, e, r] <= model.xkjer[k, j, e, r] * LargeNumber
model.a40_5 = Constraint(model.K, model.J, model.E, model.R, rule=a40_5)
def a40_7(model,k, j, e, r):
    return - LargeNumber * (2 - model.y1kje[k,j, e] - model.xkjer[k, j, e, r]) <= model.Dkjer[k, j, e, r] - ( model.Ze[e] -model.qe[e] - ts) * st
model.a40_7 = Constraint(model.K, model.J, model.E, model.R, rule=a40_7)

def a40_8(model, k, j, e, r):
    return model.Dkjer[k, j, e, r] - ( model.Ze[e] -model.qe[e] - ts) * st <= LargeNumber * (2 - model.y1kje[k,j, e] - model.xkjir[k, j, e, r])
model.a40_8 = Constraint(model.K, model.J, model.E, model.R, rule=a40_8) 


## 卡车到达货主处的时刻为：
#当卡车早于时间窗到达时，中标运输订单e的卡车到达货主处的时刻为：列车到达的时刻 + 货物装车时间 + 运输时间；
#当卡车晚于时间窗到达时，中标运输订单e的卡车到达货主处的时刻为：卡车到达铁路场站处的时刻 + 货物装车时间 + 运输时间。

def a41_1(model, k, j, e, r):
    return model.Ze[e] <= model.Te[e] + LargeNumber * model.y4kjer[k, j, e, r]
model.a41_1 = Constraint(model.K, model.J, model.E, model.R, rule=a41_1)

def a41_2(model, k, j, e, r):
    return - model.xkjer[k, j, e, r] * LargeNumber <= model.tekjer[k, j, e, r] 
model.a41_2 = Constraint(model.K, model.J, model.E, model.R, rule=a41_2)
def a41_3(model, k, j, e, r):
    return model.tekjer[k, j, e, r] <= model.xkjer[k, j, e, r] * LargeNumber 
model.a41_3 = Constraint(model.K, model.J, model.E, model.R, rule=a41_3)

def a41_4(model, k, j, e, r):
    return - LargeNumber * model.y4kjer[k, j, e, r]  <= model.tekjer[k, j, e, r] - model.Te[e] - model.tlre[e] - model.ter[e, r]
model.a41_4 = Constraint(model.K, model.J, model.E, model.R, rule=a41_4)
def a41_5(model, k, j, e, r):
    return model.tekjer[k, j, e, r] - model.Te[e] - model.tlre[e] - model.ter[e, r] <= LargeNumber * model.y4kjer[k, j, e, r]
model.a41_5 = Constraint(model.K, model.J, model.E, model.R, rule=a41_5)

def a41_6(model, k, j, e, r):
    return LargeNumber * (1-model.y4kjer[k, j, e, r]) +  model.Ze[e] >= model.Te[e]
model.a41_6 = Constraint(model.K, model.J, model.E, model.R, rule=a41_6) 
def a41_7(model, k, j, e, r):
    return - LargeNumber * (2 - model.y4kjer[k, j, e, r] - model.xkjer[k, j, e, r]) <= model.tekjer[k, j, e, r] - model.Ze[e] - model.tlre[e] - model.ter[e, r]
model.a41_7 = Constraint(model.K, model.J, model.E, model.R, rule=a41_7)
def a41_8(model, k, j, e, r):
    return model.tekjer[k, j, e, r] - model.Ze[e] - model.tlre[e] - model.ter[e, r] <= LargeNumber * (2 - model.y4kjer[k, j, e, r] - model.xkjer[k, j, e, r])
model.a41_8 = Constraint(model.K, model.J, model.E, model.R, rule=a41_8)


# 晚于时间窗到达货主处的惩罚成本
def a42_1(model, k, j, e, r):
    return model.tekjer[k, j, e, r] <= model.be[e] + LargeNumber * model.y2kjer[k, j, e, r]
model.a42_1 = Constraint(model.K, model.J, model.E, model.R, rule=a42_1)

def a42_2(model, k, j, e, r):
    return - model.y2kjer[k, j, e, r] * LargeNumber <= model.fkjer[k, j, e, r] 
model.a42_2 = Constraint(model.K, model.J, model.E, model.R, rule=a42_2)

def a42_3(model, k, j, e, r):
    return model.fkjer[k, j, e, r] <= model.y2kjer[k, j, e, r] * LargeNumber 
model.a42_3 = Constraint(model.K, model.J, model.E, model.R, rule=a42_3)


def a42_6(model, k, j, e, r):
    return LargeNumber * (1 - model.y2kjer[k, j, e, r]) + model.tekjer[k, j, e, r] >= model.be[e]
model.a42_6 = Constraint(model.K, model.J, model.E, model.R, rule=a42_6)

def a42_4(model, k, j, e, r):
    return - model.xkjer[k, j, e, r] * LargeNumber <= model.fkjer[k, j, e, r]  
model.a42_4 = Constraint(model.K, model.J, model.E, model.R, rule=a42_4)

def a42_5(model, k, j, e, r):
    return model.fkjer[k, j, e, r] <= model.xkjer[k, j, e, r] * LargeNumber
model.a42_5 = Constraint(model.K, model.J, model.E, model.R, rule=a42_5)

def a42_7(model,k, j, e, r):
    return - LargeNumber * (2 - model.y2kjer[k, j, e, r] - model.xkjer[k, j, e, r] ) <= model.fkjer[k, j, e, r] - (model.tekjer[k, j, e, r] - model.be[e] ) * f 
model.a42_7 = Constraint(model.K, model.J, model.E, model.R, rule=a42_7)

def a42_8(model, k, j, e, r):
    return model.fkjer[k, j, e, r] - (model.tekjer[k, j, e, r] - model.be[e] ) * f <= LargeNumber * (2 - model.y2kjer[k, j, e, r] - model.xkjer[k, j, e, r])
model.a42_8 = Constraint(model.K, model.J, model.E, model.R, rule=a42_8)


###货物到达客户处，考虑客户的时间满意度

def a43_1(model, k, j, e, r):
    return   model.tekjer[k, j, e, r] == model.m1kjer[k, j, e, r] * model.x1[e] + model.m2kjer[k, j, e, r] * model.x2[e] + model.m3kjer[k, j, e, r] * model.x3[e] + model.m4kjer[k, j, e, r] * model.x4[e]
model.a43_1 = Constraint(model.K, model.J, model.E, model.R, rule=a43_1)

def a43_2(model, k, j, e, r):
    return  model.Stekjer[k, j, e, r] == model.m2kjer[k, j, e, r] + model.m3kjer[k, j, e, r]
model.a43_2 = Constraint(model.K, model.J, model.E, model.R, rule=a43_2)

def a43_3(model, k, j, e, r):
    return model.m1kjer[k, j, e, r] <= model.y6kjer[k, j, e, r]  
model.a43_3 = Constraint(model.K, model.J, model.E, model.R, rule=a43_3)

def a43_4(model, k, j, e, r):
    return model.m2kjer[k, j, e, r] <= model.y6kjer[k, j, e, r] + model.y7kjer[k, j, e, r]
model.a43_4 = Constraint(model.K, model.J, model.E, model.R, rule=a43_4) 

def a43_5(model, k, j, e, r):
    return model.m3kjer[k, j, e, r] <= model.y7kjer[k, j, e, r] + model.y8kjer[k, j, e, r]
model.a43_5 = Constraint(model.K, model.J, model.E, model.R, rule=a43_5)

def a43_6(model, k, j, e, r):
    return   model.m4kjer[k, j, e, r] <= model.y8kjer[k, j, e, r] 
model.a43_6 = Constraint(model.K, model.J, model.E, model.R, rule=a43_6)

def a43_7(model, k, j, e, r):
    return   sum(model.m1kjer[k, j, e, r] + model.m2kjer[k, j, e, r] + model.m3kjer[k, j, e, r] + model.m4kjer[k, j, e, r] for k in model.K for r in model.R) == 1
model.a43_7 = Constraint(model.K, model.J, model.E, model.R, rule=a43_7)

def a43_8(model, k, j, e, r):
    return  sum(model.y6kjer[k, j, e, r] + model.y7kjer[k, j, e, r] + model.y8kjer[k, j, e, r] for k in model.K for r in model.R )  == 1
model.a43_8 = Constraint(model.K, model.J, model.E, model.R, rule=a43_8)


def a43_17(model, k, j, e, r):
    return   model.Stekjer[k, j, e, r] + LargeNumber * (1 - model.xkjer[k, j, e, r]) >= h
model.a43_17 = Constraint(model.K, model.J, model.E, model.R, rule=a43_17)

# solve the problem
solver = SolverFactory("cplex")
# solver.options['timelimit'] = 60  # 求解时间为1min
# solver = SolverFactory("gurobi")
# solver.options['IntFeasTol'] = 1E-6
instance = model.create_instance("./Data/moxing2-1205.dat")
# results = solver.solve(instance)
results = solver.solve(instance, tee=True)
instance.display('./temp.yml')
print("done.")
print(results)