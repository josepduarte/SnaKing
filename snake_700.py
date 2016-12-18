from snake import Snake
from constants import *
import math
import pygame

class MyAgent700(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0), name="Agent1"):
        super().__init__(body,direction,name=name)
        self.last = None
        self.temp_len_players_positions = None
        self.closedNodes = []
        #self.openNodes = []
        self.food_found = False

    def pathlen(self,a,b):
        distX = abs(a[0]-b[0])
        distY = abs(a[1]-b[1])
        if distX > 60/2:
            distX = 60- distX;
        if distY > 40/2:
            distY = 40 - distY;
        return distX + distY
    def add(self,a,b):
        return (a[0]+b[0])%60,(a[1]+b[1])%40
    def update(self,points=None, mapsize=None, count=None,agent_time=None):
        #self.points=points
        self.mapsize=mapsize
        self.count=count
        self.agent_time=agent_time
    def updateDirection(self,maze):
        print("===================================")

        begin_time = pygame.time.get_ticks();
        
        temp_len = self.temp_len_players_positions
        self.temp_len_players_positions = len(maze.playerpos)
        if temp_len != self.temp_len_players_positions:
            self.last = None
            self.closedNodes = []
           #self.openNodes = []
            self.food_found = False
           # print("CHANGED")

        olddir=self.direction
        position=self.body[0]
        
        complement=[(up,down),(down,up),(right,left),(left,right)]
        invaliddir=[x for (x,y) in complement if y==olddir]
        validdir=[dir for dir in directions if not ( dir in invaliddir )]

        if len(self.body) > len(maze.playerpos):
            validdir=[dir for dir in validdir if not (self.add(position,dir) in maze.obstacles or self.add(position,dir) in maze.playerpos)]
        else:
            # possible enemy positions
            enemy_head = [pos for pos in maze.playerpos if pos not in self.body][0]
            possible_next_enemy_position = [self.add(enemy_head, dir) for dir in directions]
            validdir=[dir for dir in validdir if not (self.add(position,dir) in maze.obstacles or self.add(position,dir) in maze.playerpos or self.add(position,dir) in possible_next_enemy_position)]
        

        olddir= olddir if olddir in validdir or len(validdir)==0 else validdir[0]
        shortest=self.pathlen(self.add(position,olddir) , maze.foodpos)
        
        
        
        # avoid if enemy is considerable closer than us
        if(self.pathlen(enemy_head,maze.foodpos) + 5 < shortest):
           # print("AVOID")
            self.direction=olddir
            self.last = None
            self.closedNodes = []
            self.food_found = False
          #  print("DIR1: " + str(self.direction))
        # avoid food if we are +5 larger than enemy
        if len(self.body) > (len(maze.playerpos) - len(self.body) + 200):
           # print("AVOID 2")
            self.direction = olddir
            self.last = None
            self.closedNodes = []
            self.food_found = False
        # astar saving the path
        elif shortest > 5:
           # print("FIGHT FOR IT")
            path = self.aa_improved(position, self.direction, maze, begin_time)
           # print("BLA")
            if path and path[-1].dir in validdir:
                dir = path[-1].dir
            else:
                dir = olddir
                self.last = None
                self.closedNodes = []
                self.food_found = False
           # print("DIR2: " + str(dir))
            self.direction = dir # if self.path está por segurança 
          #  print("DIR2.2: " + str(self.direction))
        # regular astart
        else:
          #  print("CLOSE")
            self.last = None
            self.closedNodes = []
            self.food_found = False
            path = self.aa_regular(position, self.direction, maze, begin_time)
            self.direction = path[-1].dir if path and path[-1].dir in validdir else olddir
         #   print("DIR3: " + str(self.direction))

    def aa_regular(self,startPos, startDir, maze, begin_time):
        startNode=Node(startPos, dir=startDir)
        targetNode=Node(maze.foodpos)
        startNode.hCost = self.pathlen((startPos[0],startPos[1]),(targetNode.x,targetNode.y))
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
        
            if currentNode == targetNode or (pygame.time.get_ticks() - begin_time > self.agent_time - 0.5):
               return self.retracePath(startNode,currentNode)
            
            for n in self.getNeighbours(currentNode, targetNode, maze):#otimizar 
                if n not in closedNodes and n not in openNodes:
                    openNodes.append(n)


    def aa_improved(self,startPos, startDir, maze, begin_time):
        if self.food_found:
          #  print("bla1")
          #  print("DEBUG 1")
            return self.retracePath(Node(startPos),self.last)
        if self.last:
          #  print("bla2")
           # print("DEBUG 2")
            startNode = self.last
            if self.last in self.closedNodes:
                self.closedNodes.remove(self.last) 
        else:
          #  print("bla3")
            startNode=Node(startPos, dir=startDir)
       # print("DEBUG 3")
        targetNode=Node(maze.foodpos)
        startNode.hCost = self.pathlen((startPos[0],startPos[1]),(targetNode.x,targetNode.y))
        openNodes=[]
        #closedNodes=[]
        openNodes.append(startNode)
        
       # print("DEBUG 4")
        while openNodes!=[]:
            currentNode = openNodes[0]
       #     print("DEBUG 5")
            for node in openNodes:
                if node.fCost() < currentNode.fCost():
                    currentNode = node
         #   print("DEBUG 6")        
            if currentNode in openNodes:
                openNodes.remove(currentNode)
            self.closedNodes.append(currentNode)
        
       #     print("DEBUG 7")
            if currentNode == targetNode:
                self.food_found = True
       #         print("DEBUG 8")
                return self.retracePath(Node(startPos),currentNode)
            if pygame.time.get_ticks() - begin_time > self.agent_time - 0.5:
       #         print("DEBUG 9")
                return self.retracePath(Node(startPos),currentNode)
       #     print("DEBUG 10")
            for n in self.getNeighbours(currentNode, targetNode, maze):#otimizar 
                if n not in self.closedNodes and n not in openNodes:
                    openNodes.append(n)
        #print("DEBUG 11")
    def retracePath(self,startNode, endNode):
        path=[]
        currentNode = endNode
        self.last = endNode
       # print("startNode: " + str(startNode))
       # print("DEBUG 20")
        while currentNode != startNode:
        #    print("DEBUG 21")
        #    print("currentNode: " + str(currentNode))
            path.append(currentNode)
            currentNode = currentNode.parent
        #    print("DEBUD 22 --- currentNode = " + str(currentNode))
        return path #if path else [startNode]

    def getNeighbours(self,node,foodNode,maze):
        neighbours = []
        validdirs = self.getValidDirs(node,maze) 
        node_for_diag = None
        for dir in validdirs:
            coord = self.add((node.x,node.y),dir)
            newnode = Node(coord, dir=dir,gCost=node.gCost+1,parent=node)
            if dir == node.dir:
                node_for_diag = newnode
            newnode.hCost = self.pathlen((newnode.x,newnode.y),(foodNode.x,foodNode.y))
            neighbours.append(newnode)
        if node.dir in validdirs:
            for diagDir in self.getValidDirsDiag(node,maze):
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
                    newnode.hCost = self.pathlen((newnode.x,newnode.y),(foodNode.x,foodNode.y))
                    neighbours.append(newnode)  
        return neighbours
    def getValidDirs(self,node,maze):       
        position=node.get_pos()
        dirs = []
        complement=[(up,down),(down,up),(right,left),(left,right)]
        invaliddir=[x for (x,y) in complement if y==node.dir]
        validdir = [dir for dir in directions if not ( dir in invaliddir )]

        return [dir for dir in validdir if not self.add(position,dir) in maze.obstacles and not self.add(position,dir) in maze.playerpos] #verificar se não vai contra o corpo

    def getValidDirsDiag(self,node,maze):       
        position=node.get_pos()
        diagComplement =[(up,(-1,1)), (up, (1,1)) , (down, (1,-1)), (down, (-1,-1)), (left, (1, 1)), (left, (1, -1)), (right, (-1,1)), (right, (-1, -1))]
        diagDirections = [(1,1),(1,-1),(-1,1),(-1,-1)]
        invaliddir = [y for (x,y) in diagComplement if x == node.dir]
        validdir = [dir for dir in diagDirections if not ( dir in invaliddir )]

        return [dir for dir in validdir if not self.add(position,dir) in maze.obstacles and not self.add(position,dir) in maze.playerpos]

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