from snake import Snake
from constants import *
import math
import pygame

class StudentPlayer(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0), name="Jewpacabra"):
        super().__init__(body,direction,name=name)
        self.last = None
        self.temp_len_players_positions = None
        self.closedNodes = []
        self.food_found = False
        self.aa_regular_food_found=False
        self.oneTimeWasFound=False
        self.maze_obstacles = []
        self.reset = 5
        self.counter = 0
        self.path_to_food = []

    def pathlen(self,a,b):
        width=self.mapsize[0]
        heigth=self.mapsize[1]
        distX = abs(a[0]-b[0])
        distY = abs(a[1]-b[1])
        if distX > width/2:
            distX = width- distX;
        if distY > heigth/2:
            distY = heigth - distY;
        return distX + distY
    def add(self,a,b):
        width=self.mapsize[0]
        heigth=self.mapsize[1]
        return (a[0]+b[0])%width,(a[1]+b[1])%heigth
    def update(self,points=None, mapsize=None, count=None,agent_time=None):
        self.mapsize=mapsize
        self.count=count
        self.agent_time=agent_time

    def update_map(self):
        for x in range(self.mapsize[0]):
            for y in range(self.mapsize[1]):
                self.dead_end((x,y))

    def dead_end(self, pos):
        neigs = self.get_pixel_free_path(pos)
        if not len(neigs):
            self.maze_obstacles.append(pos)
            return
        if len(neigs) == 1:
            self.maze_obstacles.append(pos)
            self.dead_end(neigs[0])

    def get_pixel_free_path(self, pos):
        return [self.add(pos, dir) for dir in directions if self.add(pos, dir) not in self.maze_obstacles]

    def reset_data(self):
        self.last = None
        self.closedNodes = []
        self.food_found  = False

    def get_validirs(self, position, validdir, maze):
        enemy_pos = [pos for pos in maze.playerpos if pos not in self.body]

        if len(self.body) > len(maze.playerpos):
            direction=[dir for dir in validdir if not (self.add(position,dir) in self.maze_obstacles or self.add(position,dir) in maze.playerpos)]
        else:
            # possible enemy positions
            enemy_head = enemy_pos[0]
            possible_next_enemy_position = [self.add(enemy_head, dir) for dir in directions]
            direction=[dir for dir in validdir if not (self.add(position,dir) in self.maze_obstacles or self.add(position,dir) in maze.playerpos or self.add(position,dir) in possible_next_enemy_position)]
            if not direction:
                direction=[dir for dir in validdir if not (self.add(position,dir) in self.maze_obstacles or self.add(position,dir) in maze.playerpos)]
        if not direction:
            direction = [d for d in validdir if self.add(position, d) not in maze.obstacles]
        if not direction:
            direction = [d for d in validdir if self.add(position, d) not in maze.playerpos]
        return direction

    def updateDirection(self,maze):
        try:
            if not self.temp_len_players_positions: # only to occur at the first time
                self.maze_obstacles = maze.obstacles
                self.update_map();
                begin_time = 1000
            else:
                 begin_time = pygame.time.get_ticks();

            temp_len = self.temp_len_players_positions
            self.temp_len_players_positions = len(maze.playerpos)
            if temp_len != self.temp_len_players_positions:
                self.reset_data()

            olddir=self.direction
            position=self.body[0]

            complement=[(up,down),(down,up),(right,left),(left,right)]
            invaliddir=[x for (x,y) in complement if y==olddir]
            validdir=[dir for dir in directions if not ( dir in invaliddir )]

            validdir = self.get_validirs(position, validdir, maze)
            olddir = validdir[0] if validdir else olddir

            shortest=self.pathlen(self.add(position,olddir) , maze.foodpos)


            enemy_pos = [pos for pos in maze.playerpos if pos not in self.body]
            intersects = [a for a in self.path_to_food if a.get_pos() in [b for b in maze.playerpos if b not in self.body]]
            if intersects:
                point = intersects[0]
                if self.pathlen(enemy_pos[-1], point.get_pos()) < self.pathlen(self.body[0], point.get_pos()):
                    self.reset_data()

                self.reset_data()
            # avoid food if we are +7 larger than enemy
            if len(self.body) > (len(maze.playerpos) - len(self.body) + 6):
                vdirs = self.get_validirs(position, validdir, maze)
                dir = vdirs[0] if vdirs else olddir
                self.reset_data()
            # astar saving the path
            elif not self.food_found:
                path = self.aa_improved(position, self.direction, maze, begin_time)
                if path and path[-1].dir in validdir:
                    dir = path[-1].dir
                else:
                    vdirs = self.get_validirs(position, validdir, maze)
                    dir = vdirs[0] if vdirs else olddir
                    self.reset_data()
            # regular aastar
            else:
                path = self.aa_regular(position, self.direction, maze, begin_time)
                if self.aa_regular_food_found:
                    self.oneTimeWasFound=True
                    self.aa_regular_food_found=False
                    if path and path[-1].dir in validdir:
                        dir = path[-1].dir
                    else:
                        vdirs = self.get_validirs(position, validdir, maze)
                        dir = vdirs[0] if vdirs else olddir
                else:
                    if self.oneTimeWasFound:
                        self.oneTimeWasFound=False
                        self.reset_data()
                    path = self.aa_improved(position, self.direction, maze, begin_time)
                    if path and path[-1].dir in validdir:
                        dir = path[-1].dir
                    else:
                        vdirs = self.get_validirs(position, validdir, maze)
                        dir = vdirs[0] if vdirs else olddir

                        self.reset_data()

            self.direction = dir

        except:
            self.direction = (1,0)

    def aa_regular(self,startPos, startDir, maze, begin_time):
        startNode=Node(startPos, dir=startDir)
        targetNode=Node(maze.foodpos)
        startNode.hCost = self.pathlen(startPos,targetNode.get_pos())
        openNodes=[]
        closedNodes=[]
        openNodes.append(startNode)


        while openNodes!=[]:
            currentNode = openNodes[0]

            for node in openNodes:
                if node.fCost() < currentNode.fCost():
                    currentNode = node

            if currentNode in openNodes:
                openNodes.remove(currentNode)
            closedNodes.append(currentNode)

            if currentNode == targetNode:
                self.aa_regular_food_found=True
                return self.retracePath(startNode,currentNode)
            elif(pygame.time.get_ticks() - begin_time > self.agent_time - 3):
                self.aa_regular_food_found=False
                return self.retracePath(startNode,currentNode)

            neighbours = self.getNeighbours(currentNode, targetNode, self.maze_obstacles, maze.playerpos)
            [openNodes.append(n) for n in neighbours if n not in self.closedNodes and n not in openNodes]

    def aa_improved(self,startPos, startDir, maze, begin_time):
        targetNode=Node(maze.foodpos)
        if self.food_found:
            return self.retracePath(Node(startPos),self.last)
        if self.last:
            startNode = self.last
            if self.last in self.closedNodes:
                self.closedNodes.remove(self.last)
        else:
            startNode=Node(startPos, dir=startDir)
            startNode.hCost = self.pathlen(startPos,targetNode.get_pos())

        openNodes=[]
        openNodes.append(startNode)

        while openNodes!=[]:

            currentNode = min(openNodes, key = lambda node : node.fCost())

            if currentNode in openNodes:
                openNodes.remove(currentNode)
            self.closedNodes.append(currentNode)

            if currentNode == targetNode:
                self.food_found = True
                self.last = currentNode
                self.path_to_food = self.retracePath(Node(startPos),currentNode)
                return self.path_to_food

            if pygame.time.get_ticks() - begin_time > self.agent_time - 3:
                self.last = currentNode
                return self.retracePath(Node(startPos),currentNode)

            neighbours = self.getNeighbours(currentNode, targetNode, self.maze_obstacles, maze.playerpos)
            [openNodes.append(n) for n in neighbours if n not in self.closedNodes and n not in openNodes]

        self.reset_data()
    def retracePath(self,startNode, endNode):
        path=[]
        currentNode = endNode
        while currentNode and currentNode != startNode:
            path.append(currentNode)
            currentNode = currentNode.parent
        return path #if path else [startNode]

    def getNeighbours(self,node,foodNode, obstacles, playerpos):
        neighbours = []
        validdirs = self.getValidDirs(node, obstacles, playerpos)
        node_for_diag = None
        for dir in validdirs:
            coord = self.add(node.get_pos(),dir)
            newnode = Node(coord, dir=dir,gCost=node.gCost+1,parent=node)
            if dir == node.dir:
                node_for_diag = newnode
            newnode.hCost = self.pathlen(newnode.get_pos(),foodNode.get_pos())
            neighbours.append(newnode)
        if node.dir in validdirs:
            for diagDir in self.getValidDirsDiag(node, obstacles, playerpos):
                coord = self.add((node.x,node.y),diagDir)
                if node.dir == up or node.dir == down:
                    if diagDir == (-1,-1) or diagDir == (-1,1):
                        dir = left
                    else:
                        dir = right
                else:
                    if diagDir == (-1,-1) or diagDir == (1,-1):
                        dir = up
                    else:
                        dir = down
                if dir in validdirs:
                    newnode = Node(coord, dir=dir,gCost=node.gCost+2,parent=node_for_diag)
                    newnode.hCost = self.pathlen(newnode.get_pos(), foodNode.get_pos())
                    neighbours.append(newnode)
        return neighbours
    def getValidDirs(self,node, obstacles, playerpos):
        position=node.get_pos()
        dirs = []
        complement=[(up,down),(down,up),(right,left),(left,right)]
        invaliddir=[x for (x,y) in complement if y==node.dir]
        validdir = [dir for dir in directions if not ( dir in invaliddir )]

        return [dir for dir in validdir if not self.add(position,dir) in obstacles and not self.add(position,dir) in playerpos] #verificar se não vai contra o corpo

    def getValidDirsDiag(self,node,obstacles, playerpos):
        position=node.get_pos()
        diagComplement =[(up,(-1,1)), (up, (1,1)) , (down, (1,-1)), (down, (-1,-1)), (left, (1, 1)), (left, (1, -1)), (right, (-1,1)), (right, (-1, -1))]
        diagDirections = [(1,1),(1,-1),(-1,1),(-1,-1)]
        invaliddir = [y for (x,y) in diagComplement if x == node.dir]
        validdir = [dir for dir in diagDirections if not ( dir in invaliddir )]

        return [dir for dir in validdir if not self.add(position,dir) in obstacles and not self.add(position,dir) in playerpos]

class Node:
    def __init__(self,coord,dir=(0,0), gCost=0, hCost=0, parent=None):
        self.x=coord[0]
        self.y=coord[1]
        self.dir=dir
        self.parent=parent
        self.gCost=gCost
        self.hCost=hCost
    def __str__(self):
        return str((self.x,self.y))
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    def fCost(self):
        return self.hCost+self.gCost
    def get_pos(self):
        return (self.x, self.y)
