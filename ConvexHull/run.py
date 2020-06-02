from util import *
from BruteForce import *
from divideConquer import *
from Graham import *

import time



def plotTimeCurve():
    maxN = 2500
    allTime = [[0], [0], [0]]
    for N in range(500, maxN, 500):
        Q = random_points(100, N)
        t1 = time.time()
        CH1 = bruteForce2(Q)
        t2 = time.time()
        CH2 = GrahamScan(Q)
        t3 = time.time()
        CH3 = mergeGS(Q)
        t4 = time.time()
        allTime[0].append(t2-t1)
        allTime[1].append(t3-t2)
        allTime[2].append(t4-t3)
        print("time {} {} {}".format(t2-t1, t3-t2, t4-t3))
        print("len {} {} {}".format(len(CH1), len(CH2), len(CH3)))

    before = [0, 0, 0]
    plt.figure()
    i = 0
    x_input = list(range(0, maxN, 500))
    plt.plot(x_input, allTime[0], color='red', label='BruteForce')
    plt.plot(x_input, allTime[1], color='green', label="GrahamScan")
    plt.plot(x_input, allTime[2], color='blue', label="Divide and Conquer")


    plt.legend()
    plt.show()

def showAlgo():
    # Q = [(0,0),(1,0.5),(-0.5,-1),(1.5,-1.5)] 
    # Q = [(0,0),(1,0.5),(-0.5,-1)]
    # Q = [[3,0],[4,0],[5,0],[6,1],[7,2],[7,3],[7,4],[6,5],[5,5],[4,5],[3,5],[2,5],[1,4],[1,3],[1,2],[2,1],[4,2],[0,3]]
    Q = random_points(100, 50)
    CH1 = bruteForce2(Q)
    plotCH(Q, CH1)
    CH2 = GrahamScan(Q)
    plotCH(Q, CH2)
    CH3 = mergeGS(Q)
    plotCH(Q, CH3)
    print(len(CH1), len(CH2), len(CH3))

showAlgo()