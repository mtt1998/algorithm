from util import *
from Graham import GrahamScan

def mergeGS(Q):
    N = len(Q)
    if N < 3:
        return Q
    #divide
    X = []
    for q in Q:
        X.append(q[0])
    #按x轴中位数划分点
    median = getKsmall(X, int((N+1)/2))
    Q1 = []
    Q2 = []
    tmp = []
    for q in Q:
        if q[0] < median:
            Q1.append(q)
        elif q[0] > median:
            Q2.append(q)
        else:
            tmp.append(q)
    k1 = int((N+1)/2) - len(Q1)  
    Q1 = Q1 + tmp[:k1]
    Q2 = Q2 + tmp[k1:]
    #分治求解子问题
    CH1 = mergeGS(Q1)
    CH2 = mergeGS(Q2)
    #Merge 
    #首先对极角排序，分成3段，每段是递增的。
    #因为p属于CH1,如果选x=p[0],y=p[1]-1作为极角的x轴，那么CH2极角范围为(0,180)度，且分两段递增
#     ind = random.randint(0, len(Q1) - 1)

    min_id1 = 0
    N1 = len(CH1)
    N2 = len(CH2)

    # p = CH1[0]
    #p属于CH1内一点，CH1的极角[0,360)度分一段递增,如果选取p在leftmost那么范围可以到[0,180]?????
    for i in range(1, N1):
        if CH1[i][0] < CH1[min_id1][0]:
            min_id1 = i
    p = CH1[min_id1]

    min_id2 = 0
    max_id2 = 0
    for i in range(1, N2):
        if comp(p, CH2[min_id2], CH2[i]) > 0: #i-1<=i
            min_id2 = i
        if comp(p, CH2[i], CH2[max_id2]) > 0:
            max_id2 = i

    
    #三段递增序列分别是 CH1: 0 to N1 CH2: [min_id2 to max_id2] +1 CH2: (min_id2 to max_id2) -1
    #Merge O(N) 三个指针 pid1, pid2, pid3; 里面包含的元素个数为cnt1, cnt2, cnt3, 排好序的数组为CH_merge
    
    pid1 = min_id1
    pid2 = min_id2
    pid3 = (min_id2 - 1 + N2) % N2 
    cnt1 = N1
    cnt2 = max_id2 - min_id2 + 1 if max_id2 >= min_id2 else N2 - min_id2 + max_id2 + 1
    cnt3 = N2 - cnt2
    
    CH_merge = []
    while (cnt1 + cnt2 + cnt3) > 0:
        key1 = CH1[pid1] if cnt1 > 0 else None
        key2 = CH2[pid2] if cnt2 > 0 else None
        key3 = CH2[pid3] if cnt3 > 0 else None
        if comp(p, key1, key2) <= 0 and comp(p, key1, key3) <= 0:
            CH_merge.append(CH1[pid1])
            cnt1 -= 1
            pid1 = (pid1 + 1) % N1
        elif comp(p, key2, key1) <= 0 and comp(p, key2, key3) <= 0:
            CH_merge.append(CH2[pid2])
            cnt2 -= 1
            pid2 = (pid2 + 1) % N2
        else:
            CH_merge.append(CH2[pid3])
            cnt3 -= 1
            pid3 = (pid3 - 1 + N2) % N2 
    CH = GrahamScan(CH_merge, False)
#     if len(Q)== 5:
#     plotCHmerge(Q1, Q2, CH1, CH2, CH,p, CH2[max_id2], CH2[min_id2], median)
    return CH



def plotCHmerge(Q1, Q2, CH1, CH2, CH_merge, basep, umax, vmin, median):
    plt.figure()
    for i in range(len(Q1)):
        q = Q1[i]
        plt.scatter(q[0], q[1], s=10, marker='o', color='green') # display all the points
    for i in range(len(Q2)):
        q = Q2[i]
        plt.scatter(q[0], q[1], s=10, marker='o', color='blue') # display all the points        
    for i in range(len(CH1)):
        p = CH1[i]
        q = CH1[(i + 1) % len(CH1)]
        plt.plot([p[0], q[0]], [p[1], q[1]], color='red') # display lines
    for i in range(len(CH2)):
        p = CH2[i]
        q = CH2[(i + 1) % len(CH2)]
        plt.plot([p[0], q[0]], [p[1], q[1]], color='red') # display lines    
    plt.plot([median,median],[0,100])

    plt.show()
        
    plt.figure()
    for i in range(len(CH_merge)):
        p = CH_merge[i]
        q = CH_merge[(i + 1) % len(CH_merge)]
        plt.plot([p[0], q[0]], [p[1], q[1]], color='yellow') # display lines   
        plt.annotate(str(i), xy=[p[0]+0.02, p[1]+0.02])
    plt.annotate("P", xy=basep) # display all the points 
    plt.annotate("Max", xy=umax)
    plt.annotate("Min", xy=vmin)
    plt.show()