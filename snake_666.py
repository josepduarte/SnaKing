from snake import Snake
from constants import *
import math

class MyAgent666(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0), name="Agent1"):
        super().__init__(body,direction,name=name)
        self.path = []
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
        pass
    def updateDirection(self,maze):
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
        if(shortest>10):
        #    print("----- > 5 ------")
            for dir in validdir:
                newpos=self.add(position,dir)
                newlen=self.pathlen(newpos , maze.foodpos)#length in shortest path
                if newlen < shortest:
                    olddir=dir
                    shortest=newlen
            #print("DIR in greater than 5: " + str(olddir))
            self.direction=olddir  
        else:
          #  print("-------- < 5 --------")
            path = self.aa(position, self.direction, maze)
            dir = path[-1].dir
            #print("DIR: " + str(dir))
            self.direction = dir # if self.path está por segurança 
        print("DIR ASSUMED: " + str(self.direction))

    
    def aa(self,startPos, startDir, maze):
        print("----------------------------------------------------------------------------------------startPOS: " + str(startPos))
        print("------------________________-----------------_----------------_------___________--------foodNode: " + str(maze.foodpos))
        startNode=Node(startPos, dir=startDir)
        targetNode=Node(maze.foodpos)
        startNode.hCost = self.pathlen((startPos[0],startPos[1]),(targetNode.x,targetNode.y))
        openNodes=[]
        closedNodes=[]
        openNodes.append(startNode)

        while openNodes!=[]:
            currentNode = openNodes[0]
             
            print("CURRENT NODE: " + str(currentNode))
            print("CURRENT NODE BEFORE FOR: " + str(currentNode) + " -> fcost= " + str(currentNode.fCost()))
            for node in openNodes:
                print("--- NODE " + str(node) + "NODE.gCOST = " + str(node.gCost) + "NODE.hCOST = " + str(node.hCost) + "NODE.FCOST = " + str(node.fCost()))
                if node.fCost() < currentNode.fCost():
                    currentNode = node
            print("CURRENT NODE AFTER FOR: " + str(currentNode) + " -> fcost= " + str(currentNode.fCost()) + "DIR: " + str(currentNode.dir))

            if currentNode in openNodes:
                openNodes.remove(currentNode)
            closedNodes.append(currentNode)
        
            if currentNode == targetNode:
               return self.retracePath(startNode,currentNode)

            print("___________PRINT NEIGBOURHS OF " + str(currentNode) + "_____________")
            for n in self.getNeighbours(currentNode, targetNode, maze):#otimizar
                if n not in closedNodes and n not in openNodes:
                    openNodes.append(n)
            print("_---------------------------------_")

    def retracePath(self,startNode, endNode):
        path=[]
        currentNode = endNode
        while currentNode != startNode:
            path.append(currentNode)
            currentNode = currentNode.parent
        return path #if path else [startNode]

    def getNeighbours(self,node,foodNode,maze):
        neighbours = []
        print("NODE: " + str(node) + " -> dir: " + str(node.dir))
        for dir in self.getValidDirs(node,maze):
            coord = self.add((node.x,node.y),dir)
            newnode = Node(coord, dir=dir,gCost=node.gCost+1,parent=node)
            newnode.hCost = self.pathlen((newnode.x,newnode.y),(foodNode.x,foodNode.y))
            neighbours.append(newnode)
        print("NEIGBOURS: " + str([str(a) for a in neighbours]))
        return neighbours
    def getValidDirs(self,node,maze):       
        position=node.get_pos()
        dirs = []
        complement=[(up,down),(down,up),(right,left),(left,right)]
        invaliddir=[x for (x,y) in complement if y==node.dir]
        validdir = [dir for dir in directions if not ( dir in invaliddir )]
        return [dir for dir in validdir if not (self.add(position,dir) in maze.obstacles or self.add(position,dir) in maze.playerpos) or self.add(position,dir) in self.body] #verificar se não vai contra o corpo

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
