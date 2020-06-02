from collections import defaultdict
import math
EPS = 1e-8


class Node:
    def __init__(self, pos, gval, hval, pre_pos):
        self.fval = gval + hval
        self.gval = gval
        self.hval = hval
        self.pos = pos
        self.pre_pos = pre_pos
        
    def updateG(self, gval, pre_pos):
        self.gval = gval
        self.fval = self.gval + self.hval
        self.pre_pos = pre_pos
        

class MinHeap:
    #按照f(n)排序
    def __init__(self):
        self.heap = []
        self.pos2id = {}
        self.size = 0
        
    def __len__(self):
        return self.size
    
    def __iter__(self):
        self.iter = 0
        return self
    
    def __next__(self):
        if self.iter >= self.size:
            raise StopIteration()
        else:
            x = self.heap[self.iter]
            self.iter += 1
            return x
        
    def check(self):
        valid = True
        for i in range(1, self.size):
            if self.heap[0].fval < self.heap[i].fval + EPS:
                continue
            valid = False
            break
        return valid
            
    def _swap(self, ind1, ind2):   
        tmp = self.heap[ind1]
        self.heap[ind1] = self.heap[ind2]
        self.heap[ind2] = tmp
        self.pos2id[self.heap[ind1].pos] = ind1
        self.pos2id[self.heap[ind2].pos] = ind2
        
    def _shiftup(self, index):
        while index > 0:
            pid = (index - 1) // 2 #parent i, left node i * 2 + 1, right node i * 2 + 2  
            if self.heap[pid].fval > self.heap[index].fval:
                self._swap(pid, index)
                index = pid
            else:
                break
                
    def _shiftdown(self, index):
        while index * 2 + 1 < self.size:
            left = index * 2 + 1
            right = index * 2 + 2
            minchild = left
            if right < self.size and self.heap[right].fval < self.heap[left].fval:
                minchild = right
            if self.heap[index].fval > self.heap[minchild].fval:
                self._swap(index, minchild)
                index = minchild
            else:
                break
                
    def pop(self):
        if self.size == 0:
            return None
        min_node = self.heap[0]
        del self.pos2id[min_node.pos]
        last_node = self.heap.pop()
        self.size -= 1
        if self.size > 0:
            self.heap[0] = last_node
            self.pos2id[last_node.pos] = 0
            self._shiftdown(0)
        return min_node
        
    def add(self, node):
        self.heap.append(node)
        self.size += 1
        self.pos2id[node.pos] = self.size - 1
        self._shiftup(self.size - 1)
        
    def update(self, cur_pos, gval, pre_pos):
        index = self.pos2id.get(cur_pos, -1)
        assert index != -1
        if self.heap[index].gval > gval:
            self.heap[index].updateG(gval, pre_pos)
            #f(n)变小了 上浮
            self._shiftup(index)
        
    def getbypos(self, cur_pos):
        index = self.pos2id.get(cur_pos, -1)
        if index < 0:
            return None
        return self.heap[index]
    
    def touchMin(self):
        return self.heap[0]

class Graph:
    def __init__(self, N=3, M=3):
        #N行M列
        #0正常普通格子(默认),1黄色格子，2蓝色格子，-1障碍
        self.rows = N
        self.cols = M
        self.map = defaultdict(int)
        self.costs = [0, 4, 2]
        

    def load_map(self, file):
        first_line = True
        import numpy as np
        
        with open(file, mode="r", encoding="utf-8") as fp:
            tmp = np.loadtxt(fp, delimiter=',')
        self.rows = tmp.shape[0]
        self.cols = tmp.shape[1]
        for i in range(self.rows):
            for j in range(self.cols):
                sind = int(tmp[i, j])
                if sind == 0:
                    self.map[(i, j)] = 0
                elif sind == 1:
                    self.map[(i, j)] = -1
                elif sind == 4:
                    self.map[(i, j)] = 1
                elif sind == 2:
                    self.map[(i, j)] = 2
    
class Problem:
    def __init__(self, graph, st, goal):
        self.graph = graph
        self.actions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.action_costs = [1, 1, 1, 1, math.sqrt(2), math.sqrt(2), math.sqrt(2), math.sqrt(2)]
        self.st = st
        self.goal = goal
        
    #返回当前状态合法的(action, cost=action_cost+state_cost) pair
    def get_next_states(self, cur_state):
        ans = []
        for i in range(len(self.actions)):
            a = self.actions[i]
            nxt_state = (cur_state[0] + a[0], cur_state[1] + a[1])
            #越界 不合法
            if (nxt_state[0] < 0) or (nxt_state[0] >= self.graph.rows) or (nxt_state[1] < 0) \
                or (nxt_state[1] >= self.graph.cols):
                continue
            sind = self.graph.map[nxt_state]
            #障碍 不合法
            if sind < 0:
                continue
            ans.append((nxt_state, self.graph.costs[sind] + self.action_costs[i]))
        return ans
            
    def get_h(self, cur_state):
        dx = abs(self.goal[0] - cur_state[0])
        dy = abs(self.goal[1] - cur_state[1])
        # h = math.sqrt(dx * dx + dy * dy), 都满足满足三角不等式 cost(u,v) + h(v) >= h(u)
        r = min(dx, dy)
        h = math.sqrt(2) * r + max(dx, dy) - r
        return h
    
    def show(self):
        return