from numpy.core.defchararray import _to_string_or_unicode_array, add
from Solution import LargeNum, Solution, Agent, relu
import DatRW as rw
import numpy as np
from copy import deepcopy


class Model:
    def __init__(self, solution, init_agent):
        self.solution = solution
        self.last_list = {init_agent.tokey(): init_agent}
        self.next_list = {}

        self.tckji = (np.expand_dims(solution.tdkj, axis=2).repeat(
            len(solution.I), axis=2)+solution.tji)
        self.tckji = self.tckji*np.expand_dims(solution.Nkj, 2)

        self.tmkje = (solution.tje + np.expand_dims(solution.tdkj,
                                                    2).repeat(len(solution.E), 2))

        self.t_indexes_i = []
        for i in range(len(solution.I)):
            t_index = []
            for k in range(len(solution.K)):
                for j in range(len(solution.J)):
                    t_index.append([k, j, self.tckji[k, j, i]])

            t_index.sort(key=lambda x: x[2])
            self.t_indexes_i.append(t_index)

        self.t_indexes_e = []
        for i in range(len(solution.I)):
            t_index = []
            for k in range(len(solution.K)):
                for j in range(len(solution.J)):
                    t_index.append([k, j, self.tmkje[k, j, i]])

            t_index.sort(key=lambda x: x[2])
            self.t_indexes_e.append(t_index)

        # 惩罚
        # 仓储
        self.use_cln = solution.Ni < ((solution.Qi-solution.Qoi)/solution.qi)
        self.tmkjir = np.expand_dims(
            solution.tlci+self.tckji, 3).repeat(len(solution.R), 3)+solution.tir

        self.Dkjir_temp_0 = (self.tmkjir < np.expand_dims(solution.clni, 1).repeat(
            len(solution.R), 1)) & np.expand_dims(self.use_cln, 1).repeat(len(solution.R), 1)
        self.Dkjir_temp_1 = ((1 - self.Dkjir_temp_0) * (self.tmkjir < np.expand_dims(solution.cuni, 1).repeat(
            len(solution.R), 1))) & np.expand_dims(self.use_cln, 1).repeat(len(solution.R), 1)
        self.Dkjir_temp_2 = (self.tmkjir >= np.expand_dims(solution.cuni, 1).repeat(len(
            solution.R), 1)) | (1 - np.expand_dims(self.use_cln, 1).repeat(len(solution.R), 1))

        self.Dkjir = self.Dkjir_temp_0 * \
            relu(np.expand_dims(solution.clni, 1).repeat(len(solution.R), 1)-self.tmkjir-solution.ts) * solution.st + \
            self.Dkjir_temp_2 * \
            relu(np.expand_dims(solution.cln2i, 1).repeat(
                len(solution.R), 1)-self.tmkjir-solution.ts) * solution.st

        self.Dkjer_temp_0 = self.tmkje > solution.qe
        self.Dkjer = self.Dkjer_temp_0 * \
            relu(solution.qe-self.tmkje-solution.ts) * solution.st

        # 运输
        self.cost_transfer_i = solution.Cir*solution.dir

        self.sum_d_transfer_i = self.Dkjir + self.cost_transfer_i
        self.r_kji = np.argmin(self.sum_d_transfer_i, 3)

        self.cost_transfer_e = solution.Cer*solution.der

        self.r_je = np.argmin(self.cost_transfer_e, 1)

        # 空车定位
        self.cost_position_i = solution.dji*solution.C0
        self.cost_position_e = solution.dje*solution.C0

        # 时间价值
        self.cost_ta_i = (np.expand_dims(np.expand_dims(solution.ni, axis=0).repeat(len(solution.K), axis=0), axis=1).repeat(
            len(solution.J), axis=1)-np.expand_dims(solution.tdkj, axis=2).repeat(len(solution.I), axis=2))*solution.ta
        self.cost_ta_e = (np.expand_dims(np.expand_dims(solution.qe, axis=0).repeat(len(solution.K), axis=0), axis=1).repeat(
            len(solution.J), axis=1)-np.expand_dims(solution.tdkj, axis=2).repeat(len(solution.I), axis=2))*solution.ta

        self.sum_ta_position_i = self.cost_position_i+self.cost_ta_i
        self.sum_ta_position_e = self.cost_position_e+self.cost_ta_e

        self.ta_position_list_i = []
        for i in range(len(solution.I)):
            ta_position = []
            for k in range(len(solution.K)):
                for j in range(len(solution.J)):
                    ta_position.append([k, j, self.sum_ta_position_i[k, j, i]])
            ta_position.sort(key=lambda x: x[2])
            self.ta_position_list_i.append(ta_position)

        self.ta_position_list_e = []
        for e in range(len(solution.E)):
            ta_position = []
            for k in range(len(solution.K)):
                for j in range(len(solution.J)):
                    ta_position.append([k, j, self.sum_ta_position_e[k, j, e]])
            ta_position.sort(key=lambda x: x[2])
            self.ta_position_list_e.append(ta_position)
        pass

    def run(self):

        while(True):
            for agent in self.last_list.values():
                for i in range(len(agent.status)):
                    if agent.status[i] == 0:
                        new_agent = self.update_agent(agent, i)
                        if new_agent.tokey() not in self.next_list.keys():
                            self.next_list[new_agent.tokey()] = new_agent
                        else:
                            if new_agent.obj > self.next_list[new_agent.tokey()].obj:
                                self.next_list[new_agent.tokey()] = new_agent
            self.last_list = self.next_list
            if len(self.last_list) == 1:
                break
            self.next_list = {}
        return self.next_list['1111']

    def update_agent(self, agent, num):
        agent_new = deepcopy(agent)
        agent_new.status[num] = 1
        self.solution.generate_solution(agent.x)
        self.solution.update()

        if num < len(self.solution.I):
            # 公转铁
            i = num
            t_index = []
            for k, j, value in self.t_indexes_i[i]:
                if not agent_new.KJ[k, j]:
                    t_index.append([k, j, value])

            best_obj = 0
            for k, j, cost_dt in t_index:
                r = self.r_kji[k, j, i]
                add_list = [[k, j, i, r, 1]]
                sum_cost_tp = 0
                for k_, j_, cost_tp in self.ta_position_list_i[i]:
                    if agent_new.KJ[k_, j_] == 0 and self.tckji[k_, j_, i] <= self.tckji[k, j, i] and not(k == k_ and j == j_):
                        add_list.append([k_, j_, i, r, 1])
                        sum_cost_tp += cost_tp
                    if len(add_list) == solution.Ni[i]:
                        break
                solution.generate_solution(agent_new.x+add_list)
                feas, val = solution.value()
                if val > best_obj:
                    best_obj = val
                    best_add = add_list
            agent_new.obj = best_obj
            agent_new.x = agent_new.x+best_add
            for k, j, _, _, _ in best_add:
                agent_new.KJ[k, j] = 1
        else:
            # 铁转公
            e = num-len(solution.I)
            t_index = []
            for k, j, value in self.t_indexes_e[e]:
                if not agent_new.KJ[k, j]:
                    t_index.append([k, j, value])

            best_obj = 0
            for k, j, cost_dt in t_index:
                r = self.r_je[e]
                add_list = [[k, j, e, r, 0]]
                for k_, j_, _ in self.ta_position_list_e[e]:
                    if agent_new.KJ[k_, j_] == 0 and self.tckji[k_, j_, e] <= self.tckji[k, j, e] and not(k == k_ and j == j_):
                        add_list.append([k_, j_, e, r, 0])
                    if len(add_list) == solution.Ni[e]:
                        break
                solution.generate_solution(agent_new.x+add_list)
                feas, val = solution.value()
                if val > best_obj:
                    best_obj = val
                    best_add = add_list
            agent_new.obj = best_obj
            agent_new.x = agent_new.x+best_add
            for k, j, _, _, _ in best_add:
                agent_new.KJ[k, j] = 1
        print(agent_new.tokey())
        xkjir_list = []
        xkjer_list = []
        for k, j, i, r, is_i in agent_new.x:
            if is_i:
                xkjir_list.append([k+1, j+3, i+1, r+1])
            else:
                xkjer_list.append([k+1, j+3, i+1, r+1])
        return agent_new


solution = Solution(rw.readDat('./Data/moxing2-1205.dat'))

init_status = np.zeros(len(solution.Ni)+len(solution.Ne)).astype(np.int)
init_KJ = np.zeros([len(solution.K), len(solution.J)])
init_agent = Agent([], status=init_status, KJ=init_KJ)

model = Model(solution, init_agent)

result = model.run()
solution.generate_solution(result.x)
value = solution.value()
pass
# 逐订单遍历
