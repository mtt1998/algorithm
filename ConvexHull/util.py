import math
import functools
import random
import matplotlib.pyplot as plt

random.seed(42)

ESP = 1e-8

def cal_crossdot(p, q):
    return p[0] * q[1] - p[1] * q[0]

def cal_dis(p, q):
    return math.sqrt((p[0] - q[0]) * (p[0] - q[0]) + (p[1] - q[1]) * (p[1] - q[1]))

#以a1为原点，计算a2 X a3,如果|a||b|sin大于0,说明左转 (==0 共线，尤其和p0共线且成为一条边时需要小心，
# 如果不是和p0共线，那么可以根据极角区分访问的正确顺序)
def left_rotate(a1, a2, a3):
    tmp = cal_crossdot((a2[0] - a1[0], a2[1] - a1[1]), (a3[0] - a1[0], a3[1] - a1[1]))
    if tmp > 0:
        return 1
    elif tmp < 0:
        return -1
    return 0


#大于则返回1，小于则返回-1，等于则返回0
def comp(centerp, x1, x2):
    if x1 is None:
        return 1
    if x2 is None:
        return -1
    tmp = left_rotate(centerp, x1, x2) #>0左转返回-1
    if tmp > 0:
        return -1
    elif tmp < 0:
        return 1
    elif cal_dis(centerp, x1) < cal_dis(centerp, x2):
        return -1
    else:
        return 1
    
def sort_theta(Q, centerp):
    #使用comp函数比较的前提是 规定一个方向(逆时针/顺时针)，那么任意两点都在(0，180)内，否则3者大小顺序不确定, 但一定是逆时针
    return sorted(Q,key=functools.cmp_to_key(lambda x,y:comp(centerp, x, y)))

def isInseg(a, st, end):
    dis1 = cal_dis(a, st) + cal_dis(a, end)
    dis2 = cal_dis(st, end)
    if dis1 < dis2 + ESP and dis1 > dis2 - ESP:
        return True
    return False


#判断p点是否在三角形ABC内
def isInside(p, a, b, c):
    if left_rotate(a, b, c) == 0: #如果不构成三角形,判断p是否在线段上
        return isInseg(p, a, b) or isInseg(p, a, c) or isInseg(p, b, c)
    # 如果pa在bc同侧, pb在ac同侧, pc在ab同侧,那么p点在ABC内或边/顶点上，return True
    pa_valid = left_rotate(b, c, p) + left_rotate(b, c, a)
    if abs(pa_valid) == 0: # -1, 1 异侧
        return False
    pb_valid = left_rotate(a, c, p) + left_rotate(a, c, b)
    if abs(pb_valid) == 0:
        return False
    pc_valid = left_rotate(a, b, p) + left_rotate(a, b, c)
    if abs(pc_valid) == 0:
        return False
    return True

#分治算法求第K小
def getKsmall(X, k):
    if len(X) < 5:
        return sorted(X)[k-1]
    while(len(X) % 5 != 0):
        X.append(float("inf"))
    medians = []
    for i in range(int(len(X)/5)):
        medians.append(sorted(X[i * 5: (i+1) * 5])[2])
    # print(len(X), k, len(medians), int((len(medians) + 1) / 2))
    mm = getKsmall(medians, int((len(medians) + 1) / 2))
    S = [[], [], []]
    for x in X:
        if x < mm:
            S[0].append(x)
        elif x == mm:
            S[1].append(x)
        else:
            S[2].append(x)
    # print(len(S[0]), len(S[1]), len(S[2]))
    if k <= len(S[0]):
        return getKsmall(S[0], k)
    elif k > len(S[0]) + len(S[1]):
        return getKsmall(S[2], k - len(S[0]) - len(S[1]))
    else:
        return mm


def random_points(r, N):
    Q = []
    for i in range(N):
        Q.append([random.random() * r, random.random() * r])
    return Q

def plotCH(Q, CH):
    plt.figure()
    for i in range(len(Q)):
        q = Q[i]
        plt.scatter(q[0], q[1], s=5, marker='o', color='green') # display all the points
#         plt.annotate(str(i), xy=q)
    for i in range(len(CH)):
        p = CH[i]
        q = CH[(i + 1) % len(CH)]
        plt.plot([p[0], q[0]], [p[1], q[1]], color='red') # display lines
        plt.scatter(p[0], p[1], s=10, marker='o', color='blue')
    plt.show()
