from util import *
from search import *
from visual import *

graph = Graph()

graph.load_map("F:\\algorithm-experiments\\Astar\\hard_map.txt")
problem = Problem(graph, (10,4), (0, 35))

# graph.load_map("F:\\algorithm-experiments\\Astar\\simple_map.txt")
# problem = Problem(graph, (8,3), (9, 14))

solver2 = BiAstarSolver(problem)

root2 = Tk()
app2 = VisualSearch(root2, solver2, "BiAstar")
root2.mainloop()
