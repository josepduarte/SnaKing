from snake import Snake
from constants import *
import math

class MyAgent1(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0)):
        super().__init__(body,direction,name="MyAgent1")
    def pathlen(self,a,b,obstacles):
        return int( ((a[0]-b[0])**2 + (a[1]-b[1])**2 )**0.5)
    def add(self,a,b):
        return (a[0]+b[0])%60,(a[1]+b[1])%40
    def update(self,points=None, mapsize=None, count=None,agent_time=None):
        pass
    def space(self,newdir):
        for x,y in self.body:
            if math.fabs(x-newdir[0])<=2:
                return False
            if math.fabs(y-newdir[1])<=2:
                return False
        for x,y in maze.playerpos:
            if math.fabs(x-newdir[0])<=2 and math.fabs(y-newdir[0]<=2):
                return False            
        return True               
    def teste(self,validdir,maze,position):
        newdir = [dir for dir in validdir for x,y in maze.playerpos if math.fabs(self.add(position,dir)[0]-x)>2 and math.fabs(self.add(position,dir)[1]-y)>2]
        if newdir!=[]:
            return newdir
        else:
            return validdir
    def updateDirection(self,maze):
        #this is the brain of the snake player
        olddir=self.direction
        position=self.body[0]
        
        #new direction can't be up if current direction is down...and so on
        complement=[(up,down),(down,up),(right,left),(left,right)]
        invaliddir=[x for (x,y) in complement if y==olddir]
        validdir=[dir for dir in directions if not ( dir in invaliddir )]
        
        #get the list of valid directions for us
        validdir=[dir for dir in validdir if not (self.add(position,dir) in maze.obstacles or self.add(position,dir) in maze.playerpos) or self.add(position,dir) in self.body] #verificar se não vai contra o corpo
       # print(maze.playerpos)
        #if we collide then set olddir to first move of validdir (if validdir is empty then leave it to olddir)
        olddir= olddir if olddir in validdir or len(validdir)==0 else validdir[0]
        #shortest path.....we assume that the direction we are currently going now gives the shortest path
        shortest=self.pathlen(self.add(position,olddir) , maze.foodpos, maze.obstacles)#length in shortest path
        print(maze.foodpos)
   #     for dir in validdir:
                #          newpos=self.add(position,dir)
  #          newlen=self.pathlen(newpos , maze.foodpos, maze.obstacles)#length in shortest path
  #          if newlen < shortest:
                    #             olddir=dir
   #             shortest=newlen
        self.direction=self.aa(position,maze.foodpos)
        #self.direction=olddir
    
    def aa(self,startPos,targetPos):
        startNode=node(startPos)
        targetNode=node(targetPos)
        openNodes=[]
        closedNodes=[]
    
        openNodes.append(startNode)

        while openNodes!=[]:
            currentNode = openNodes[0]
            openNodes.remove(currentNode)
        
            for n in openNodes:
                if n.f_cost() < currentNode.f_cost() or n.f_cost() == currentNode.f_cost() and openNode.h_cost < currentNode.h_cost:
                    currentNode = n
           # openNode.remove(currentNode)
            closedNodes.append(currentNode)
            if currentNode == targetNode:
               return retracePath(startNode,targetNode)
               # return None
            
            for n in self.getNeighbours(currentNode):
                if not (n in closedNodes):  #falta verificação
                    newMovementCost = currentNode.g_cost + self.getDistance(currentNode,n)
                if newMovementCost < n.g_cost or n in openNodes:
                    n.g_cost=newMovementCost
                    n.h_cost=self.getDistance(n,targetNode)
                    n.parent=currentNode
                    if not (n in openNode):
                        openNode.append(n)
    def retracePath(self,startNode, endNode):
        path=[]
        currentNode = endNode
        while currentNode != startNode:
            path.append(currentNode)
            currentNode = currentNode.parent
       # print(path.reverse)
        return path[0]

    def getDistance(self,nodeA,nodeB):
        print(nodeB.x)
        distX = math.fabs(nodeA.x-nodeB.x)
        distY = math.fabs(nodeA.y-nodeB.y)
        if distX > distY:
            return disty + distX-distY
        else:
            return distX + distY-distX

    def getNeighbours(self,node):
        neighbours = []

        for x in range(-1,2):
            for y in range(-1,2):
                if x == 0 and y == 0:
                    break
                else:
                    coor_x = node.x+x
                    coor_y = node.y+y
                    if coor_x >=0 and coor_x <=39 and coor_y>=0 and coor_y <=59:
                        neighbours.append((coor_x,coor_y))
        return neighbours
class node:
    def __init__(self,coord):
        self.x=coord[0]
        self.y=coord[1]
        self.parent=None
        self.g_cost=None
        self.h_cost=None
    def __str__(self):
        return x,y
    def f_cost(self):
        return self.h_cost+self.g_cost
     
