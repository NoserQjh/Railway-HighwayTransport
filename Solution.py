
import numpy as np
import DatRW as rw
import random
LargeNum = 99999999


def relu(x):
    return x * (x > 0)


class Solution:
    def __init__(self, info, seed=0, type=1):
        self.info = info

        self.init_static_param()
        # 节点
        self.I = info['I']
        self.E = info['E']
        self.J = info['J']
        self.K = info['K']
        self.R = info['R']
        self.T = info['T']
        self.N = info['N']

        # Cir 选择路线r时，中标运输订单i的单位运输成本
        self.Cir = info['Cir']
        # dir 选择路线r时，中标运输订单i的单位运输距离
        self.dkjir = info['dkjir']
        # vir 选择路线r时，中标运输订单i的单位运输速度
        self.vir = info['vir']

        # dji 从既有运输订单j的终点到运输订单i的起点的空车行驶距离
        self.d0kji = info['d0kji']

        # tdkj  运输订单j的卡车k到达终点的时刻
        self.tdkj = info['tdkj']

        # 既有运输订单j的车辆数
        self.Nkj = info['Nkj']

        # Ni 中标运输订单i的集装箱
        self.Ni = info['Ni']

        # bia 中标运输订单i的单位报价
        self.bia = info['bia']

        # dvi 中标运输订单i的平均运输距离
        self.dvi = info['dvi']

        # TODO Trni 列车运行时刻表
        # self.Trni = info['Trni']

        # clni 铁路端时间窗的下限
        self.clni = info['clni']

        # clni 铁路端时间窗的上限
        self.cuni = info['cuni']

        # cln2i 下一班次列车出发的铁路端时间窗的下限
        self.cln2i = info['cln2i']

        # TODO mi 去货主处提货的时间窗下限
        # self.mi=info['mi']

        # ni 去货主处提货的时间窗上限
        self.ni = info['ni']

        # tlckji 在客户处装货或卸货的时间
        self.tlckji = info['tlckji']

        # TODO tskji 在铁路场站的免费堆存时间
        # self.tskjir = info['tskjir']

        # Qei 运输订单i所到的铁路场站的其他货物重量
        self.Qei = info['Qei']
        # Qri 运输订单i所到的铁路场站的运能
        self.Qri = info['Qri']
        # qi 运输订单i所到的铁路场站的列车运力
        self.qi = info['qi']

        # Te 运输订单e的列车到达时刻
        self.Te = info['Te']

        # Cer 选择路线r时，中标运输订单e的单位运输成本
        self.Cer = info['Cer']

        # dkjer 选择路线r时，中标运输订单e的单位运输距离
        self.dkjer = info['dkjer']

        # ver 选择路线r时，中标运输订单e的单位运输速度
        self.ver = info['ver']

        # d0kje 从既有运输订单j的终点到运输订单e的起点的空车行驶距离
        self.d0kje = info['d0kje']

        # Ne 中标运输订单e的集装箱
        self.Ne = info['Ne']

        # bea 中标运输订单e的单位报价
        self.bea = info['bea']

        # dve 中标运输订单e的平均运输距离
        self.dve = info['dve']

        # TODO pe 去铁路场站处提货的时间窗下限
        # self.pe = info['pe']

        # qe 去铁路场站处提货的时间窗上限
        self.qe = info['qe']

        # ae 去货主处提货的时间窗下限
        self.ae = info['ae']

        # be 去货主处提货的时间窗上限
        self.be = info['be']

        # tlrkje 在客户处装货或卸货的时间
        self.tlrkje = info['tlrkje']

        # xkjir 卡车K从既有运输订单j的终点运往中标运输订单i的起点且选择线路r运输集装箱
        self.xkjir = np.zeros(
            [len(self.K), len(self.J), len(self.I), len(self.R)])

        # xkjer 卡车K将运输订单e的集装箱从起点运往终点所选择的线路
        self.xkjer = np.zeros(
            [len(self.K), len(self.J), len(self.E), len(self.R)])

        # 提前算出
        # 路途运输时间
        self.tkjir = self.dkjir/self.vir

        # 空车定位时间
        self.tkji = self.d0kji/self.v0

        # 路途运输时间
        self.tkjer = self.dkjer/self.ver

        # 空车定位时间
        self.tkje = self.d0kje/self.v0

    def update(self):

        # 既有运输订单j的卡车到达中标运输订单i的货主处的时刻为：该卡车完成上一批运输订单的时刻 + 空车定位时间
        self.tckji = (np.expand_dims(self.tdkj, axis=2).repeat(
            len(self.I), axis=2)+self.tkji)*np.sum(self.xkjir, axis=3)

        self.Zi = np.max(np.max(self.tckji, 0), 0)

        # 惩罚成本
        self.fi = relu(self.Zi-self.ni)*self.Ni*self.f

        # 卡车到达铁路场站的时刻为：卡车到达货主处的最晚时刻 + 货物装车时间 + 运输时间
        self.tmkji = np.sum(self.xkjir*(np.expand_dims(
            self.tlckji+self.Zi, axis=3).repeat(len(self.R), axis=3)+self.tkjir), 3)

        self.use_cln = self.Ni < ((self.Qri-self.Qei)/self.qi)

        self.Dkjir_temp_0 = (self.tmkji < np.expand_dims(
            np.expand_dims(self.clni, 0).repeat(len(self.J), 0), 0).repeat(len(self.K), 0)) & self.use_cln
        self.Dkjir_temp_1 = ((1 - self.Dkjir_temp_0) * (self.tmkji < np.expand_dims(
            np.expand_dims(self.cuni, 0).repeat(len(self.J), 0), 0).repeat(len(self.K), 0))) & self.use_cln
        self.Dkjir_temp_2 = (self.tmkji >= np.expand_dims(
            np.expand_dims(self.cuni, 0).repeat(len(self.J), 0), 0).repeat(len(self.K), 0)) | (1 - self.use_cln)

        self.Dkjir = self.Dkjir_temp_0 * \
            relu(self.clni-self.tmkji-self.ts) * \
            np.sum(self.xkjir, 3)*self.st + \
            self.Dkjir_temp_2 * \
            relu(self.cln2i-self.tmkji-self.ts) * \
            np.sum(self.xkjir, 3)*self.st

        # 铁路

        # 既有运输订单j的卡车到达中标运输订单i的货主处的时刻为：该卡车完成上一批运输订单的时刻 + 空车定位时间
        self.tmkje = np.sum(self.xkjer, 3)*(self.tkje +
                                            np.expand_dims(self.tdkj, 2).repeat(len(self.E), 2))

        self.Ze = np.max(np.max(self.tmkje, 0), 0)

        self.Dkjer_temp_0 = self.Ze > self.qe
        self.Dkjer = self.Dkjer_temp_0 * \
            relu(self.qe-self.Ze-self.ts) * \
            np.sum(self.xkjer, 3)*self.st

        self.tekjer_temp_0 = self.Ze <= self.ae

        self.tekjer_temp_1 = self.Ze > self.be

        self.tekjer = self.tekjer_temp_0 *\
            (self.Te+self.tlrkje+np.sum(self.tkjer, 3)) * \
            np.sum(self.xkjer, 3) +\
            self.tekjer_temp_1 *\
            (self.Ze+self.tlrkje+np.sum(self.tkjer, 3)) * \
            np.sum(self.xkjer, 3)

        self.fkjer = (self.tekjer-self.be)*self.f*np.sum(self.xkjer, 3)

        self.ta_i = (np.expand_dims(np.expand_dims(self.ni, axis=0).repeat(len(self.K), axis=0), axis=1).repeat(
            len(self.J), axis=1)-np.expand_dims(self.tdkj, axis=2).repeat(len(self.I), axis=2))
        self.ta_e = (np.expand_dims(np.expand_dims(self.qe, axis=0).repeat(len(self.K), axis=0), axis=1).repeat(
            len(self.J), axis=1)-np.expand_dims(self.tdkj, axis=2).repeat(len(self.I), axis=2))

        pass

    def feasible(self):
        result = True
        # 车辆调配数=集装箱数量，所有车辆只能服务一个运输订单且只能利用一次
        # TODO后者不必在此写
        result &= not np.sum(
            self.Ni - np.sum(np.sum(np.sum(self.xkjir, axis=0), axis=0), axis=1))
        result &= not np.sum(
            self.Ne - np.sum(np.sum(np.sum(self.xkjer, axis=0), axis=0), axis=1))
        return result

    def Obj(self):
        # 盈利
        benefit_i = np.sum(self.bia*self.dvi*self.Ni)
        benefit_e = np.sum(self.bea*self.dve*self.Ne)

        # 运输成本
        cost_transfer_i = np.sum(self.xkjir*self.Cir*self.dkjir)
        cost_transfer_e = np.sum(self.xkjer*self.Cer*self.dkjer)

        # 空车定位成本
        cost_position_i = np.sum(np.sum(self.xkjir, axis=3)*self.d0kji*self.C0)
        cost_position_e = np.sum(np.sum(self.xkjer, axis=3)*self.d0kje*self.C0)

        # 仓储成本
        cost_storage_i = np.sum(self.Dkjir)
        cost_storage_e = np.sum(self.Dkjer)

        # 惩罚成本
        cost_punish_i = np.sum(self.fi)
        cost_punish_e = np.sum(self.fkjer)

        # 时间价值成本
        cost_ta_i = np.sum(np.sum(self.xkjir, 3)*self.ta_i)
        cost_ta_e = np.sum(np.sum(self.xkjer, 3)*self.ta_e)

        cost = benefit_i+benefit_e-cost_transfer_i-cost_transfer_e-cost_position_i-cost_position_e - \
            cost_storage_i-cost_storage_e-cost_punish_i-cost_punish_e-cost_ta_i-cost_ta_e
        return benefit_i+benefit_e-cost_transfer_i-cost_transfer_e-cost_position_i-cost_position_e-cost_storage_i-cost_storage_e-cost_punish_i-cost_punish_e-cost_ta_i-cost_ta_e

    def value(self):
        self.update()
        return self.feasible(), self.Obj()

    def generate_solution(self, x):

        self.xkjir = np.zeros(
            [len(self.K), len(self.J), len(self.I), len(self.R)])

        # xkjer 卡车K将运输订单e的集装箱从起点运往终点所选择的线路
        self.xkjer = np.zeros(
            [len(self.K), len(self.J), len(self.E), len(self.R)])

        for item in x:
            [k, j, idx, r, is_i] = item
            if is_i:
                self.xkjir[k, j, idx, r] = 1
            else:
                self.xkjer[k, j, idx, r] = 1

    def init_static_param(self):
        # C0 承运人的空车定位成本
        self.C0 = 5
        # v0 空车行驶速度
        self.v0 = 85
        # ts 在铁路场站的免费堆存时间
        self.ts = 1
        # st 在铁路场站的单位存储成本
        self.st = 5
        # sc 在客户处的单位存储成本
        self.sc = 5
        # f 单位惩罚成本
        self.f = 8
        # ta 单位时间价值成本
        self.ta = 2

        # h 时间满意度的约束值
        self.h = 0.8

        # 客户的容忍时间节点
        self.x1 = 20
        self.x2 = 20.8
        self.x3 = 21
        self.x4 = 23


class Agent:
    def __init__(self, x=[], obj=0, status=None, KJ=None):
        self.x = x
        self.obj = obj
        self.status = status
        self.KJ = KJ

    def tokey(self):
        result = ''
        for x in self.status.tolist():
            result += str(x)
        return result


if __name__ == '__main__':

    random.seed(1)
    solution = Solution(rw.readDat('./Data/moxing2-1124.dat'))
    solution.update()
    solution.feasible()
    solution.Obj()
    agent = Agent([], solution.Ni, solution.Ne)
    pass
