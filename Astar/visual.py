from tkinter import (
        Tk, Canvas, Scrollbar, Text,
        TOP, BOTTOM, BOTH,
        X, Y, N, S, E, W,
        LEFT, RIGHT, RAISED,
        HORIZONTAL, VERTICAL
    )

from tkinter import Frame, Button, Label
import tkinter.font as tkFont
from search import *

import time

class VisualSearch(Frame):
    def __init__(self, parent, solver, algotype):
        super().__init__(parent)
        self.pack()

        self.solver = solver
        self.algotype = algotype
        self.parent = parent
        
        self.step_num = 0

        self.cur_node = None
        self.minF = -1
        self.startloop = True
                
        if self.algotype == "Astar":
            self.graph = self.solver.problem.graph
            self.st = self.solver.problem.st
            self.goal = self.solver.problem.goal
        else:
            self.graph = self.solver.fwd_solver.problem.graph
            self.st = self.solver.fwd_solver.problem.st
            self.goal = self.solver.fwd_solver.problem.goal

        self.parent.title(algotype)

        self.stepLabel = Label(self, text="Step: 0")
        self.stepLabel.pack(side=TOP, padx=5, pady=5)
        self.algoLabel = Label(self, text="g:  h:  f:")
        self.algoLabel.pack(side=TOP, padx=5, pady=5)

        print(self.graph.rows, self.graph.cols)
            
        self.pixel = 20
        self.canvas = Canvas(self, width=self.pixel * self.graph.cols, height=self.pixel * self.graph.rows, bg="white")
        self.canvas.pack()
        self.pos2cid = {}
        # self.canvas.pack(fill=BOTH, expand='yes')
        self.lines = []
        
        runButton = Button(self, text="Run", command=self.run)
        runButton.pack(side=LEFT, padx=5, pady=5)
        stepButton = Button(self, text="Step", command=self._step)
        stepButton.pack(side=LEFT, padx=5, pady=5)
        clearButton = Button(self, text="Reset", command=self.reset)
        clearButton.pack(side=LEFT, padx=5, pady=5)
        stopButton = Button(self, text="Stop", command=self.stop)
        stopButton.pack(side=LEFT, padx=5, pady=5)
        quitButton = Button(self, text="Quit", command=self._quit)
        quitButton.pack(side=LEFT, padx=5, pady=5)

        
        self.gid2color = {-1: "gray", 0 : "white", 1 : "Bisque", 2 : "SkyBlue"} #graph state id => color
        self.vid2color = {0: "orange", 1: "PaleVioletRed", 2: "Pink"} #search visited id => color 0:cur pos, 1: closed list, 2: open list

        self.draw_graph()
        self.draw_st()
        return

    def _quit(self):
        self.quit()
    
        
    def _step(self):
        node = self.solver._step()
        #把之前的node加入closed list颜色
        if self.cur_node:
            self.draw_node(self.cur_node.pos, self.vid2color[1])
        #保存当前状态
        self.cur_node = node
        self.step_num += 1
        self.stepLabel.configure(text="Step: " + str(self.step_num))
        if node:
            #更新f值
            if node.fval > self.minF:
                self.minF = node.fval    
            #更新当前点的颜色
            self.draw_node(node.pos, self.vid2color[0])    
            #更新当前点信息框
            self.algoLabel.configure(text="g:{:.2f}  h:{:.2f}  f:{:.2f} cur_best_cost: {:.2f}".format(node.gval, node.hval, node.fval, self.solver.best_cost))  

        #更新open list的color
        if self.algotype == "Astar":
            open_pos_list = [x.pos for x in self.solver.open_nodes]
        else:
            open_pos_list = [x.pos for x in self.solver.fwd_solver.open_nodes] + [x.pos for x in self.solver.bwd_solver.open_nodes]
        for pos in open_pos_list:
            self.draw_node(pos, self.vid2color[2])
        return node

    def loop(self):
        if not self.startloop:
            return
        millisec = 1
        if self.algotype == "Astar":
            #只要有点可以explore就继续
            if len(self.solver.open_nodes) > 0:
                node = self._step()
                #判断是否继续扩展
                if node.pos == self.goal:
                    self.draw_graph()
                    self.draw_path(self.solver.get_opt_path(self.goal))
                    self.algoLabel.configure(text="f: {:.2f} g: {:.2f} h:{:.2f} final cost: {:.2f}".format(node.fval, node.gval, node.hval, self.solver.get_opt_cost()))
                    self.startloop = False
                    return
                self.parent.after(millisec, self.loop)
            else:
                self.algoLabel.configure(text="can not find a path!") 
                self.startloop = False
        else:
            if len(self.solver.fwd_solver.open_nodes) > 0 and len(self.solver.bwd_solver.open_nodes) > 0:
                #node.fval <= 之后扩展到的点f <= 经过之后扩展到的点(s,t) path价值
                node = self._step()
                #判断是否继续扩展
                if self.solver.best_cost <= self.minF:
                    self.draw_graph()
                    self.draw_path(self.solver.get_opt_path(), self.solver.pass_pos)
                    self.algoLabel.configure(text="final cost: {:.2f}".format(self.solver.get_opt_cost()))
                    self.startloop = False
                    return
                self.parent.after(millisec, self.loop)
            else:
                self.algoLabel.configure(text="can not find a path!") 
                self.startloop = False

  
    def stop(self):
        self.startloop = False

    def run(self):
        self.startloop = True
        self.loop()
        # self.reset()
        # self.loop(cur_node = self.cur_node, minF = self.minF)
        return
        
    def draw_path(self, path, pass_node=None):
        pcolor = "red"
        pre_pixel = [(path[0][1] + 0.5) * self.pixel, (path[0][0] + 0.5) * self.pixel]
        for pos in path[1:]:
            if pos == pass_node:
                pcolor = "green"
            # cid = self.pos2cid[pos]
            # self.canvas.itemconfig(cid, fill=pcolor)
            tmp = [(pos[1] + 0.5) * self.pixel, (pos[0] + 0.5) * self.pixel]
            self.lines.append(self.canvas.create_line(pre_pixel[0], pre_pixel[1], tmp[0], tmp[1], fill=pcolor))
            pre_pixel = tmp
        
    def draw_node(self, pos, color): 
        if pos in self.pos2cid:
            cid = self.pos2cid[pos]
            self.canvas.itemconfig(cid, fill=color)
        else:
            cid = self.canvas.create_rectangle(pos[1] * self.pixel + 1,
                           pos[0] * self.pixel + 1,
                           pos[1] * self.pixel + self.pixel - 1,
                           pos[0] * self.pixel + self.pixel - 1,
                           fill=color) 
            self.pos2cid[pos] = cid
        return cid
           
    def draw_st(self):
        #draw text
        ft = tkFont.Font(size=12, weight=tkFont.BOLD)
        stText = self.canvas.create_text((self.st[1] + 0.5) * self.pixel, (self.st[0] + 0.5) * self.pixel, text="S", font=ft)
        goalText = self.canvas.create_text((self.goal[1] + 0.5) * self.pixel, (self.goal[0] + 0.5) * self.pixel, text="T", font=ft)
        self.canvas.tag_lower(self.pos2cid[self.st], stText)
        self.canvas.tag_lower(self.pos2cid[self.goal], goalText)

    def draw_graph(self):
        for i in range(self.graph.rows):
            for j in range(self.graph.cols):
                color = self.gid2color[self.graph.map[(i, j)]]
                self.draw_node((i, j), color)

    def reset(self):
        self.solver.reset()
        self.startloop = True
        self.step_num = 0  
        self.cur_node = None
        self.minF = -1
        self.stepLabel.configure(text="Step: 000")
        self.algoLabel.configure(text="g:  h:  f:")
        self.draw_graph()
        for line in self.lines:
            self.canvas.delete(line)
        return