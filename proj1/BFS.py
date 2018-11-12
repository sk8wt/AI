# Created by Minbiao Han and Roman Sharykin
# AI fall 2018
import collections
import os
#Links used: https://www.redblobgames.com/pathfinding/a-star/implementation.html
#http://interactivepython.org/courselib/static/pythonds/BasicDS/ImplementingaQueueinPython.html


def search(maze, start, end):
    queue = [[start]]
    visited = set()
    path = []
    num_nodes_expanded = 0
    adjacent = []

    while len(queue) > 0:
        path = queue.pop(0)
        front = path[-1]

        if front == end:
            return path, num_nodes_expanded

        if front not in visited:
            adjacent = neighbors(maze, front, visited)

            for i in adjacent:
                new_path = path.copy()
                new_path.append(i)
                queue.append(new_path)
            visited.add(front)
            num_nodes_expanded += 1

    return path, num_nodes_expanded


### feel free to add any aditional support functions for your search here ###
#https://www.redblobgames.com/pathfinding/a-star/implementation.html

def neighbors(maze, front, visited):
    x = front[0]
    y = front[1]

    results = []
    if (maze[x + 1][y] != "%" and (x + 1) <= len(maze) and (x+1, y) not in visited):
        results.append((x+1, y))

    # check if (x, y+1) = valid
    if (maze[x][y + 1] != "%" and (y + 1) <= len(maze[0]) and (x, y+1) not in visited):
        results.append((x, y+1))

    # check if (x-1, y) = valid
    if (maze[x - 1][y] != "%" and 0 < (x - 1) <= len(maze) and (x-1, y) not in visited):
        results.append((x-1, y))

    if (maze[x][y - 1] != "%" and 0< (y - 1) <= len(maze[0]) and (x, y-1) not in visited):
        results.append((x, y-1))
    return results

# def getLayout(name):
#     matrix = tryToLoad("layouts/" + name)
#     return matrix
#
#
# def tryToLoad(fullname):
#     if (not os.path.exists(fullname)): return None
#     f = open(fullname)
#     Matrix = [line.strip() for line in f]
#     f.close()
#     return Matrix
#
#
# level_mat = getLayout("mediumMaze" + ".lay")
# #print(search(level_mat, (3,11), (8,1)))
# print(search(level_mat, (1,34), (16,1)))
# #print(search(level_mat, (35,35), (35,1)))