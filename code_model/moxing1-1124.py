# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 15:40:46 2021

@author: 1
"""

##### （一）	第一套模型：当第一阶段模型输出结果为基于组合价格定价时，此时已经知道该中标运输订单和哪些既有运输订单一起组合，已经知道调配那些车去服务中标运输订单

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
# rtj 选择路线r时，中标运输订单i的单位运输成本(协同值)      
model.rtj = Param(model.J)
# Cir 选择路线r时，中标运输订单i的单位运输成本
model.Cir = Param(model.I, model.R)
# dkjir 选择路线r时，中标运输订单i的单位运输距离
model.dkjir = Param(model.K, model.J, model.I, model.R)
# vir 选择路线r时，中标运输订单i的单位运输速度
model.vir = Param(model.I, model.R)
# d0kji 从既有运输订单j的终点到运输订单i的起点的空车行驶距离
model.d0kji = Param(model.K, model.J, model.I)
# tdkj  运输订单j的卡车k到达终点的时刻
model.tdkj = Param(model.K, model.J)
# Nkj 既有运输订单j的车辆k     
model.Nkj = Param(model.K, model.J)
# Ni 中标运输订单i的集装箱
model.Ni = Param(model.I)
# dvi 中标运输订单i的平均运输距离
model.dvi = Param(model.I)
# Trn 列车运行时刻表
model.Trni = Param(model.T, model.I)
# clni 铁路端时间窗的下限
model.clni = Param(model.I)
# cuni 铁路端时间窗的上限
model.cuni = Param(model.I)
# cln2i 下一班次列车出发的铁路端时间窗的下限
model.cln2i = Param(model.I)
# mi 去货主处提货的时间窗下限
model.mi = Param(model.I)
# ni 去货主处提货的时间窗上限    参数可变化
model.ni = Param(model.I)
# tlckji 在客户处装货或卸货的时间
model.tlckji = Param(model.K, model.J, model.I)
# tskji 在铁路场站的免费堆存时间
model.tskjir = Param(model.K, model.J, model.I,model.R)
# Qei 运输订单i所到的铁路场站的其他货物重量
model.Qei = Param(model.I)
# Qri 运输订单i所到的铁路场站的运能
model.Qri = Param(model.I)
# qi 运输订单i所到的铁路场站的列车运力
model.qi = Param(model.I)

###### 参数  铁路运输转公路运输
# Te 运输订单e的列车到达时刻
model.Te = Param(model.E)
# Cer 选择路线r时，中标运输订单e的单位运输成本
model.Cer = Param(model.E, model.R)
# dkjer 选择路线r时，中标运输订单e的单位运输距离
model.dkjer = Param(model.K, model.J, model.E, model.R)
# ver 选择路线r时，中标运输订单e的单位运输速度
model.ver = Param(model.E, model.R)
# d0kje 从既有运输订单j的终点到运输订单e的起点的空车行驶距离
model.d0kje = Param(model.K, model.J, model.E)
# Ne 中标运输订单e的集装箱
model.Ne = Param(model.E)
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
# tskje 在铁路场站的免费堆存时间
#model.tskjie = Param(model.K, model.J, model.I,model.E)
# mi 去货主处提货的时间窗下限
model.pe = Param(model.E)
# tlrkji 在客户处装货或卸货的时间
model.tlrkje = Param(model.K, model.J, model.E)



###### 变量  公路运输转铁路运输
# xkjir 卡车K从既有运输订单j的终点运往中标运输订单i的起点且选择线路r运输
model.xkjir = Var(model.K, model.J, model.I, model.R, domain=Binary)

# tkjir 选择路线r时，中标运输订单i的单位运输时间
model.tkjir = Var(model.K, model.J, model.I, model.R, domain=NonNegativeReals)
# tkji 从既有运输订单j的终点到运输订单i的起点的空车行驶时间
model.tkji = Var(model.K, model.J, model.I, domain=NonNegativeReals)

# mkji 在计算卡车到达货主处的辅助变量
model.mkji = Var(model.K, model.J, model.I, domain=Binary)
# zkji 在计算卡车到达货主处的辅助变量
model.Zkji = Var(model.K, model.J, model.I, domain=NonNegativeReals)
# y1kji 惩罚成本处的辅助变量
model.y1kji = Var(model.K, model.J, model.I, domain=Binary, initialize=0)
# d1kji 仓储成本处的辅助变量
model.d1kjir = Var(model.K, model.J, model.I, model.R, domain=Binary, initialize=0) 
# d2kji 仓储成本处的辅助变量
model.d2kjir = Var(model.K, model.J, model.I, model.R, domain=Binary, initialize=0)
# gi 仓储成本处的辅助变量
model.gi = Var(model.I, domain=Binary, initialize=0)

# Dkjir 总储存成本
model.Dkjir = Var(model.K, model.J, model.I, model.R, domain=NonNegativeReals, initialize=0)
# fkjir 总惩罚成本
model.fkjir = Var(model.K, model.J, model.I, model.R, domain=NonNegativeReals, initialize=0)
# tckji  卡车k到达运输订单i的铁路场站的时刻
model.tckji = Var(model.K, model.J, model.I, domain=NonNegativeReals, initialize=0)
# tmkjir  卡车k到达运输订单i的铁路场站的时刻
model.tmkjir = Var(model.K, model.J, model.I, model.R, domain=NonNegativeReals, initialize=0)
# tekji  卡车k到达运输订单i的终点的时刻
model.tekji = Var(model.K, model.J, model.I, domain=NonNegativeReals, initialize=0)



###### 变量  铁路运输转公路运输
# xkjer 卡车K将运输订单e的集装箱从起点运往终点所选择的线路
model.xkjer = Var(model.K, model.J, model.E, model.R, domain=Binary) 

# tkjer 选择路线r时，中标运输订单e的单位运输时间
model.tkjer = Var(model.K, model.J, model.E, model.R, domain=NonNegativeReals)
# tkje 从既有运输订单j的终点到运输订单e的起点的空车行驶时间
model.tkje = Var(model.K, model.J, model.E, domain=NonNegativeReals)

# tmkje  卡车k到达运输订单e的铁路场站的时刻
model.tmkje = Var(model.K, model.J, model.E, domain=NonNegativeReals, initialize=0)
# mkje 在计算卡车到达铁路场站处的辅助变量
model.mkje = Var(model.K, model.J, model.E, domain=Binary)
# zkje 在计算卡车到达铁路场站处的辅助变量
model.Zkje = Var(model.K, model.J, model.E, domain=NonNegativeReals)
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
h = 0.8

# 客户的容忍时间节点
x1 = 20
x2 = 20.8
x3 = 21
x4 = 23

# M无限大
LargeNumber = 100000


# 目标函数（求最大值）    
def Obj(model):
    return  sum(model.rtj[j]  * model.xkjir[k, j, i, r] * model.dvi[i] for i in model.I for j in model.J for k in model.K for r in model.R ) - \
           sum(model.xkjir[k, j, i, r] * model.Cir[i,r]  * model.dkjir[k, j, i,r] for i in model.I for r in model.R for j in model.J for k in model.K) - \
           sum(model.xkjir[k, j, i, r] * model.d0kji[k,j,i] * C0 for i in model.I for j in model.J for k in model.K for r in model.R) - \
           sum(model.Dkjir[k, j, i, r] for i in model.I for j in model.J for k in model.K for r in model.R) - sum(model.fkjir[k,j,i,r] for i in model.I for j in model.J for k in model.K for r in model.R) + \
           sum(model.rtj[j]  * model.xkjer[k, j, e, r] * model.dve[e] for e in model.E for j in model.J for k in model.K for r in model.R ) - \
           sum(model.xkjer[k, j, e, r] * model.Cir[e,r]  * model.dkjir[k, j, e,r] for e in model.E for r in model.R for j in model.J for k in model.K) - \
           sum(model.xkjer[k, j, e, r] * model.d0kje[k,j,e] * C0 for e in model.E for j in model.J for k in model.K for r in model.R) - \
           sum(model.Dkjer[k, j, e, r] for e in model.E for j in model.J for k in model.K for r in model.R) - sum(model.fkjer[k,j,e,r] for e in model.E for j in model.J for k in model.K for r in model.R) 


model.Obj = Objective(rule=Obj, sense=maximize)

# 约束，每个a后面的数字对应模型文本中的约束编号
########公路运输转铁路运输的情况 
## 路途运输时间   
def a2(model, k, j, i, r):
    return model.tkjir[k, j, i, r] == model.dkjir[k, j, i, r] / model.vir[i, r] 
model.a2 = Constraint(model.K, model.J, model.I, model.R, rule=a2)

## 空车定位时间   
def a3(model, k, j, i):
    return model.tkji[k, j, i] == model.d0kji[k, j, i] / v0 
model.a3 = Constraint(model.K, model.J, model.I, rule=a3)

# 车辆调配数=集装箱数量，所有车辆只能服务一个运输订单且只能利用一次！！！
def a4(model, k, j, i, r):  
    return  sum(model.xkjir[k, j, i, r] for k in model.K for j in model.J for r in model.R) == model.Ni[i]
model.a4 = Constraint(model.K, model.J, model.I, model.R, rule=a4)
def a5(model, k, j, i, r, e):  
    return  sum(model.xkjir[k, j, i, r] for i in model.I for r in model.R) + sum(model.xkjer[k, j, e, r] for e in model.E for r in model.R) <= 1
model.a5 = Constraint(model.K, model.J, model.I, model.R, model.E,rule=a5)


# 既有运输订单j的卡车到达中标运输订单i的货主处的时刻为：该卡车完成上一批运输订单的时刻 + 空车定位时间    
def a6(model, k, j, i, r):
    return LargeNumber * (1 - model.xkjir[k, j, i, r]) + model.tdkj[k, j] + model.tkji[k, j, i] >= model.tckji[k, j, i]
model.a6 = Constraint(model.K, model.J, model.I, model.R, rule=a6)
def a6_1(model, k, j, i, r):
    return model.tdkj[k, j] + model.tkji[k, j, i] <= model.tckji[k, j, i] + LargeNumber * (1 - model.xkjir[k, j, i, r])
model.a6_1 = Constraint(model.K, model.J, model.I, model.R, rule=a6_1)


#当从两个及以上地方调配卡车时，找到卡车到达货主处的最晚时间为：
def a7_1(model, k, j, i): 
    return  model.Zkji[k, j, i] >= model.tckji[k, j, i] 
model.a7_1 = Constraint(model.K, model.J, model.I, rule=a7_1)

def a7_2(model, k, j, i): 
    return  model.tckji[k, j, i] >= model.Zkji[k, j, i] - LargeNumber *  (1 - model.mkji[k, j, i]) 
model.a7_2 = Constraint(model.K, model.J, model.I, rule=a7_2)

def a7_3(model, k, j, i): 
    return  sum(model.mkji[k, j, i] for j in model.J for k in model.K for i in model.I) >= 1    
model.a7_3 = Constraint(model.K, model.J, model.I, rule=a7_3) 


#惩罚成本 
def a8_1(model, k, j, i):
    return model.Zkji[k, j, i] <= model.ni[i] + LargeNumber * model.y1kji[k, j, i]
model.a8_1 = Constraint(model.K, model.J, model.I, rule=a8_1)

def a8_2(model, k, j, i, r):
    return - model.y1kji[k, j, i] * LargeNumber <= model.fkjir[k, j, i, r] 
model.a8_2 = Constraint(model.K, model.J, model.I, model.R, rule=a8_2)

def a8_3(model, k, j, i, r):
    return model.fkjir[k, j, i, r] <= model.y1kji[k, j, i] * LargeNumber 
model.a8_3 = Constraint(model.K, model.J, model.I, model.R, rule=a8_3)

def a8_4(model, k, j, i, r):
    return - model.xkjir[k, j, i, r] * LargeNumber <= model.fkjir[k, j, i, r]  
model.a8_4 = Constraint(model.K, model.J, model.I, model.R, rule=a8_4)

def a8_5(model, k, j, i, r):
    return model.fkjir[k, j, i, r] <= model.xkjir[k, j, i, r] * LargeNumber
model.a8_5 = Constraint(model.K, model.J, model.I, model.R, rule=a8_5)

def a8_6(model, k, j, i, r):
    return LargeNumber * (1 - model.y1kji[k, j, i]) + model.Zkji[k, j, i] >= model.ni[i]
model.a8_6 = Constraint(model.K, model.J, model.I, model.R, rule=a8_6)

def a8_7(model,k, j, i, r):
    return - LargeNumber * (2 - model.y1kji[k, j, i] - model.xkjir[k, j, i, r]) <= model.fkjir[k, j, i, r] - (model.Zkji[k, j, i] - model.ni[i]) * f
model.a8_7 = Constraint(model.K, model.J, model.I, model.R, rule=a8_7)

def a8_8(model, k, j, i, r):
    return model.fkjir[k, j, i, r] - (model.Zkji[k, j, i] - model.ni[i]) * f <= LargeNumber * (2 - model.y1kji[k, j, i] - model.xkjir[k, j, i, r])
model.a8_8 = Constraint(model.K, model.J, model.I, model.R, rule=a8_8)
 
## 卡车到达铁路场站的时刻为：卡车到达货主处的最晚时刻 + 货物装车时间 + 运输时间     
def a10_1(model, k, j, i, r):
    return LargeNumber * (1 - model.xkjir[k, j, i, r]) + model.Zkji[k, j, i] + model.tlckji[k, j, i] + model.tkjir[k, j, i, r] >= model.tmkjir[k, j, i, r]
model.a10_1 = Constraint(model.K, model.J, model.I, model.R, rule=a10_1)
def a10_2(model, k, j, i, r):
    return model.Zkji[k, j, i] + model.tlckji[k, j, i] + model.tkjir[k, j, i, r] <= model.tmkjir[k, j, i, r] + LargeNumber * (1 - model.xkjir[k, j, i, r]) 
model.a10_2 = Constraint(model.K, model.J, model.I, model.R, rule=a10_2)


# 卡车到达铁路场站的每一个集装箱的仓储成本   # 构造0-1变量和大M
def a11_1(model, k, j, i, r):
    return  model.tmkjir[k, j, i, r] <= model.clni[i] + LargeNumber * model.d1kjir[k, j, i, r]
model.a11_1 = Constraint(model.K, model.J, model.I, model.R, rule=a11_1)

def a11_11(model, k, j, i, r):
    return - model.xkjir[k, j, i, r] * LargeNumber <= model.Dkjir[k, j, i, r]  
model.a11_11 = Constraint(model.K, model.J, model.I, model.R, rule=a11_11)

def a11_12(model, k, j, i, r):
    return model.Dkjir[k, j, i, r] <= model.xkjir[k, j, i, r] * LargeNumber
model.a11_12 = Constraint(model.K, model.J, model.I, model.R, rule=a11_12)

def a11_13(model, k, j, i, r):
    return - LargeNumber * (2 - model.d1kjir[k, j, i, r] - model.xkjir[k, j, i, r]) <= model.Dkjir[k, j, i, r] - (model.clni[i] - model.tmkjir[k, j, i, r] - ts) * st  
model.a11_13 = Constraint(model.K, model.J, model.I, model.R, rule=a11_13)

def a11_14(model, k, j, i, r):
    return model.Dkjir[k, j, i, r] - (model.clni[i] - model.tmkjir[k, j, i, r] - ts) * st  <= LargeNumber * (2 - model.d1kjir[k, j, i, r] - model.xkjir[k, j, i, r])
model.a11_14 = Constraint(model.K, model.J, model.I, model.R, rule=a11_14)



def a11_2(model, k, j, i, r):
    return  model.clni[i] - LargeNumber * model.d1kjir[k, j, i, r] <= model.tmkjir[k, j, i, r]
model.a11_2 = Constraint(model.K, model.J, model.I, model.R, rule=a11_2)

def a11_21(model, k, j, i, r):
    return  model.tmkjir[k, j, i, r] <= model.cuni[i] + LargeNumber * ( 1 - model.d1kjir[k, j, i, r])
model.a11_21 = Constraint(model.K, model.J, model.I, model.R, rule=a11_21)

def a11_22(model, k, j, i, r):
    return - LargeNumber * (2 - model.d1kjir[k, j, i, r] - model.xkjir[k, j, i, r]) <= model.Dkjir[k, j, i, r]
model.a11_22 = Constraint(model.K, model.J, model.I, model.R, rule=a11_22)

def a11_23(model, k, j, i, r):
    return model.Dkjir[k, j, i, r] <= LargeNumber * (2 - model.d1kjir[k, j, i, r] - model.xkjir[k, j, i, r])
model.a11_23 = Constraint(model.K, model.J, model.I, model.R, rule=a11_23)


def a11_3(model, k, j, i, r):
    return  model.cuni[i] - LargeNumber * model.d2kjir[k, j, i, r] <= model.tmkjir[k, j, i, r]
model.a11_3 = Constraint(model.K, model.J, model.I, model.R, rule=a11_3)

def a11_31(model, k, j, i, r):
    return  model.tmkjir[k, j, i, r] <= model.cuni[i] + LargeNumber * ( 1 - model.d2kjir[k, j, i, r])
model.a11_31 = Constraint(model.K, model.J, model.I, model.R, rule=a11_31)

def a11_34(model, k, j, i, r):
    return - model.xkjir[k, j, i, r] * LargeNumber <= model.Dkjir[k, j, i, r]  
model.a11_34 = Constraint(model.K, model.J, model.I, model.R, rule=a11_34)

def a11_35(model, k, j, i, r):
    return model.Dkjir[k, j, i, r] <= model.xkjir[k, j, i, r] * LargeNumber
model.a11_35 = Constraint(model.K, model.J, model.I, model.R, rule=a11_35)

def a11_36(model, k, j, i, r):
    return - LargeNumber * (3 - model.d1kjir[k, j, i, r] - model.d2kjir[k, j, i, r] - model.xkjir[k, j, i, r]) <= model.Dkjir[k, j, i, r] - (model.cln2i[i] - model.tmkjir[k, j, i, r] - ts) * st  
model.a11_36 = Constraint(model.K, model.J, model.I, model.R, rule=a11_36)

def a11_37(model, k, j, i, r):
    return model.Dkjir[k, j, i, r] - (model.cln2i[i] - model.tmkjir[k, j, i, r] - ts) * st  <= LargeNumber * (3 - model.d1kjir[k, j, i, r] - model.d2kjir[k, j, i, r] - model.xkjir[k, j, i, r])
model.a11_37 = Constraint(model.K, model.J, model.I, model.R, rule=a11_37)


#货物的容量不能超过可用列车车厢的容量（满足铁路运力要求） 
def a12_1(model, i):
    return model.qi[i] * model.Ni[i] + model.Qei[i] <= model.Qri[i] + LargeNumber * model.gi[i] 
model.a12_1 = Constraint(model.I, rule=a12_1)

def a12_2(model, k, j, i, r):
    return - model.gi[i] * LargeNumber <= model.Dkjir[k, j, i, r] 
model.a12_2 = Constraint(model.K, model.J, model.I, model.R, rule=a12_2)

def a12_3(model, k, j, i, r):
    return model.Dkjir[k, j, i, r] <= model.gi[i] * LargeNumber 
model.a12_3 = Constraint(model.K, model.J, model.I, model.R, rule=a12_3)

def a12_4(model, k, j, i, r):
    return - model.xkjir[k, j, i, r] * LargeNumber <= model.Dkjir[k, j, i, r]
model.a12_4 = Constraint(model.K, model.J, model.I, model.R, rule=a12_4)

def a12_5(model, k, j, i, r ):
    return model.Dkjir[k, j, i, r] <= model.xkjir[k, j, i, r] * LargeNumber
model.a12_5 = Constraint(model.K, model.J, model.I, model.R, rule=a12_5)

def a12_6(model, k, j, i, r):
    return LargeNumber * (1 - model.gi[i]) + model.qi[i] * model.Ni[i] + model.Qei[i] >= model.Qri[i]
model.a12_6 = Constraint(model.K, model.J, model.I, model.R, rule=a12_6)

def a12_7(model,k, j, i, r):
    return - LargeNumber * (2 - model.gi[i] - model.xkjir[k, j, i, r]) <= model.Dkjir[k, j, i, r] - (model.cln2i[i] - model.tmkjir[k, j, i, r] - ts) * st
model.a12_7 = Constraint(model.K, model.J, model.I, model.R, rule=a12_7)

def a12_8(model, k, j, i, r):
    return model.Dkjir[k, j, i, r] - (model.cln2i[i] - model.tmkjir[k, j, i, r] - ts) * st  <= LargeNumber * (2 - model.gi[i] - model.xkjir[k, j, i, r])
model.a12_8 = Constraint(model.K, model.J, model.I, model.R, rule=a12_8)




############铁路运输转公路运输的情况
## 路途运输时间   没问题！
def a13(model, k, j, e, r):
    return model.tkjer[k, j, e, r] == model.dkjer[k, j, e, r] / model.ver[e, r] 
model.a13= Constraint(model.K, model.J, model.E, model.R, rule=a13)

## 空车定位时间   没问题！
def a14(model, k, j, e):
    return model.tkje[k, j, e] == model.d0kje[k, j, e] / v0 
model.a14 = Constraint(model.K, model.J, model.E, rule=a14)

# 车辆调配数=集装箱数量   
def a15(model, k, j, e, r):  
    return  sum(model.xkjer[k, j, e, r] for k in model.K for j in model.J for r in model.R) == model.Ne[e] 
model.a15 = Constraint(model.K, model.J, model.E, model.R, rule=a15)



# 既有运输订单j的卡车到达中标运输订单e的货主处的时刻为：该卡车完成上一批运输订单的时刻 + 空车定位时间   
def a16(model, k, j, e, r):
    return LargeNumber * (1 - model.xkjer[k, j, e, r]) + model.tdkj[k, j] + model.tkje[k, j, e] >= model.tmkje[k, j, e]
model.a16 = Constraint(model.K, model.J, model.E, model.R, rule=a16)
def a16_1(model, k, j, e, r):
    return model.tdkj[k, j] + model.tkje[k, j, e] <= model.tmkje[k, j, e] + LargeNumber * (1 - model.xkjer[k, j, e, r])
model.a16_1 = Constraint(model.K, model.J, model.E, model.R, rule=a16_1)

#当从两个及以上地方调配卡车时，找到卡车到达铁路场站处的最晚时间为： 
def a17_1(model, k, j, e): 
    return  model.Zkje[k, j, e] >= model.tmkje[k, j, e]
model.a17_1 = Constraint(model.K, model.J, model.E, rule=a17_1)

def a17_2(model, k, j, e): 
    return  model.tmkje[k, j, e] >= model.Zkje[k, j, e] - LargeNumber *  (1 - model.mkje[k, j, e]) 
model.a17_2 = Constraint(model.K, model.J, model.E, rule=a17_2)

def a17_3(model, k, j, e): 
    return  sum(model.mkje[k, j, e] for j in model.J for k in model.K for e in model.E) >= 1    
model.a17_3 = Constraint(model.K, model.J, model.E, rule=a17_3) 


# 到处铁路场站处的仓储成本
def a18_1(model, k, j, e):
    return model.Zkje[k, j, e] <= model.qe[e] + LargeNumber * model.y1kje[k, j, e]
model.a18_1 = Constraint(model.K, model.J, model.E, rule=a18_1)

def a18_2(model, k, j, e, r):
    return - model.y1kje[k, j, e] * LargeNumber <= model.Dkjer[k, j, e, r] 
model.a18_2 = Constraint(model.K, model.J, model.E, model.R, rule=a18_2)

def a18_3(model, k, j, e, r):
    return model.Dkjer[k, j, e, r] <= model.y1kje[k, j, e] * LargeNumber 
model.a18_3 = Constraint(model.K, model.J, model.E, model.R, rule=a18_3)

def a18_4(model, k, j, e, r):
    return - model.xkjer[k, j, e, r] * LargeNumber <= model.Dkjer[k, j, e, r]  
model.a18_4 = Constraint(model.K, model.J, model.E, model.R, rule=a18_4)

def a18_5(model, k, j, e, r):
    return model.Dkjer[k, j, e, r] <= model.xkjer[k, j, e, r] * LargeNumber
model.a18_5 = Constraint(model.K, model.J, model.E, model.R, rule=a18_5)

def a18_6(model, k, j, e, r):
    return LargeNumber * (1 - model.y1kje[k, j, e]) + model.Zkje[k, j, e] >= model.qe[e]
model.a18_6 = Constraint(model.K, model.J, model.E, model.R, rule=a18_6)

def a18_7(model,k, j, e, r):
    return - LargeNumber * (2 - model.y1kje[k, j, e] - model.xkjer[k, j, e, r]) <= model.Dkjer[k, j, e, r] - (model.qe[e] - model.Zkje[k, j, e] - ts) * st
model.a18_7 = Constraint(model.K, model.J, model.E, model.R, rule=a18_7)

def a18_8(model, k, j, e, r):
    return model.Dkjer[k, j, e, r] - (model.qe[e] - model.Zkje[k, j, e] - ts) * st <= LargeNumber * (2 - model.y1kje[k, j, e] - model.xkjir[k, j, e, r])
model.a18_8 = Constraint(model.K, model.J, model.E, model.R, rule=a18_8)

## 卡车到达货主处的时刻为：
#当卡车早于时间窗到达时，中标运输订单e的卡车到达货主处的时刻为：列车到达的时刻 + 货物装车时间 + 运输时间；
#当卡车晚于时间窗到达时，中标运输订单e的卡车到达货主处的时刻为：卡车到达铁路场站处的时刻 + 货物装车时间 + 运输时间。
def a19_1(model, k, j, e, r):
    return model.Zkje[k, j, e] <= model.ae[e] + LargeNumber * model.y4kjer[k, j, e, r]
model.a19_1 = Constraint(model.K, model.J, model.E, model.R, rule=a19_1)
def a19_2(model, k, j, e, r):
    return - model.xkjer[k, j, e, r] * LargeNumber <= model.tekjer[k, j, e, r] 
model.a19_2 = Constraint(model.K, model.J, model.E, model.R, rule=a19_2)
def a19_3(model, k, j, e, r):
    return model.tekjer[k, j, e, r] <= model.xkjer[k, j, e, r] * LargeNumber 
model.a19_3 = Constraint(model.K, model.J, model.E, model.R, rule=a19_3)
def a19_4(model, k, j, e, r):
    return - LargeNumber * (2 - model.y4kjer[k, j, e, r] - model.xkjer[k, j, e, r]) <= model.tekjer[k, j, e, r] - model.Te[e] - model.tlrkje[k, j, e] - model.tkjer[k, j, e, r]
model.a19_4 = Constraint(model.K, model.J, model.E, model.R, rule=a19_4)
def a19_5(model, k, j, e, r):
    return model.tekjer[k, j, e, r] - model.Te[e] - model.tlrkje[k, j, e] - model.tkjer[k, j, e, r] <= LargeNumber * (2 - model.y4kjer[k, j, e, r] - model.xkjer[k, j, e, r])
model.a19_5 = Constraint(model.K, model.J, model.E, model.R, rule=a19_5)
def a19_6(model, k, j, e, r):
    return LargeNumber * model.y4kjer[k, j, e, r] +  model.Zkje[k, j, e] >= model.be[e]
model.a19_6 = Constraint(model.K, model.J, model.E, model.R, rule=a19_6)
def a19_7(model, k, j, e, r):
    return - LargeNumber * (2 - model.y4kjer[k, j, e, r] - model.xkjer[k, j, e, r]) <= model.tekjer[k, j, e, r] - model.Zkje[k, j, e] - model.tlrkje[k, j, e] - model.tkjer[k, j, e, r]
model.a19_7 = Constraint(model.K, model.J, model.E, model.R, rule=a19_7)
def a19_8(model, k, j, e, r):
    return model.tekjer[k, j, e, r] - model.Zkje[k, j, e] - model.tlrkje[k, j, e] - model.tkjer[k, j, e, r] <= LargeNumber * (2 - model.y4kjer[k, j, e, r] - model.xkjer[k, j, e, r])
model.a19_8 = Constraint(model.K, model.J, model.E, model.R, rule=a19_8)

# 晚于时间窗到达货主处的惩罚成本
def a20_1(model, k, j, e, r):
    return model.tekjer[k, j, e, r] <= model.be[e] + LargeNumber * model.y2kjer[k, j, e, r]
model.a20_1 = Constraint(model.K, model.J, model.E, model.R, rule=a20_1)

def a20_2(model, k, j, e, r):
    return - model.y2kjer[k, j, e, r] * LargeNumber <= model.fkjer[k, j, e, r] 
model.a20_2 = Constraint(model.K, model.J, model.E, model.R, rule=a20_2)

def a20_3(model, k, j, e, r):
    return model.fkjer[k, j, e, r] <= model.y2kjer[k, j, e, r] * LargeNumber 
model.a20_3 = Constraint(model.K, model.J, model.E, model.R, rule=a20_3)

def a20_4(model, k, j, e, r):
    return - model.xkjer[k, j, e, r] * LargeNumber <= model.fkjer[k, j, e, r]  
model.a20_4 = Constraint(model.K, model.J, model.E, model.R, rule=a20_4)

def a20_5(model, k, j, e, r):
    return model.fkjer[k, j, e, r] <= model.xkjer[k, j, e, r] * LargeNumber
model.a20_5 = Constraint(model.K, model.J, model.E, model.R, rule=a20_5)

def a20_6(model, k, j, e, r):
    return LargeNumber * (1 - model.y2kjer[k, j, e, r]) + model.tekjer[k, j, e, r] >= model.be[e]
model.a20_6 = Constraint(model.K, model.J, model.E, model.R, rule=a20_6)

def a20_7(model,k, j, e, r):
    return - LargeNumber * (2 - model.y2kjer[k, j, e, r] - model.xkjer[k, j, e, r]) <= model.fkjer[k, j, e, r] - (model.tekjer[k, j, e, r] - model.be[e] ) * f
model.a20_7 = Constraint(model.K, model.J, model.E, model.R, rule=a20_7)

def a20_8(model, k, j, e, r):
    return model.fkjer[k, j, e, r] - (model.tekjer[k, j, e, r] - model.be[e] ) * f <= LargeNumber * (2 - model.y2kjer[k, j, e, r] - model.xkjir[k, j, e, r])
model.a20_8 = Constraint(model.K, model.J, model.E, model.R, rule=a20_8)


#时间满意度，非线性函数，无法求解

###货物到达客户处，考虑客户的时间满意度
def a21_1(model, k, j, e, r):
    return   x1 - LargeNumber * model.y3kjer[k, j, e, r] <= model.tekjer[k, j, e, r]
model.a21_1 = Constraint(model.K, model.J, model.E, model.R, rule=a21_1)

def a21_2(model, k, j, e, r):
    return  model.tekjer[k, j, e, r] <= x2 + LargeNumber *  (1 - model.y3kjer[k, j, e, r])
model.a21_2 = Constraint(model.K, model.J, model.E, model.R, rule=a21_2)

def a21_3(model, k, j, e, r):
    return - model.xkjer[k, j, e, r] * LargeNumber <= model.Stekjer[k, j, e, r]  
model.a21_3 = Constraint(model.K, model.J, model.E, model.R, rule=a21_3)

def a21_4(model, k, j, e, r):
    return model.Stekjer[k, j, e, r] <= model.xkjer[k, j, e, r] * LargeNumber
model.a21_4 = Constraint(model.K, model.J, model.E, model.R, rule=a21_4)

def a21_5(model, k, j, e, r):
    return   - LargeNumber * (2 - model.y3kjer[k, j, e, r] - model.xkjer[k, j, e, r]) <= model.Stekjer[k, j, e, r] - ((model.tekjer[k, j, e, r] - x1)/ (x2 - x1)) 
model.a21_5 = Constraint(model.K, model.J, model.E, model.R, rule=a21_5)

def a21_6(model, k, j, e, r):
    return   model.Stekjer[k, j, e, r] - ((model.tekjer[k, j, e, r] - x1)/ (x2 - x1))  <= LargeNumber * (2 - model.y3kjer[k, j, e, r] - model.xkjer[k, j, e, r])
model.a21_6 = Constraint(model.K, model.J, model.E, model.R, rule=a21_6)


def a21_7(model, k, j, e, r):
    return   x2 - LargeNumber * model.y3kjer[k, j, e, r] <= model.tekjer[k, j, e, r]
model.a21_7 = Constraint(model.K, model.J, model.E, model.R, rule=a21_7)

def a21_8(model, k, j, e, r):
    return  model.tekjer[k, j, e, r] <= x3 + LargeNumber * (1- model.y3kjer[k, j, e, r])
model.a21_8 = Constraint(model.K, model.J, model.E, model.R, rule=a21_8)

def a21_9(model, k, j, e, r):
    return   - LargeNumber * (2 - model.y3kjer[k, j, e, r] - model.xkjer[k, j, e, r])<= model.Stekjer[k, j, e, r] - 1 
model.a21_9 = Constraint(model.K, model.J, model.E, model.R, rule=a21_9)

def a21_10(model, k, j, e, r):
    return   model.Stekjer[k, j, e, r] - 1  <= LargeNumber * (2 - model.y3kjer[k, j, e, r] - model.xkjer[k, j, e, r])
model.a21_10 = Constraint(model.K, model.J, model.E, model.R, rule=a21_10)



def a21_11(model, k, j, e, r):
    return   x3 - LargeNumber * model.y5kjer[k, j, e, r]<= model.tekjer[k, j, e, r]
model.a21_11 = Constraint(model.K, model.J, model.E, model.R, rule=a21_11)

def a21_12(model, k, j, e, r):
    return  model.tekjer[k, j, e, r] <= x4 + LargeNumber *  (1 - model.y5kjer[k, j, e, r])
model.a21_12 = Constraint(model.K, model.J, model.E, model.R, rule=a21_12)

def a21_15(model, k, j, e, r):
    return   - LargeNumber * (3- model.y3kjer[k, j, e, r] - model.y5kjer[k, j, e, r] - model.xkjer[k, j, e, r]) <= model.Stekjer[k, j, e, r] - (( x4 - model.tekjer[k, j, e, r])/ (x4 - x3)) 
model.a21_15 = Constraint(model.K, model.J, model.E, model.R, rule=a21_15)

def a21_16(model, k, j, e, r):
    return   model.Stekjer[k, j, e, r] - (( x4 - model.tekjer[k, j, e, r])/ (x4 - x3)) <= LargeNumber * (3- model.y3kjer[k, j, e, r] - model.y5kjer[k, j, e, r] - model.xkjer[k, j, e, r])
model.a21_16 = Constraint(model.K, model.J, model.E, model.R, rule=a21_16)


def a21_17(model, k, j, e, r):
    return   model.Stekjer[k, j, e, r] + LargeNumber * (1 - model.xkjer[k, j, e, r]) >= h
model.a21_17 = Constraint(model.K, model.J, model.E, model.R, rule=a21_17)


