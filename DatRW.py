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

            if item[0][1] in ['dvi', 'Ni', 'mi', 'ni', 'bia', 'clni', 'cln2i', 'cuni', 'Qoi', 'Qi', 'qi', 'tlci']:
                l = np.array(l)
                l.resize(I, 2)
                result[item[0][1]] = l[:, 1]

            elif item[0][1] in ['Cir', 'vir', 'dir']:
                l = np.array(l)
                l.resize(I, R+1)
                result[item[0][1]] = l[:, 1:]

            elif item[0][1] in ['dji']:
                l = np.array(l)
                l.resize(J, I+1)
                result[item[0][1]] = l[:, 1:]

            elif item[0][1] in ['tdkj', 'Nkj']:
                l = np.array(l)
                l.resize(K, J+1)
                result[item[0][1]] = l[:, 1:]

            elif item[0][1] in ['dve', 'Ne', 'bea', 'pe', 'qe', 'ae', 'be', 'Te', 'tlre', 'x1', 'x2', 'x3', 'x4']:
                l = np.array(l)
                l.resize(I, 2)
                result[item[0][1]] = l[:, 1]

            elif item[0][1] in ['Cer', 'ver', 'der']:
                l = np.array(l)
                l.resize(I, R+1)
                result[item[0][1]] = l[:, 1:]

            elif item[0][1] in ['dje']:
                l = np.array(l)
                l.resize(J, E+1)
                result[item[0][1]] = l[:, 1:]

            else:
                print(item[0][1])
    return result


if __name__ == '__main__':
    x = readDat('./Data/moxing2-1205.dat')
    x

'''
dir
dji
tlci
Qoi
Qi
der
dje
tlre
x1
x2
x3
x4
'''