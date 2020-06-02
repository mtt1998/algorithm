from util import *
EPS = 1e-8

class AstarSolver:
    def __init__(self, problem):
        self.problem = problem
        # self.cur_node = None
        self.reset()
        return
    
    def reset(self):
        # self.cur_node = None
        self.open_nodes = MinHeap()
        self.close_nodes = {} #pos : node
        #unexplored: 0, open: 1 close: 2
        self.visited = defaultdict(int)
        sind = self.problem.graph.map[self.problem.st]
        if sind < 0:
            #障碍
            return
        self._add_state(self.problem.st, self.problem.graph.costs[sind], None)
        return
        
    def _add_state(self, cur_pos, gval, pre_pos):
        gid = self.visited[cur_pos]
        if gid == 0: #unexplored nodes, add to open list
            self.open_nodes.add(Node(cur_pos, gval, self.problem.get_h(cur_pos), pre_pos))
            self.visited[cur_pos] = 1
        elif gid == 1: #open list
            node = self.open_nodes.update(cur_pos, gval, pre_pos)
        else: #closed list 一定不会被更新 如果是consistent heuristic
#             print(cur_pos, self.close_nodes[cur_pos].gval, self.close_nodes[cur_pos].pre_pos, " compare with ", gval, pre_pos)
            assert self.close_nodes[cur_pos].gval < gval + EPS
    
    def _step(self):
        #取出最小的，加入close list, 如果不是goal, 扩展
        assert self.open_nodes.check()
        node = self.open_nodes.pop()

        self.close_nodes[node.pos] = node
        self.visited[node.pos] = 2
        if node.pos != self.problem.goal:
            moves = self.problem.get_next_states(node.pos)
            for nxt_pos, cost in moves:
                self._add_state(nxt_pos, node.gval + cost, node.pos)
        return node
    
    def get_opt_path(self, cur_pos):
        #optimal path这些点都在closed list里
        path_stk = []
        while cur_pos is not None:
            path_stk.append(cur_pos)
            cur_pos = self.close_nodes[cur_pos].pre_pos
        return list(reversed(path_stk))

    def solve(self):
        self.reset()
        #只要有点可以explore就继续
        while len(self.open_nodes) > 0:
            node = self._step()
            #输出最优路径
            if node.pos == self.problem.goal:
                return self.get_opt_path(self.problem.goal)
        return False #不能到底目标
    
    def get_opt_cost(self):
        return self.close_nodes[self.problem.goal].gval
    
class BiAstarSolver:
    def __init__(self, problem):
        self.fwd_solver = AstarSolver(problem)
        self.bwd_solver = AstarSolver(Problem(problem.graph, problem.goal, problem.st))
        self.best_cost = float("inf")
        self.pass_pos = None
        self.cur_turn = 0
        
    def reset(self):
        self.cur_turn = 0
        self.fwd_solver.reset()
        self.bwd_solver.reset()
        self.best_cost = float("inf")
        self.pass_pos = None
        
    def get_opt_path(self):
        fwd_path = self.fwd_solver.get_opt_path(self.pass_pos) # start=>pass_pos
        bwd_path = self.bwd_solver.get_opt_path(self.pass_pos)
        return fwd_path + list(reversed(bwd_path))[1:]
    
    def get_opt_cost(self):
        return self.best_cost
    
    def _step(self):
        #选择open_set小的进行扩展
        l1 = len(self.fwd_solver.open_nodes)
        l2 = len(self.bwd_solver.open_nodes)
        if(l1 < l2) or (l1 == l2 and self.cur_turn == 0):
            node = self.fwd_solver._step()
            sind = self.fwd_solver.problem.graph.map[node.pos]
            if self.bwd_solver.visited[node.pos] == 2: #in closed list
                cost = node.gval + self.bwd_solver.close_nodes[node.pos].gval - self.fwd_solver.problem.graph.costs[sind]
                if cost < self.best_cost:
                    self.best_cost = cost
                    self.pass_pos = node.pos
            self.cur_turn = 1
        else:
            node = self.bwd_solver._step()
            sind = self.fwd_solver.problem.graph.map[node.pos]
            if self.fwd_solver.visited[node.pos] == 2: #in closed list
                cost = node.gval + self.fwd_solver.close_nodes[node.pos].gval - self.fwd_solver.problem.graph.costs[sind]
                if cost < self.best_cost:
                    self.best_cost = cost
                    self.pass_pos = node.pos  
            self.cur_turn = 0       
        return node
    
    def solve(self):
        #如果有一个为0说明已经找到了最短路或者没有路
        minF = -1
        while len(self.fwd_solver.open_nodes) > 0 and len(self.bwd_solver.open_nodes) > 0:
            #node.fval <= 之后扩展到的点f <= 经过之后扩展到的点(s,t) path价值
            node = self._step()
            if node.fval > minF:
                minF = node.fval
            if self.best_cost <= minF:
                print(self.pass_pos)
                return self.get_opt_path()
        return False
                
    def plot(self):
        return