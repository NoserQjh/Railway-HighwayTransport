from numpy.core.defchararray import _to_string_or_unicode_array, add
from Solution import LargeNum, Solution, Agent
import DatRW as rw
import numpy as np
from copy import deepcopy


def find_r_i(k, j, i):
    best_obj_temp = 0
    result = -1
    for r in range(len(solution.R)):
        solution.xkjir[k, j, i, r] = 1
        solution.update()
        obj = solution.Obj()
        if best_obj_temp < obj:
            result = r
            best_obj_temp = obj
        solution.xkjir[k, j, i, r] = 0
    return result, best_obj_temp


def find_r_e(k, j, e):
    best_obj_temp = 0
    result = -1
    for r in range(len(solution.R)):
        solution.xkjer[k, j, e, r] = 1
        solution.update()
        obj = solution.Obj()
        if best_obj_temp < obj:
            result = r
            best_obj_temp = obj
        solution.xkjer[k, j, e, r] = 0
    return result, best_obj_temp


def update_agent(agent, num):
    agent_new = deepcopy(agent)
    agent_new.status[num] = 1
    solution.generate_solution(agent.x)
    solution.update()

    if num < len(solution.I):
        # 公转铁

        tckji = (np.expand_dims(solution.tdkj, axis=2).repeat(
            len(solution.I), axis=2)+solution.tkji)
        tckji = tckji*np.expand_dims(solution.Nkj, 2).repeat(
            len(solution.I), 2)*np.expand_dims(1-agent_new.KJ, 2).repeat(len(solution.I), 2)

        t_index = []
        for k in range(len(solution.K)):
            for j in range(len(solution.J)):
                if tckji[k, j, num] > 0:
                    t_index.append([k, j, tckji[k, j, num]])

        t_index.sort(key=lambda x: x[2])

        best_obj = 0
        for idx1 in range(int(solution.Ni[num]-1), len(t_index)):
            k, j, _ = t_index[idx1]
            r, obj = find_r_i(k, j, num)
            added_x = [[k, j, num, r, 0, obj]]
            solution.xkjir[k, j, num, r] = 1
            temp_list = []
            for idx2 in range(idx1):
                k, j, _ = t_index[idx2]
                r, obj = find_r_i(k, j, num)
                temp_list.append([k, j, num, r, 0, obj])
            temp_list.sort(key=lambda x: x[5])
            added_x += temp_list[-int(solution.Ni[num]-1):]
            for x in added_x:
                x.pop()
            solution.generate_solution(agent_new.x+added_x)
            solution.update()
            obj = solution.Obj()
            if obj > best_obj:
                best_obj = obj
                best_added_x = added_x
        agent_new.x += best_added_x
        for x in best_added_x:
            k, j, _, _, _ = x
            agent_new.KJ[k,j] = 1
        agent_new.obj = best_obj
        best_obj = best_obj

    else:
        num-=len(solution.I)
        # 铁转公
        tmkje = (solution.tkje +np.expand_dims(solution.tdkj, 2).repeat(len(solution.E), 2))
        tmkje = tmkje*np.expand_dims(solution.Nkj, 2).repeat(
            len(solution.I), 2)*np.expand_dims(1-agent_new.KJ, 2).repeat(len(solution.I), 2)
        t_index = []
        for k in range(len(solution.K)):
            for j in range(len(solution.J)):
                if tmkje[k, j, num] > 0:
                    t_index.append([k, j, tmkje[k, j, num]])

        t_index.sort(key=lambda x: x[2])

        best_obj = 0
        for idx1 in range(int(solution.Ni[num]-1), len(t_index)):
            k, j, _ = t_index[idx1]
            r, obj = find_r_e(k, j, num)
            added_x = [[k, j, num, r, 1, obj]]
            solution.xkjir[k, j, num, r] = 1
            temp_list = []
            for idx2 in range(idx1):
                k, j, _ = t_index[idx2]
                r, obj = find_r_e(k, j, num)
                temp_list.append([k, j, num, r, 1, obj])
            temp_list.sort(key=lambda x: x[5])
            added_x += temp_list[-int(solution.Ni[num]-1):]
            for x in added_x:
                x.pop()
            solution.generate_solution(agent_new.x+added_x)
            solution.update()
            obj = solution.Obj()
            if obj > best_obj:
                best_obj = obj
                best_added_x = added_x
        agent_new.x += best_added_x
        for x in best_added_x:
            k, j, _, _, _ = x
            agent_new.KJ[k,j] = 1
        agent_new.obj = best_obj
        best_obj = best_obj
    return agent_new

solution = Solution(rw.readDat('./Data/moxing2-1124.dat'))

init_status = np.zeros(len(solution.Ni)+len(solution.Ne)).astype(np.int)
init_KJ = np.zeros([len(solution.K), len(solution.J)])
init_agent = Agent([], status=init_status, KJ=init_KJ)
last_list = {init_agent.tokey(): init_agent}
next_list = {}
while(True):
    for agent in last_list.values():
        for i in range(len(agent.status)):
            if agent.status[i] == 0:
                new_agent = update_agent(agent, i)
                if new_agent.tokey() not in next_list.keys():
                    next_list[new_agent.tokey()] = new_agent
                else:
                    if new_agent.obj > next_list[new_agent.tokey()].obj:
                        next_list[new_agent.tokey()] = new_agent
    last_list = next_list
    if len(last_list) == 1:
        break
    next_list = {}


result = next_list['1111']
solution.generate_solution(result.x)
solution.value()
pass
# 逐订单遍历
