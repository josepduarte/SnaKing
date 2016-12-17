from snake import Snake
from constants import *
import math
import pygame

class Agent_jps_memory(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0), name="Agent1"):
        super().__init__(body,direction,name=name)
        self.openNodes=[]
        self.closedNodes=[]
        self.lastPlayerlen=2
        self.foodpos=None
        self.path=[]
        self.first=True
        self.found_food_in_jps = False

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
        """
        if(shortest>25):
            for dir in validdir:
                newpos=self.add(position,dir)
                newlen=self.pathlen(newpos , maze.foodpos)#length in shortest path
                if newlen < shortest:
                    olddir=dir
                    shortest=newlen
            self.direction=olddir
        else:
        """

        if self.openNodes!=[] or self.closedNodes!=[]:
            if self.lastPlayerlen!=len(maze.playerpos):   #esta condição não deve ser necessária pois a comida muda de lugar
                self.lastPlayerlen=len(maze.playerpos)
                self.openNodes=[]
                self.closedNodes=[]
            elif self.pathlen(position,maze.foodpos)<2:
                self.openNodes=[]
                self.closedNodes=[]
            elif self.foodpos==None:
                self.foodpos=maze.foodpos
                self.openNodes=[]
                self.closedNodes=[]
            elif self.pathlen(maze.foodpos,self.foodpos)>20:
                self.foodpos=maze.foodpos
                self.openNodes=[]
                self.closedNodes=[]
            else:
                print("guarda")





        path = self.jps_astar(position, self.direction, maze, begin_time)
        dir = path[-1].dir if path and path[-1].dir in validdir else olddir
        self.direction = dir # if self.path está por segurança


    def aa(self,startPos, startDir, maze, begin_time):
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

            if currentNode == targetNode or (pygame.time.get_ticks() - begin_time > self.agent_time - 0.05):
               return self.retracePath(startNode,currentNode)

            for n in self.getNeighbours(currentNode, targetNode, maze):#otimizar
                if n not in closedNodes and n not in openNodes:
                    openNodes.append(n)


    def retracePath(self,startNode, endNode):
        path=[]
        currentNode = endNode
        while currentNode != startNode:
            path.append(currentNode)
            currentNode = currentNode.parent
        return path #if path else [startNode]

    def getNeighbours(self,node,foodNode,maze):
        neighbours = []
        validdirs = self.getValidDirs(node,maze)
        for dir in validdirs:
            coord = self.add((node.x,node.y),dir)
            newnode = Node(coord, dir=dir,gCost=node.gCost+1,parent=node)
            newnode.hCost = self.pathlen((newnode.x,newnode.y),(foodNode.x,foodNode.y))
            neighbours.append(newnode)
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
                newnode = Node(coord, dir=dir,gCost=node.gCost+2,parent=node)
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



    def jps_astar(self,startPos, startDir, maze, begin_time):
        # indicates if food has been found or not to be able to return sooner
        self.found_food_in_jps = False


        targetNode=Node(maze.foodpos)
        if self.closedNodes==[] or self.openNodes==[]:
            self.startNode=Node(startPos, dir=startDir)
            self.startNode.hCost = self.pathlen((startPos[0],startPos[1]),(targetNode.x,targetNode.y))
            self.openNodes=[]
            self.closedNodes=[]
            self.first=True
            print("reset")


        if self.first:
        # get the neighbours of start node
            for n in self.getNeighbours(self.startNode, targetNode, maze):#otimizar
                if n not in self.closedNodes and n not in self.openNodes:
                    self.openNodes.append(n)

            self.closedNodes.append(self.startNode)

        # start jps algorithm
        while self.openNodes:
            if self.first:
                self.currentNode = self.openNodes[0]

                # get the best neighbour
                for node in self.openNodes:
                    if node.fCost() < self.currentNode.fCost():
                        self.currentNode = node

                self.openNodes.remove(self.currentNode)
                self.closedNodes.append(self.currentNode)


                # get the neighbours of the current node
                for n in self.getNeighbours(self.currentNode, targetNode, maze):#otimizar
                    if n not in self.closedNodes and n not in self.openNodes:
                        self.openNodes.append(n)

                if (pygame.time.get_ticks() - begin_time > self.agent_time - 0.05):
                    self.first=False
                    return self.retracePath(self.startNode,self.currentNode)
                elif self.currentNode == targetNode:
                   self.openNodes=[]
                   self.closedNodes=[]
                   return self.retracePath(self.startNode,self.currentNode)
            self.first=True
            # expand (using jps algorithm) the best node
            node = self.expand_node(self.currentNode, targetNode, maze)
            # if the food has been found we can just retrace the path of the node we expanded
            if self.found_food_in_jps:
                return self.retracePath(startNode,self.currentNode)

            #print("NODE: " + str(node))
            if node and node not in self.closedNodes and node not in self.openNodes:
                self.openNodes.append(node)


    def expand_node(self, currentNode, targetNode, maze):
        temp_node = currentNode
        if temp_node.dir == right or temp_node.dir == left:
            while(temp_node.get_pos() not in maze.playerpos and temp_node.get_pos() not in maze.obstacles and temp_node != currentNode):
                if temp_node == targetNode:
                    self.found_food_in_jps = True
                    return currentNode
                if self.add(temp_node.get_pos(), up) in maze.obstacles or self.add(temp_node.get_pos(), down) in maze.obstacles or self.add(temp_node.get_pos(), up) in maze.playerpos or self.add(temp_node.get_pos(), down) in maze.playerpos:
                    return temp_node
                temp_node = Node(self.add(temp_node.get_pos(), temp_node.dir), temp_node.dir, temp_node.gCost+1, self.pathlen((temp_node.x,temp_node.y),(targetNode.x,targetNode.y)) ,currentNode)

        elif temp_node.dir == up or temp_node.dir == down:
             while(temp_node.get_pos() not in maze.playerpos and temp_node.get_pos() not in maze.obstacles and temp_node != currentNode):
                if temp_node == targetNode:
                    self.found_food_in_jps = True
                    return currentNode
                if self.add(temp_node.get_pos(), left) in maze.obstacles or self.add(temp_node.get_pos(), right) in maze.obstacles or self.add(temp_node.get_pos(), left) in maze.playerpos or self.add(temp_node.get_pos(), right) in maze.playerpos:
                    return temp_node
                temp_node = Node(self.add(temp_node.get_pos(), temp_node.dir), temp_node.dir, temp_node.gCost+1, self.pathlen((temp_node.x,temp_node.y),(targetNode.x,targetNode.y)) ,currentNode)

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
