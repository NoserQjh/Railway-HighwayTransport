'''
Author: NoserQJH
LastEditors: NoserQJH
Date: 2021-07-28 14:46:47
LastEditTime: 2021-09-29 09:47:43
Description:
    数据文件读取脚本
'''

'''
dat中没有:
    tskjir 
'''




import numpy as np
def readDat(filename):
    with open(filename, 'r') as f:
        s = f.read()
    s = s.replace('\n', ' ')
    s = s.replace('\t', ' ')
    s = s.split('; ')
    x = [x.split(' := ') for x in s]

    result = dict()

    for item in x:
        item[0] = item[0].lstrip(' ').split(' ')
        if item[0][0] == 'set':
            item[1] = item[1].strip().split(' ')
            item[1] = [int(x) for x in item[1]]
            result[item[0][1]] = list(item[1])

    I = len(result['I'])
    E = len(result['E'])
    J = len(result['J'])
    K = len(result['K'])
    R = len(result['R'])
    T = len(result['T'])
    N = len(result['N'])

    for item in x:
        if item[0][0] == 'param':
            item[1] = item[1].strip(' ').strip(';').split(' ')
            l = []
            for i in item[1]:
                if i == '':
                    pass
                else:
                    l.append(float(i))
            pass

            if item[0][1] in ['dvi', 'Ni', 'mi', 'ni', 'bia', 'clni', 'cln2i', 'cuni', 'Qei', 'Qri', 'qi']:
                l = np.array(l)
                l.resize(I, 2)
                result[item[0][1]] = l[:, 1]

            elif item[0][1] in ['Cir', 'vir']:
                l = np.array(l)
                l.resize(I, R+1)
                result[item[0][1]] = l[:, 1:]

            elif item[0][1] in ['tdkj', 'Nkj']:
                l = np.array(l)
                l.resize(K, J+1)
                result[item[0][1]] = l[:, 1:]

            elif item[0][1] in ['dkjir']:
                l = np.array(l)
                d = np.zeros([K, J, I, R])

                l.resize(K*J*I*R, 5)
                for i in range(l.shape[0]):
                    d[result['K'].index(l[i, 0]), result['J'].index(l[i, 1]), result['I'].index(
                        l[i, 2]), result['R'].index(l[i, 3])] = l[i, 4]
                result[item[0][1]] = d

            elif item[0][1] in ['d0kji', 'tlckji']:
                l = np.array(l)
                d = np.zeros([K, J, I])

                l.resize(K*J*I, 4)
                for i in range(l.shape[0]):
                    d[result['K'].index(l[i, 0]), result['J'].index(l[i, 1]), result['I'].index(
                        l[i, 2])] = l[i, 3]
                result[item[0][1]] = d

            elif item[0][1] in ['dve', 'Ne', 'bea', 'pe', 'qe', 'ae', 'be', 'Te']:
                l = np.array(l)
                l.resize(I, 2)
                result[item[0][1]] = l[:, 1]

            elif item[0][1] in ['Cer', 'ver']:
                l = np.array(l)
                l.resize(I, R+1)
                result[item[0][1]] = l[:, 1:]

            elif item[0][1] in ['dkjer']:
                l = np.array(l)
                d = np.zeros([K, J, I, R])

                l.resize(K*J*I*R, 5)
                for i in range(l.shape[0]):
                    d[result['K'].index(l[i, 0]), result['J'].index(l[i, 1]), result['I'].index(
                        l[i, 2]), result['R'].index(l[i, 3])] = l[i, 4]
                result[item[0][1]] = d

            elif item[0][1] in ['d0kje', 'tlrkje']:
                l = np.array(l)
                d = np.zeros([K, J, I])

                l.resize(K*J*I, 4)
                for i in range(l.shape[0]):
                    d[result['K'].index(l[i, 0]), result['J'].index(l[i, 1]), result['I'].index(
                        l[i, 2])] = l[i, 3]
                result[item[0][1]] = d

            else:
                print(item[0][1])
    return result


if __name__ == '__main__':
    x = readDat('./Data/moxing2-1124.dat')
    x
