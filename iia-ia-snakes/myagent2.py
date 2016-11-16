from snake import Snake
from constants import *
import math

class MyAgent2(Snake):
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
        node1=self.aa(position,self.direction,maze)
        
        self.direction=(node1.x-position[0],node1.y-position[1])
        #self.direction=olddir
    
    def aa(self,startPos, startDir, maze):
        targetPos = maze.foodpos
        startNode=Node(startPos, startDir)
        targetNode=Node(targetPos)
        openNodes=[]
        closedNodes=[]
        openNodes.append(startNode)

       # print("DEBUG0 - openNodes: " + str([node for node in openNodes]))

        while openNodes!=[]:

            #print("DEBUG1 - openNodes: " + str([str(node) for node in openNodes]))

            currentNode = openNodes[0]
        #    openNodes.remove(currentNode)
             
            #for n in openNodes:
            #    if n!=currentNode and n.fCost() < currentNode.fCost() or n.fCost() == currentNode.fCost() and n.hCost < currentNode.hCost:
             #       currentNode = n
            for i in range(1,len(openNodes)):
                if openNodes[i].fCost() < currentNode.fCost() or(openNodes[i].fCost() == currentNode.fCost() and openNodes[i].hCost < currentNode.hCost):
                    print("Debug 13")
                    currentNode = openNodes[i]
            openNodes.remove(currentNode)
            closedNodes.append(currentNode)
            
            #print("DEBUG2 - openNodes: " + str([str(node) for node in openNodes]))

            if currentNode == targetNode:
               print("DEBUG 1O")
               return self.retracePath(startNode,currentNode)

            
            for n in self.getNeighbours(currentNode, targetNode, maze):#otimizar
                if n not in closedNodes and n not in openNodes:
                    openNodes.append(n)


            openNodes.sort(key=lambda x: x.fCost())
           # print("DEBUG3 - openNodes: " + str([str(node) for node in openNodes]))



    def retracePath(self,startNode, endNode):
        path=[]
        print("DEBUG 12-")
        currentNode = endNode
        print("ENDNODE: " + str(endNode))
        while currentNode != startNode:
            print("CURREENT NODE: ------ " + str(currentNode))
            path.append(currentNode)
            print("CURRENT NODE PARETN: " + str(currentNode.parent))
            currentNode = currentNode.parent
        print("PATH BEFORE REVERSE" + str(path))
        path.reverse()
        print("PATH AFTER REVERSE: " + str(path))
        return path[0]

    def getDistance(self,nodeA,nodeB):
        distX = math.fabs(nodeA.x-nodeB.x)
        distY = math.fabs(nodeA.y-nodeB.y)
        if distX > distY:
            return distY + distX-distY
        else:
            return distX + distY-distX

    def getNeighbours(self,node,foodNode,maze):
        neighbours = []
        for dir in self.getValidDirs(node,maze):
            coord = self.add((node.x,node.y),dir)
            if coord[0] >=0 and coord[0] <=39 and coord[1]>=0 and coord[1] <=59: #que validação é esta ?
                newnode = Node(coord, dir,node.gCost+1,parent=node)
                newnode.hCost = self.getDistance(newnode,foodNode)
                neighbours.append(newnode)
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
