# Created by Minbiao Han and Roman Sharykin
# AI fall 2018
'''
Links used: https://www.redblobgames.com/pathfinding/a-star/implementation.html
http://interactivepython.org/courselib/static/pythonds/BasicDS/ImplementingaQueueinPython.html
'''
import collections
import os
import heapq

#Used generic PriorityQueue class from geeksforgeeks website, used this to develop this class used in the function
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def search(maze, start, end):
    goal = end

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    path = []
    num_nodes_expanded = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        adjacent = neighbors(maze, current)

        for next in adjacent:
            new_cost = cost_so_far[current] + heuristic(current, next)

            if (next not in cost_so_far) or (new_cost < cost_so_far[next]):
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
                num_nodes_expanded +=1

    current = end
    while (current != start):
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()

    return path, num_nodes_expanded


def neighbors(maze, front):
    x = front[0]
    y = front[1]

    results = []
    if (maze[x + 1][y] != "%" and (x + 1) <= len(maze)):
        results.append((x+1, y))

    # check if (x, y+1) = valid
    if (maze[x][y + 1] != "%" and (y + 1) <= len(maze[0])):
        results.append((x, y+1))

    # check if (x-1, y) = valid
    if (maze[x - 1][y] != "%" and 0 < (x - 1) <= len(maze)):
        results.append((x-1, y))

    if (maze[x][y - 1] != "%" and 0 < (y - 1) <= len(maze[0])):
        results.append((x, y-1))
    return results


def heuristic(goal, next):
    return (abs(goal[0] - next[0]) + abs(goal[1] - next[1]))

# def getLayout(name):
#     matrix = tryToLoad("layouts/" + name)
#     return matrix
#
# def tryToLoad(fullname):
#     if (not os.path.exists(fullname)): return None
#     f = open(fullname)
#     Matrix = [line.strip() for line in f]
#     f.close()
#     return Matrix
#
# level_mat = getLayout("smallMaze" + ".lay")
# print(search(level_mat, (3,11), (8,1)))
# #print(search(level_mat, (1,34), (16,1)))
# #print(search(level_mat, (35,35), (35,1)))