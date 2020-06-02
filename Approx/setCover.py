import pulp
import random
import math
from collections import defaultdict
import itertools
import numpy as np


ESP = 1e-9

def generate_maxf(N, maxf):
    #N: 点和集合个数: 3个点0,1,2
    fcount = [0] * N
    set_lists = [set(random.sample(range(N), 20))]
    for x in set_lists[0]:
        fcount[x] += 1
    gold_num = 0
    union_points = set_lists[0]
    retain_points = set(range(N)) - union_points
    select_flag = [False] * N
    while(len(retain_points) >= 20):
        size = random.randint(1, 20) # k=>union_points n-k=>retain_points
        k = random.randint(1, size) #k个从新的point (retain)里选择
        unseen = random.sample(retain_points, k)
        seen = random.sample(union_points, size - k)
        # print(seen)
        for i in range(len(seen)):
            while fcount[seen[i]] == maxf:
                x = random.sample(union_points - set(seen), 1)[0]
                seen[i] = x
            fcount[seen[i]] += 1
        for i in range(len(unseen)):
            fcount[unseen[i]] += 1
        Si = set(unseen + seen)
        retain_points = retain_points - Si 
        union_points = union_points | Si 
        set_lists.append(Si)        
    if len(retain_points) > 0:
        set_lists.append(retain_points)
    for x in retain_points:
        fcount[x] += 1
    gold_len = len(set_lists)
    
    cur_max = max(fcount)
    if cur_max == maxf:
        max_cnt = -1
        max_num = -1
        print("satisify")
    else:
        max_num = np.argmax(fcount)
        max_cnt = maxf - cur_max
    print("gold answer is not great than ", gold_len)
    while len(set_lists) < N:
        cur_set = []
        if (max_cnt > 0):
            cur_set.append(max_num)
            fcount[max_num] += 1
            max_cnt -= 1
        
        size = random.randint(10,30)
        tmp = random.sample(range(N), size)

        for i in tmp:
            if i == max_num:
                continue
            if (fcount[i] + 1 > maxf):
                continue
            cur_set.append(i)
            fcount[i] += 1
        set_lists.append(set(cur_set))
    return set_lists


#生成可行解的集合
def generate(N):
    #N: 点和集合个数: 3个点0,1,2
    set_lists = [set(random.sample(range(N), 20))]
    gold_num = 0
    union_points = set_lists[0]
    retain_points = set(range(N)) - union_points
    select_flag = [False] * N
    while(len(retain_points) >= 20):
        size = random.randint(1, 20) # k=>union_points n-k=>retain_points
        k = random.randint(1, size) #k个从新的point (retain)里选择
        unseen = random.sample(retain_points, k)
        seen = random.sample(union_points, size - k)
        Si = set(unseen + seen)
        retain_points = retain_points - Si 
        union_points = union_points | Si 
        set_lists.append(Si)        
    if len(retain_points) > 0:
        set_lists.append(retain_points)
    gold_len = len(set_lists)
    print("gold ans is not great than ", gold_len)
    while len(set_lists) < N:
        # j = random.randint(0, gold_len - 1)
        # size = random.randint(1, len(set_lists[j]))
        # set_lists.append(set(random.sample(set_lists[j], size)))
        j = random.sample(range(len(set_lists)), 2)
        set_lists.append(set_lists[j[0]] | set_lists[j[1]])
    return set_lists

#无权,Ratio Bound是 p(n)多项式 ln N + 1, 因此理论上点数越多，可能结果越差...，另外时间复杂度为N^3
def GreedyApprox(N, set_list):
    retain_points = set(range(N))
    select_flags = [False] * len(set_list)
    select_ids = []
    while len(retain_points) > 0:
        max_id = -1
        max_cover = -1
        for i in range(len(set_list)):
            if select_flags[i]:
                continue
            cover_num = len(set_list[i] & retain_points)
            if cover_num > max_cover:
                max_cover = cover_num
                max_id = i
        select_ids.append(max_id)
        select_flags[max_id] = True
        retain_points -= set_list[max_id]
    maxS = max([len(i) for i in set_list])
    return select_ids, math.log(maxS) + 1


#每个集合可以有非负权值, x[i]=1表示选择集合i
# min w[i]x[i] s.t. 对于元素i所在的集合族f[i] sum(x) >= 1
# thredbound: 1/maxf, 不能再大了否则可能有元素没被覆盖，近似比为maxf,因此取最小为maxf
# 因此理论上maxf越大，可能结果越差...时间复杂度为p(N)
def ILPApprox(N, set_lists, weights):
    set_num = len(set_lists)
    select_ids = []
    model = pulp.LpProblem("min set cover", pulp.LpMinimize)
    x_vars = pulp.LpVariable.dicts("select x",
                                     range(set_num),
                                     lowBound=0,
                                     upBound=1,
                                     cat='Continuous')
    # Objective Function
    model += pulp.lpSum([weights[i] * x_vars[i] for i in range(set_num)])
    maxf = 1
    for elem in range(N):
        inSet = [int(elem in set_lists[j]) for j in range(set_num)]
        maxf = max(sum(inSet), maxf)
        model += pulp.lpSum([x_vars[j] * inSet[j] for j in range(set_num)]) >= 1
    model.solve()
    for i in range(set_num):
        if x_vars[i].value() > 1.0/maxf - ESP:
            select_ids.append(i)
    return select_ids, maxf

#根本没法做啊...
def bruteForce(N, set_lists):
    set_num = len(set_lists)
    select_ids = []
    inSet = [[] for i in range(set_num)]
    for i in range(set_num):
        for j in set_lists[i]:
            inSet[j].append(i)
    model = pulp.LpProblem("min set cover accurate", pulp.LpMinimize)
    # x_vars = pulp.LpVariable.dicts("select x",
    #                                  range(set_num),
    #                                  lowBound=0,
    #                                  upBound=1,
    #                                  cat='Integer')
    x_vars = [pulp.LpVariable("x-"+str(i), lowBound=0, upBound=1, cat="Integer") for i in range(set_num)]
    # Objective Function
    model += pulp.lpSum([x_vars[i] for i in range(set_num)])
    for elem in range(N):
        model += pulp.lpSum([x_vars[j] for j in inSet[elem]]) >= 1
    model.solve()
    for i in range(set_num):
        if x_vars[i].value() > 1.0 - ESP:
            select_ids.append(i)
    return select_ids

def check(N, set_lists, select_ids):
    inSet = defaultdict(int)
    for ind in select_ids:
        for x in set_lists[ind]:
            inSet[x] = 1
    for i in range(N):
        if inSet[i] == 0:
            return False
    return True


def show_res(N, set_lists, select_ids):
    print("select num ", len(select_ids))
    union_sets = set([])
    for i in select_ids:
        print_line = "set {}: ".format(i)
        newset = []
        for x in set_lists[i]:
            if x in union_sets:
                print_line += "{},".format(x)
            else:
                newset.append(x)
        print_line += " NEW :"
        for x in newset:
            print_line += "{},".format(x)
        print(print_line)
        union_sets = union_sets | set_lists[i]
    return





N = 100
set_lists = generate_maxf(N, 5)

gold_ids = bruteForce(N, set_lists)
gold_num = len(gold_ids)
print("gold ans size {}".format(gold_num))

# gold_ids = intergerProgramming(N, set_lists)
# print("gold ans size {}".format(len(gold_ids)))


greedy_ids, gratio_bound = GreedyApprox(N, set_lists)
print("greedy ratio : ", gratio_bound)
print("greedy actual ratio: ", len(greedy_ids) / gold_num)
show_res(N, set_lists, greedy_ids)

print("=" * 30)

lp_ids, lpratio_bound = ILPApprox(N, set_lists, [1] * N)
print("LP ratio : ", lpratio_bound)
print("LP actual ratio: ", len(lp_ids) / gold_num)
show_res(N, set_lists, lp_ids)

