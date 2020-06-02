from util import *
from search import *
from visual import *

graph = Graph()

graph.load_map("F:\\algorithm-experiments\\Astar\\hard_map.txt")
problem = Problem(graph, (10,4), (0, 35))

# graph.load_map("F:\\algorithm-experiments\\Astar\\simple_map.txt")
# problem = Problem(graph, (8,3), (9, 14))

solver = AstarSolver(problem)

root = Tk()
app = VisualSearch(root, solver, "Astar")
root.mainloop()