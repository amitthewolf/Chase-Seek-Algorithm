import pygame as pg
import math
from queue import PriorityQueue
import time


Width = 800
ExpandedAstar = []
GeneratedAstar = []
ExpandedAstarC = 0
GeneratedAstarC = 0


pg.init()
Win = pg.display.set_mode((Width,Width))
pg.display.set_caption("Search Problem Solver")
font = pg.font.SysFont(None,85)
ButtonFont = pg.font.SysFont(None,85)
fontSmall = pg.font.SysFont(None,50)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQ = (64,224,208)

class Node:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def getPosition(self):
        return self.row,self.col

    def isClosed(self):
        return self.color == RED

    def isOpen(self):
        return self.color == GREEN

    def isBarrier(self):
        return self.color == BLACK

    def isStart(self):
        return self.color == ORANGE

    def isPath(self):
        return self.color == PURPLE

    def isEnd(self):
        return self.color == TURQ

    def makeClosed(self):
        self.color = RED

    def makeOpen(self):
        self.color = GREEN

    def makePath(self):
        self.color = PURPLE

    def makeBarrier(self):
        self.color = BLACK

    def makeStart(self):
        self.color = ORANGE

    def makeEnd(self):
        self.color = TURQ

    def reset(self):
        self.color = WHITE

    def draw(self,win):
        pg.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def updateNeighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].isBarrier(): #down
            self.neighbors.append(grid[self.row+1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier(): #up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].isBarrier(): #right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].isBarrier(): #left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2)+abs(y1-y2)

def makeGrid(rows, width):
    grid = []
    gap = width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            newNode = Node(i,j,gap,rows)
            grid[i].append(newNode)
    return grid

def resetGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            currNode = grid[i][j]
            if currNode.isOpen() or currNode.isClosed() or currNode.isPath():
                currNode.reset()
            if currNode.isStart():
                currNode.makeStart()
            if currNode.isEnd():
                currNode.makeEnd()
    return grid

def drawGrid(win,rows,width):
    Gap = width//rows
    for i in range(rows):
        pg.draw.line(win,GREY,(0,i*Gap),(width,i*Gap))
        for j in range(rows):
            pg.draw.line(win, GREY, (j * Gap, 0), ( j * Gap,width))


def draw(win,grid,rows,width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    drawGrid(win, rows, width)
    pg.display.update()


def getClickPosition(pos,rows,width):
    gap = width//rows
    y,x = pos
    row = y // gap
    col = x // gap
    return row,col


def reconstructPath(cameFrom, current, draw):
    while current in cameFrom:
        current = cameFrom[current]
        if not current.isStart():
            current.makePath()
    draw()


#A*
def algorithm(draw, grid, start, end):
    count = 0
    Expanded = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    cameFrom = {}
    gScore = { spot: float("inf") for row in grid for spot in row}
    gScore[start] = 0
    fScore = {spot: float("inf") for row in grid for spot in row}
    fScore[start] = h(start.getPosition(),end.getPosition())
    openSetHash = {start}

    while not openSet.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    return False
        current = openSet.get()[2]
        openSetHash.remove(current)
        Expanded += 1
        if current == end:
            reconstructPath(cameFrom, end, draw)
            current.makeEnd()
            print("A* Expanded ",Expanded," nodes")
            return True
        for neighbor in current.neighbors:
            tempGScore = gScore[current]+1
            if tempGScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tempGScore
                fScore[neighbor] = tempGScore + h(neighbor.getPosition(),end.getPosition())
                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((fScore[neighbor],count,neighbor))
                    openSetHash.add(neighbor)
                    neighbor.makeOpen()
        if current != start:
            current.makeClosed()
        # draw()
    return False

def weighted(draw, grid, start, end):
    count = 0
    Expanded = 0
    openSet = PriorityQueue()
    openSet.put((h(start.getPosition(),end.getPosition()),0, count, start))
    cameFrom = {}
    gScore = { spot: float("inf") for row in grid for spot in row}
    gScore[start] = 0
    fScore = {spot: float("inf") for row in grid for spot in row}
    fScore[start] = h(start.getPosition(),end.getPosition())
    openSetHash = {start}

    while not openSet.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    return False
        current = openSet.get()[3]
        openSetHash.remove(current)
        Expanded += 1
        if current == end:
            reconstructPath(cameFrom, end, draw)
            current.makeEnd()
            print("A* Expanded ",Expanded," nodes")
            return True
        for neighbor in current.neighbors:
            if not neighbor.isClosed():
                tempGScore = gScore[current]+1
                if tempGScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tempGScore
                    fScore[neighbor] = h(neighbor.getPosition(),end.getPosition())
                    if neighbor not in openSetHash:
                        count += 1
                        openSet.put((fScore[neighbor],gScore[neighbor],count,neighbor))
                        openSetHash.add(neighbor)
                        neighbor.makeOpen()
        # draw()
        if current != start:
            current.makeClosed()
    return False

def MakeBarriers(grid):
    Rows = len(grid)
    for i in range(0,int(Rows-(Rows/5))):
        grid[int(Rows/5)][i].makeBarrier()
        grid[int(2*Rows/5)][i].makeBarrier()
        grid[int(3*Rows/5)][i].makeBarrier()

    for i in range(20,Rows):
        grid[int(5+Rows-(Rows/5))][i].makeBarrier()
        grid[int(5+Rows-(2*Rows/5))][i].makeBarrier()
        grid[int(5+Rows-(3*Rows/5))][i].makeBarrier()


def RemoveFromQueue(Queue,ItemToRemove,fScore,Counts):
    curr = Queue.get()[2]
    Temparr = []
    while curr != ItemToRemove:
        Temparr.append(curr)
        curr = Queue.get()[2]
    for item in Temparr:
        Queue.put((fScore[item], Counts[item], item))
    return Queue


def WolfMarch(draw, grid, start, end):
    count = 0
    Expanded = 0
    FrontierSet = PriorityQueue()
    FrontierSet.put((0, count, start))
    PerimeterSet = PriorityQueue()
    cameFrom = {}
    Counts = {}
    gScore = { spot: float("inf") for row in grid for spot in row}
    gScore[start] = 0
    fScore = {spot: float("inf") for row in grid for spot in row}
    fScore[start] = h(start.getPosition(),end.getPosition())
    hscore = {spot: float("inf") for row in grid for spot in row}
    hscore[start] = h(start.getPosition(), end.getPosition())
    FrontierSetHash = {start}
    PerimeterSetHash = {start}

    while not FrontierSet.empty() or not PerimeterSet.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    return False
        if not FrontierSet.empty():
            current = FrontierSet.get()[2]
            FrontierSetHash.remove(current)
        else:
            current = PerimeterSet.get()[2]
            # while current in FrontierSetHash:
            #     current = PerimeterSet.get()[2]
            PerimeterSetHash.remove(current)
        Expanded += 1
        if current == end:
            reconstructPath(cameFrom, end, draw)
            current.makeEnd()
            print("WolfMarch Expanded ", Expanded, " nodes")
            return True
        for neighbor in current.neighbors:
            tempGScore = gScore[current]+1
            if tempGScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tempGScore
                hscore[neighbor] = h(neighbor.getPosition(),end.getPosition())
                fScore[neighbor] = tempGScore + h(neighbor.getPosition(),end.getPosition())
                if not neighbor in Counts:
                    count += 1
                    Counts[neighbor] = count
                if hscore[neighbor] < hscore[current]:
                    if neighbor not in FrontierSetHash:
                        if neighbor in PerimeterSetHash:
                            PerimeterSetHash.remove(neighbor)
                            PerimeterSet = RemoveFromQueue(PerimeterSet,neighbor,fScore,Counts)
                        # count+1
                        # Counts[neighbor] = count
                        FrontierSet.put((hscore[neighbor],Counts[neighbor],neighbor))
                        FrontierSetHash.add(neighbor)
                        neighbor.makeOpen()
                else:
                    if neighbor not in PerimeterSetHash and neighbor not in FrontierSetHash:
                        # count += 1
                        PerimeterSet.put((fScore[neighbor], Counts[neighbor], neighbor))
                        PerimeterSetHash.add(neighbor)
                        neighbor.makeOpen()
        # draw()
        if current != start:
            current.makeClosed()
    return False


# your code here
#A*
def Heuristic(draw, grid, start, end):
    count = 0
    Expanded = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    cameFrom = {}
    gScore = { spot: float("inf") for row in grid for spot in row}
    gScore[start] = 0
    fScore = {spot: float("inf") for row in grid for spot in row}
    fScore[start] = h(start.getPosition(),end.getPosition())
    openSetHash = {start}

    while not openSet.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
        current = openSet.get()[2]
        openSetHash.remove(current)
        Expanded += 1
        if current == end:
            reconstructPath(cameFrom, end, draw)
            current.makeEnd()
            print("Heuristic Expanded ", Expanded, " nodes")
            return True
        for neighbor in current.neighbors:
            tempGScore = gScore[current]+1
            if tempGScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tempGScore
                fScore[neighbor] = h(neighbor.getPosition(),end.getPosition())
                if neighbor not in openSetHash and not neighbor.isClosed():
                    count += 1
                    openSet.put((fScore[neighbor],count,neighbor))
                    openSetHash.add(neighbor)
                    neighbor.makeOpen()
        # draw()
        if current != start:
            current.makeClosed()
    return False

def MainMenu():
    click = False
    while True:

        Win.fill(BLACK)
        textOBJ = font.render('Main Menu',1,WHITE)
        textrect = textOBJ.get_rect()
        textrect.topleft = (240,10)
        Win.blit(textOBJ,textrect)

        mx,my = pg.mouse.get_pos()

        button1 = pg.Rect(300, 525, 200, 50)
        button2 = pg.Rect(300, 675, 200, 50)
        StartTextrect = textOBJ.get_rect()
        StartTextrect.topleft = (300, 400)



        #A* Circle
        Astar = fontSmall.render('A* - \'Space\'', 1, WHITE)
        Astarect = Astar.get_rect()
        Astarect.topleft = (60, 100)
        Win.blit(Astar, Astarect)


        # IDA* Circle
        Astar = fontSmall.render('Heuristic - \'h\'', 1, WHITE)
        Astarect = Astar.get_rect()
        Astarect.topleft = (60, 140)
        Win.blit(Astar, Astarect)

        # IDA* Circle
        Astar = fontSmall.render('Chase & Seek - \'w\'', 1, WHITE)
        Astarect = Astar.get_rect()
        Astarect.topleft = (60, 180)
        Win.blit(Astar, Astarect)

        # IDA* Circle
        Astar = fontSmall.render('Stop Algorithm - \'s\'', 1, WHITE)
        Astarect = Astar.get_rect()
        Astarect.topleft = (450, 100)
        Win.blit(Astar, Astarect)

        # IDA* Circle
        Astar = fontSmall.render('Reset Graph - \'r\'', 1, WHITE)
        Astarect = Astar.get_rect()
        Astarect.topleft = (450, 140)
        Win.blit(Astar, Astarect)

        # IDA* Circle
        Astar = fontSmall.render('Clean Graph - \'c\'', 1, WHITE)
        Astarect = Astar.get_rect()
        Astarect.topleft = (450, 180)
        Win.blit(Astar, Astarect)

        # IDA* Circle
        Astar = fontSmall.render('Start by creating a start and end node by ', 1, WHITE)
        Astarect = Astar.get_rect()
        Astarect.topleft = (50, 250)
        Win.blit(Astar, Astarect)

        # IDA* Circle
        Astar = fontSmall.render('clicking the left mouse button on nodes.',
                                 1, WHITE)
        Astarect = Astar.get_rect()
        Astarect.topleft = (50, 290)
        Win.blit(Astar, Astarect)

        # IDA* Circle
        Astar = fontSmall.render('Then click on nodes to make them barriers.',
                                 1, WHITE)
        Astarect = Astar.get_rect()
        Astarect.topleft = (50, 330)
        Win.blit(Astar, Astarect)

        # IDA* Circle
        Astar = fontSmall.render('Right click on nodes to reset them.',
                                 1, WHITE)
        Astarect = Astar.get_rect()
        Astarect.topleft = (50, 370)
        Win.blit(Astar, Astarect)



        pg.draw.rect(Win,WHITE,button1)
        Astar = font.render('Start', 1, BLACK)
        Astarect = Astar.get_rect()
        Astarect.topleft = (330, 524)
        Win.blit(Astar, Astarect)
        pg.draw.rect(Win,WHITE,button2)
        Astar = font.render('Exit', 1, BLACK)
        Astarect = Astar.get_rect()
        Astarect.topleft = (343, 674)
        Win.blit(Astar, Astarect)

        if button1.collidepoint(mx,my):
            if click:
                return
        if button1.collidepoint(mx, my):
            if click:
                return

        click = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pg.display.update()

def main(win,width):
    MainMenu()
    ROWS = 100
    grid = makeGrid(ROWS,width)
    start = None
    end = None
    run = True
    started = False
    while run:
        draw(win,grid,ROWS,width)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if started:
                continue
            if pg.mouse.get_pressed()[0]: #left
                pos = pg.mouse.get_pos()
                row, col = getClickPosition(pos,ROWS,width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.makeStart()
                elif not end and spot != start:
                    end = spot
                    end.makeEnd()
                elif spot != end and spot != start:
                    spot.makeBarrier()
            elif pg.mouse.get_pressed()[2]: #right
                pos = pg.mouse.get_pos()
                row, col = getClickPosition(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.updateNeighbors(grid)
                    starttime = time.process_time()
                    algorithm(lambda : draw(win,grid,ROWS,width), grid, start, end)
                    print(time.process_time() - starttime)
                if event.key == pg.K_w and not started:
                    for row in grid:
                        for spot in row:
                            spot.updateNeighbors(grid)
                    starttime = time.process_time()
                    WolfMarch(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    print(time.process_time() - starttime)
                if event.key == pg.K_h:
                    for row in grid:
                        for spot in row:
                            spot.updateNeighbors(grid)
                    starttime = time.process_time()
                    Heuristic(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    print(time.process_time() - starttime)
                if event.key == pg.K_e:
                    for row in grid:
                        for spot in row:
                            spot.updateNeighbors(grid)
                    weighted(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pg.K_b:
                    MakeBarriers(grid)
                if event.key == pg.K_c:
                    start = None
                    end = None
                    grid = makeGrid(ROWS,width)
                if event.key == pg.K_r:
                    grid = resetGrid(grid)

    pg.quit()


main(Win,Width)