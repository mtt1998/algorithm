from util import *

def bruteForce(Q):
    N = len(Q)
    del_flag = [False] * N
    for pid in range(N):
        for i in range(N):
            if del_flag[pid]:
                break
            if (i == pid) or del_flag[i]:
                continue
            for j in range(i + 1, N):
                if del_flag[pid]:
                    break
                if (j == pid) or del_flag[j]:
                    continue
                for k in range(j + 1, N):
                    if (k == pid) or del_flag[k]:
                        continue
                    if isInside(Q[pid], Q[i], Q[j], Q[k]):
                        del_flag[pid] = True
                        break
        ans = [Q[i] for i in range(N) if not del_flag[i]]
    return sort_theta(ans, ans[0])

def bruteForce2(Q):
    N = len(Q)
    ans = []
    isConvex = [False] * N
    for pid in range(N):
        for j in range(pid + 1, N):
            side = None
            flag = True
            for k in range(N):
                if (k == pid) or (k == j):
                    continue
                cur_side = left_rotate(Q[pid], Q[j], Q[k])
                if side is None:
                    side = cur_side
                if cur_side == 0:
                    if isInseg(Q[k], Q[pid], Q[j]):
                        continue
                    else:
                        flag = False
                        break
                elif cur_side == side:
                    continue
                else:
                    flag = False
                    break
            if flag:
                if(not isConvex[j]):
                    ans.append(Q[j])
                if(not isConvex[pid]):
                    ans.append(Q[pid])
                isConvex[j] = True
                isConvex[pid] = True
                
    return sort_theta(ans, ans[0])