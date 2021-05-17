import cv2
import numpy as np
import time
import math

# class object point for each point in matrix
class Point:
    def __init__(self, x_coor = 0, y_coor = 0):
        self.x = x_coor
        self.y = y_coor
        self.distance = float('inf')
        self.prev_x = None
        self.prev_y = None
        self.visited = False
    def __lt__(self, other):
        return (self.x < other.x)
    def __gt__(self, other):
        return (self.x > other.x)
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

start_color = [113,204,45]  # [B, G, R]
end_color = [60,76,231]
visit = [117, 34, 33]
popped = [100, 100, 33]
white = [255,255,255]
black = [0,0,0]
start_to_end = [117, 255, 100]

img = cv2.imread('./Images/Task_1_Low_Empty.png',cv2.IMREAD_COLOR)
try:
    l, w, t = img.shape
    print("Image has been read")
    print("Height Width = ", l, w)
except:
    print("Problem in image reading. Try again in ./Images directory")

# Search for start and end coordinates
switch1 = True
switch2 = True
for i in range(l):
    for j in range(w):
        if switch1:
            if (img[i,j] == start_color).all():
                start = (i,j)
                switch1 = False
        if switch2:
            if (img[i,j] == end_color).all():
                end = (i,j)
                switch2 = False

print("Source = ", start)
print("Destination = ", end)
start = Point(start[1],start[0])
end = Point(end[1], end[0])

case = int(input("Case 1 or Case 2 ? (Enter 1 or 2):"))

# check if a point can be visited
def is_ok(img, matrix, x, y):
    h, w = matrix.shape
    return (x < w and x >= 0 and y < h and y >= 0 and matrix[y][x].visited == False and (img[(y,x)] != white).all())

# Returning neighbours of current point
def pop_element_adj(case, img, matrix, Point):
    adj = []
    x = Point.x
    y = Point.y
    if(is_ok(img, matrix, x - 1, y)): adj.append((matrix[y][x-1]))
    if(is_ok(img, matrix, x + 1, y)): adj.append((matrix[y][x+1]))
    if(is_ok(img, matrix, x, y-1)): adj.append((matrix[y-1][x]))
    if(is_ok(img, matrix, x, y+1)): adj.append((matrix[y+1][x]))
    if case == 2:
        if(is_ok(img, matrix, x - 1, y - 1)): adj.append((matrix[y-1][x-1]))
        if(is_ok(img, matrix, x + 1, y + 1)): adj.append((matrix[y+1][x+1]))
        if(is_ok(img, matrix, x - 1, y + 1)): adj.append((matrix[y+1][x-1]))
        if(is_ok(img, matrix, x + 1, y - 1)): adj.append((matrix[y-1][x + 1]))
    return adj

# Main algorithm
def dijkstra(case, img, start, end):
    l,w,t = img.shape
    found = False
    open_queue = []
    open_queue.append(start)
    start.distance = 0
    matrix = np.full((l, w), None)

    # Making a matrix full of points
    for r in range(l):
        for c in range(w):
            matrix[r][c] = Point(c,r)
    
    while len(open_queue):
        # Getting point with lowest distance in queue
        currentPoint = open_queue[0]
        current_index = 0
        for index, item in enumerate(open_queue):
            if item.distance < currentPoint.distance:
                currentPoint = item
                current_index = index
        open_queue.pop(current_index)
        img[(currentPoint.y, currentPoint.x)] = popped
        currentPoint.visited = True

        if (currentPoint.y == end.y and currentPoint.x == end.x):
            found = True
            print("Path finding complete")
            break

        for nextNode in pop_element_adj(case, img, matrix, currentPoint):
            dist = 1
            if(nextNode.y - currentPoint.y and nextNode.x - currentPoint.x): dist = 1.4
            if nextNode in open_queue:
                if currentPoint.distance + dist < nextNode.distance:
                    matrix[nextNode.y][nextNode.x].distance = currentPoint.distance + dist
                    nextNode.distance = currentPoint.distance + dist
                    open_queue.append(nextNode)
                    matrix[nextNode.y][nextNode.x].prev_x = currentPoint.x
                    matrix[nextNode.y][nextNode.x].prev_y = currentPoint.y
            else:
                matrix[nextNode.y][nextNode.x].distance = currentPoint.distance + dist
                nextNode.distance = currentPoint.distance + dist
                open_queue.append(nextNode)
                matrix[nextNode.y][nextNode.x].prev_x = currentPoint.x
                matrix[nextNode.y][nextNode.x].prev_y = currentPoint.y
            

    img[(start.y, start.x)] = start_color
    closes = time.time()
    print("Time taken = ", closes - begins)
    pathFound = []
    if found:
        # Backtracking to find the path
        Pointer = end
        while (Pointer.x != start.x or Pointer.y != start.y):
            Pointer = matrix[matrix[Pointer.y][Pointer.x].prev_y][matrix[Pointer.y][Pointer.x].prev_x]
            pathFound.append((Pointer.x, Pointer.y))
        print("Cost of Path = ", matrix[end.y][end.x].distance)
    else:
        print("Path could not be found")
    return pathFound

def showPath(img, path):
    # color coding path
    for i in path:
        img[(i[1], i[0])] = start_to_end
    img[(path[0][1], path[0][0])] = start_color
    img[(path[len(path) - 1][1], path[len(path) - 1][0])] = end_color

begins = time.time()

print("Processing ...")
path = dijkstra(case, img, start, end)

showPath(img, path)

# Upscaling each pixel as specified in statement
outpush_element_image = np.zeros((1000,1000,3), np.uint8)
for i in range(l):
    for j in range(w):
        color = img[(i,j)]
        for n in range(10):
            for m in range(10):
                outpush_element_image[i*10 + n][j*10 + m] = color
imagename = "./Output/Dijkstra" + str(case) + ".png"
cv2.imwrite(imagename, outpush_element_image)
cv2.imshow('Dijkstra', outpush_element_image)
cv2.waitKey(0)
cv2.destroyAllWindows()