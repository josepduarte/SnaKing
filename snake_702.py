from snake import Snake
from constants import *
import math
import pygame

class MyAgent702(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0), name="Jewpacabra"):
        super().__init__(body,direction,name=name)
        self.path = []
        self.last = None
        self.temp_len_players_positions = None
        self.closedNodes = []
        self.openNodes = []

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
        begin_time = pygame.time.get_ticks();

        temp_len = self.temp_len_players_positions
        self.temp_len_players_positions = len(maze.playerpos)
        if temp_len != self.temp_len_players_positions:
            self.last = None
            self.closedNodes = []
            self.openNodes = []

        olddir=self.direction
        position=self.body[0]
        
        complement=[(up,down),(down,up),(right,left),(left,right)]
        invaliddir=[x for (x,y) in complement if y==olddir]
        validdir=[dir for dir in directions if not ( dir in invaliddir )]
        
        validdir=[dir for dir in validdir if not (self.add(position,dir) in maze.obstacles or self.add(position,dir) in maze.playerpos) or self.add(position,dir) in self.body] 
        olddir= olddir if olddir in validdir or len(validdir)==0 else validdir[0]
        shortest=self.pathlen(self.add(position,olddir) , maze.foodpos)
        
        #opponentSnakePos = [pos for pos in maze.playerpos if pos not in self.body]
        #if(self.pathlen(opponentSnakePos[0],maze.foodpos) + 10 < shortest):
        #    self.direction=olddir
        
        path = self.aa(position, self.direction, maze, begin_time)
        if path and path[-1].dir in validdir:
            dir = path[-1].dir
        else:
            dir = olddir
            self.last = None
            self.openNodes = []
            self.closedNodes = []
        self.direction = dir # if self.path está por segurança 
    
    def aa(self,startPos, startDir, maze, begin_time):
     #   print("=================== STARTNODE = " + str(startPos) + "===================")
        targetNode=Node(maze.foodpos)
        if self.last:
            if self.last == targetNode:
                return self.retracePath(Node(startPos), self.last)
            else:
                startNode = self.last
        else:
            startNode=Node(startPos, dir=startDir)
            startNode.hCost = self.pathlen(startPos,targetNode.get_pos())

        openNodes=[]
        openNodes.append(startNode)
        
        
        while openNodes!=[]:
            currentNode = openNodes[0]
             
            for node in openNodes:
                if node.fCost() < currentNode.fCost():
                    currentNode = node

            if currentNode in openNodes:
                openNodes.remove(currentNode)
            self.closedNodes.append(currentNode)
        
            if currentNode == targetNode or (pygame.time.get_ticks() - begin_time > self.agent_time - 1):
                self.last = currentNode
                return self.retracePath(Node(startPos),currentNode)
            
            for n in self.getNeighbours(currentNode, targetNode, maze):#otimizar 
                if n not in self.closedNodes and n not in openNodes:
                    openNodes.append(n)

     #   print("GETTED OUT OF THE WHILE")

    def retracePath(self,startNode, endNode):
        path=[]
        currentNode = endNode
       # print("-----------------------------------------")
       # print("STARNODE: " + str(startNode))
       # print("ENDNODE: " + str(endNode))
        while currentNode != startNode:
            path.append(currentNode)
        #    print("NODE: " + str(currentNode.get_pos()) + "---» PARENT: " + str(currentNode.parent))
        #    print("RESULT: " + str(startNode) + "+" + str(currentNode.dir) + "= " + str(self.add(startNode.get_pos(), currentNode.dir)))
            currentNode = currentNode.parent
        #print("_________________________________________")
        return path #if path else [startNode]

    def getNeighbours(self,node,foodNode,maze):
        neighbours = []
        validdirs = self.getValidDirs(node,maze) 
        node_for_diag = None
        for dir in validdirs:
            coord = self.add((node.x,node.y),dir)
            newnode = Node(coord, dir=dir,gCost=node.gCost+1,parent=node)
           # print("NODE: " + str(newnode.get_pos()) + " - " + str(newnode.dir) + "---» PARENT: " + str(newnode.parent))
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
             #       print("NODE: " + str(newnode.get_pos()) + " - " + str(newnode.dir) + "---» PARENT: " + str(newnode.parent))
                    newnode.hCost = self.pathlen((newnode.x,newnode.y),(foodNode.x,foodNode.y))
                    neighbours.append(newnode)  
        return neighbours
    def getValidDirs(self,node,maze):       
        position=node.get_pos()
        dirs = []
        complement=[(up,down),(down,up),(right,left),(left,right)]
        invaliddir=[x for (x,y) in complement if y==node.dir]
        validdir = [dir for dir in directions if not ( dir in invaliddir )]

        return [dir for dir in validdir if not self.add(position,dir) in maze.obstacles and not self.add(position,dir) in maze.playerpos and not self.add(position,dir) in self.body] #verificar se não vai contra o corpo

    def getValidDirsDiag(self,node,maze):       
        position=node.get_pos()
        diagComplement =[(up,(-1,1)), (up, (1,1)) , (down, (1,-1)), (down, (-1,-1)), (left, (1, 1)), (left, (1, -1)), (right, (-1,1)), (right, (-1, -1))]
        diagDirections = [(1,1),(1,-1),(-1,1),(-1,-1)]
        invaliddir = [y for (x,y) in diagComplement if x == node.dir]
        validdir = [dir for dir in diagDirections if not ( dir in invaliddir )]

        return [dir for dir in validdir if not self.add(position,dir) in maze.obstacles and not self.add(position,dir) in maze.playerpos and not self.add(position,dir) in self.body]

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
