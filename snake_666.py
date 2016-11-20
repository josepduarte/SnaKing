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
        shortest=self.pathlen(self.add(position,olddir) , maze.foodpos)#length in shortest path
        
        if(shortest>5):
            print("----- > 5 ------")
            for dir in validdir:
                newpos=self.add(position,dir)
                newlen=self.pathlen(newpos , maze.foodpos)#length in shortest path
                if newlen < shortest:
                    olddir=dir
                    shortest=newlen
            print("DIR in greater than 5: " + str(olddir))
            self.direction=olddir  
        else:
            print("-------- < 5 --------")
            dir = self.aa(position, olddir, maze)[-1].dir
            print("DIR: " + str(dir))
            self.direction = dir # if self.path está por segurança 

    
    def aa(self,startPos, startDir, maze):
        startNode=Node(startPos, dir=startDir)
        targetNode=Node(maze.foodpos)
        startNode.hCost = self.pathlen((startPos[0],startPos[1]),(targetNode.x,targetNode.y))
        openNodes=[]
        closedNodes=[]
        openNodes.append(startNode)

       # print("DEBUG0 - openNodes: " + str([node for node in openNodes]))

        while openNodes!=[]:

            #print("DEBUG1 - openNodes: " + str([str(node) for node in openNodes]))

            currentNode = openNodes[0]
             
            # !!! Não falta adicionar o current node aos closed???

            #for n in openNodes:
            #    if n!=currentNode and n.fCost() < currentNode.fCost() or n.fCost() == currentNode.fCost() and n.hCost < currentNode.hCost:
             #       currentNode = n
            #print("LEN OF OPEN NODES BEFORE IF: " + str(len(openNodes)))
            #if len(openNodes) > 50:
           #     openNodes = openNodes[-50:]
            #print("LEN OF OPEN NODES AFTER IF: " + str(len(openNodes)))
            for node in openNodes:
             #   print("Node: " + str(node) + "- f cost = " + str(node.fCost()))
                if node.fCost() < currentNode.fCost():
                    currentNode = node

            if currentNode in openNodes:
                openNodes.remove(currentNode)
            closedNodes.append(currentNode)
            
         #   print("DEBUG2 - openNodes: " + str([str(node) for node in openNodes]))
         #   print("CurrentNode - " + str(currentNode) + "== Target Node - " + str(targetNode))
            if currentNode == targetNode:
               return self.retracePath(startNode,currentNode)

            
            for n in self.getNeighbours(currentNode, targetNode, maze):#otimizar
                if n not in closedNodes and n not in openNodes:
                    openNodes.append(n)


           # openNodes.sort(key=lambda x: x.fCost())
           # print("DEBUG3 - openNodes: " + str([str(node) for node in openNodes]))

     #   print("BLAAAAAAAA")

    def retracePath(self,startNode, endNode):
        #
        #   !! path às vezes está a returnar none
        #
        path=[]
      #  print("STARTNODE: " + str(startNode))
     #   print("ENDNODE: " + str(endNode))
        #print("DEBUG 12-")
        currentNode = endNode
        #print("ENDNODE: " + str(endNode))
        while currentNode != startNode:
            print("CURRENT NODE: " + str(currentNode))
            print("START NODE: " + str(startNode))
            print("DIR OF CURRENT NODE" + str(currentNode.dir))
            #print("CURREENT NODE: ------ " + str(currentNode))
            path.append(currentNode)
            #print("CURRENT NODE PARETN: " + str(currentNode.parent))
            currentNode = currentNode.parent
        #print("PATH BEFORE REVERSE" + str(path))
        #path.reverse()
        #print("PATH AFTER REVERSE: " + str(path))
    #    print("PATH: " + str(path[0]))
        return path #if path else [startNode]

    def getNeighbours(self,node,foodNode,maze):
        #possibleNeighbours = 
        neighbours = []
        for dir in self.getValidDirs(node,maze):
            coord = self.add((node.x,node.y),dir)
       # if coord[0] >=0 and coord[0] <=39 and coord[1]>=0 and coord[1] <=59: #que validação é esta ?
            newnode = Node(coord, dir=dir,gCost=node.gCost+1,parent=node)
            newnode.hCost = self.pathlen((newnode.x,newnode.y),(foodNode.x,foodNode.y))
            neighbours.append(newnode)
        return neighbours
    def getValidDirs(self,node,maze):       
        # considerar todas as posições em vez de apenas os validdirs
        #   | 2 | 1 | 2 |
        #   | 3 | » | 1 |
        #   | 2 | 1 | 2 |
        #
        """
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
        """
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
