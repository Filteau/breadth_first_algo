import curses
from curses import wrapper
import queue
import time

######################################################
# Breadth First Search Algorithm                     #                
# 1. Create a queue                                  #          
# 2. Enqueue the starting node                       #
# 3. While the queue is not empty:                   #
#   3.1 Dequeue a node                               #
#   3.2 If the node is the goal node, return success #
#   3.3 Otherwise, enqueue any successors            #
# 4. Return failure                                  #
######################################################

##############################################################################
# the way this works is the starting node "O" is thrown into the queue       #
# then the node is checking nearby nodes to see if they are the goal node "X"#
# if the nearest nodes are blank spaces then they are thrown into the queue  #
# if the nearest nodes are walls then they are not thrown into the queue     #
# when the node has been checked it will be put into a list of checked nodes #
# if the nearest node is the goal node "X" then the program ends             #
##############################################################################


maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["O", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", "#", "#", " ", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", "#", " ", "#"],
    ["#", "#", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", "#", " ", " ", " ", "#"],
    ["#", " ", "#", "#", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "X"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#"]
]


def print_maze(stdscr, maze, path=[]):
    GREEN = curses.color_pair(1)
    RED = curses.color_pair(3)

    for i, row in enumerate(maze): # iterating through rows and cols of maze
        for j, value in enumerate(row):
            if (i,j) in path:
                stdscr.addstr(i,j, "X", RED)
            else:
                stdscr.addstr(i,j,value, GREEN)
                
# need to find the start first
def startfinder(maze, start):
    for i, row in enumerate(maze): # iterating through rows and cols of maze
        for j, value in enumerate(row):
            if value == start: # if the value is the start value then return the position
                return (i,j)
    return None


# pathfinding algorithm
def pathfinder(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = startfinder(maze, start) # call the startfinder function

    q = queue.Queue() # create a queue - we want to process by 
    q.put((start_pos, [start_pos])) # put the start position in the queue

    visited = set() # create a set of visited nodes

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        stdscr.clear()
        print_maze(stdscr, maze, path)
        stdscr.refresh()

        if maze[row][col] == end: # if the end is found then return the path
            return path
        
        neighbors = find_neighbors(maze, row, col) # find the neighbors of the current position
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            row, col = neighbor
            if maze[row][col] == "#":
                continue

            new_path = path + [neighbor]    # add the neighbor to the path
            q.put((neighbor, new_path))
            visited.add(neighbor)


def find_neighbors(maze, row, col): # does not check for obstacles

    neighbors = []

    if row > 0:         # if row is 0, we are at the top boundary of the maze --------- UPWARDS
        neighbors.append((row-1, col))

    if row + 1 < len(maze):     # if row is the last row, we are at the lower bounds of the maze --------- DOWNWARDS
        neighbors.append((row+1, col))

    if col > 0:         # if col is 0, we are at the left bounds of the maze --------- LEFTWARDS
        neighbors.append((row, col-1))

    if col + 1 < len(maze[0]):  # if col is the last col, we are at the right bounds of the maze --------- RIGHTWARDS
        neighbors.append((row, col+1))  # maze is using [0] ----- maze must have an upper boundary else this part will not work
    
    return neighbors

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # 1 is the pair number, green is foreground, black is background
    color_pair_1 = curses.color_pair(1) #use ID of color pair you want to use (1 in this case)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    path = pathfinder(maze, stdscr) # store the returned path
    print_maze(stdscr, maze, path) # print the maze with the path
    stdscr.refresh()
    stdscr.getch()

wrapper(main)

