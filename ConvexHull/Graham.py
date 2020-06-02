from util import *

def GrahamScan(Q, sort_flag=True):
    N = len(Q)
    if sort_flag:
        idx = 0
        for i in range(N):
            if Q[i][1] < Q[idx][1]:
                idx = i
            elif Q[i][1] == Q[idx][1] and Q[i][0] < Q[idx][0]:
                idx = i
        p = Q[idx]    
        #计算极角并逆时针从小到大排序
        Q = sort_theta(Q, p)
    #initialize Stack
    stk_arr = [Q[0], Q[1]]
    stk_top = 1
    #按顺序入栈，并弹出非法点(右转)
#     print(Q)
    for i in range(2, N):
        while (stk_top > 0) and (left_rotate(stk_arr[stk_top - 1], stk_arr[stk_top], Q[i]) <= 0):
            stk_arr.pop()
            stk_top -= 1
        stk_top += 1
        stk_arr.append(Q[i])
    stk_bottom = 0
    if not sort_flag:
        for j in range(0, stk_top + 1):
            #check stk_bottom, stk_top, stk_top - 1 
            while (stk_top > stk_bottom + 1):
                if j == stk_bottom:
                    ind1 = stk_top
                    ind2 = stk_top - 1
                elif j == stk_bottom + 1:
                    ind1 = stk_bottom
                    ind2 = stk_top
                if (left_rotate(stk_arr[ind2], stk_arr[ind1], stk_arr[j]) > 0):
                    break
                if j == stk_bottom:
                    stk_top -= 1
                elif j == stk_bottom + 1:
                    stk_bottom += 1
                assert j - stk_bottom == 0 or j - stk_bottom - 1 == 0
            if j == stk_bottom + 1:
                break
    return stk_arr[stk_bottom : stk_top + 1]