from snake import Snake
from constants import *
import pygame

class Agent_cluster(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0), name="Agent1"):
        super().__init__(body,direction,name=name)
        self.openNodes=[]
        self.closedNodes=[]
        self.lastPlayerlen=None
        self.foodpos=None
        self.path=[]
        self.cont=1
    # def pathlen(self,a,b):
    #     return int( ((a[0]-b[0])**2 + (a[1]-b[1])**2 )**0.5)
    def add(self,a,b):
        return (a[0]+b[0])%60,(a[1]+b[1])%40
    def pathlen(self,a,b):
        distX = abs(a[0]-b[0])
        distY = abs(a[1]-b[1])
        if distX > 60/2:
            distX = 60- distX;
        if distY > 40/2:
            distY = 40 - distY;
        return distX + distY
    def update(self,points=None, mapsize=None, count=None,agent_time=None):
        #self.points=points
        self.mapsize=mapsize
        self.count=count
        self.agent_time=agent_time
    def updateDirection(self,maze):
        #this is the brain of the snake player
        begin_time = pygame.time.get_ticks();

        olddir=self.direction
        position=self.body[0]

        #new direction can't be up if current direction is down...and so on
        complement=[(up,down),(down,up),(right,left),(left,right)]
        invaliddir=[x for (x,y) in complement if y==olddir]
        validdir=[dir for dir in directions if not ( dir in invaliddir )]

        #get the list of valid directions for us
        validdir=[dir for dir in validdir if not (self.add(position,dir) in maze.obstacles or self.add(position,dir) in maze.playerpos)]
        #if we collide then set olddir to first move of validdir (if validdir is empty then leave it to olddir)
        olddir= olddir if olddir in validdir or len(validdir)==0 else validdir[0]
        #shortest path.....we assume that the direction we are currently going now gives the shortest path
        # shortest=self.pathlen(self.add(position,olddir) , maze.foodpos)#length in shortest path
        # for dir in validdir:
        #     newpos=self.add(position,dir)
        #     newlen=self.pathlen(newpos , maze.foodpos)#length in shortest path
        #     if newlen < shortest:
        #         olddir=dir
        #         shortest=newlen
        # clusters=self.abstractMaze((2,2))

        # clusters=[print(x) for x in clusters]
        # targetPoint=maze.foodpos

        # idActualCluster = self.calculateClusterId(position)
        # idGoalCluster = self.calculateClusterId(maze.foodpos)
        # if(idActualCluster==idGoalCluster)
        #     self.a*(position,maze.foodpos)
        # else:
        #     bestPoint=self.bestTargetPoint(position,idActualCluster,clusters)
        #     self.a*(position,bestPoint)
        #
        #

        # if self.openNodes!=[]:
        #         path = self.aa(position, self.direction, maze, begin_time)
        #
        # else:
        # if path==[]:
        #print( self.pathlen(position,maze.foodpos))
        if self.openNodes!=[] or self.closedNodes!=[]:
            if self.lastPlayerlen!=len(maze.playerpos):
                self.lastPlayerlen=len(maze.playerpos)
                self.openNodes=[]
                self.closedNodes=[]
            elif self.pathlen(position,maze.foodpos)<10:
                print("teste")
                self.openNodes=[]
                self.closedNodes=[]
            elif self.foodpos==None:
                self.foodpos=maze.foodpos
                self.openNodes=[]
                self.closedNodes=[]
            elif self.pathlen(maze.foodpos,self.foodpos)>10:
                self.foodpos=maze.foodpos
                self.openNodes=[]
                self.closedNodes=[]
            else:
                print("guarda")

        if self.path!=[] and self.closedNodes!=[]:
            self.path=self.aa(position, self.direction, maze, begin_time)
            print("&")
            print(position, self.path[-1])
            dir = self.path[-1*cont].dir if self.path else olddir
            self.direction = dir # if self.path está por segurança
            #print(self.cont, len(path))
            self.cont+=1  # erro a usar isto. porquê?
        else:
            self.cont=1
            ##isto é o normal sem o if anterior e tirar o self.path para path
            self.path = self.aa(position, self.direction, maze, begin_time)
        # else:
            dir = self.path[-1].dir if self.path else olddir
            self.direction = dir # if self.path está por segurança




    # def bestTargetPoint(self,position,idActualCluster,clusters):
    #     getPoint=True
    #     clusterPoints=cluster[idActualCluster].defineCluster()
    #
    #     while getPoint:
    #         distTofood=[(x,self.pathlen(x,maze.foodpos)) for x in clusterPoints]



    # def calculateClusterId(self,point):
    #     xC=point[0]//self.horizontalNodesOfCluster
    #     yC=point[1]//self.verticalNodesOfCluster
    #
    #     return (xC,yC)


    def abstractMaze(self,numberofclusters):
        clusters=[]
        node=[0,0]
        cont=0
        self.horizontalNodesOfCluster=self.mapsize[0]/numberofclusters[0]
        self.verticalNodesOfCluster=self.mapsize[1]/numberofclusters[1]
        for y in range(numberofclusters[1]):
            for x in range(numberofclusters[0]):
                clusters.append(Cluster((x,y),(node[0],node[1]),(node[0]+self.horizontalNodesOfCluster-1,(y+1)*self.verticalNodesOfCluster-1)))
                node[0]=node[0]+self.horizontalNodesOfCluster
                cont+=1
            node[0]=0
            node[1]=(y+1)*self.verticalNodesOfCluster
        return clusters

######################################################################################
######################################################################################
######################################################################################

    def aa(self,startPos, startDir, maze, begin_time):
        ##############
        # clusterId=self.calculateClusterId(startPos)
        #############
        targetNode=Node(maze.foodpos)
        if self.closedNodes==[]:
            self.startNode=Node(startPos, dir=startDir)
            self.startNode.hCost = self.pathlen((startPos[0],startPos[1]),(targetNode.x,targetNode.y))
            self.openNodes.append(self.startNode)


        while self.openNodes!=[]:
            currentNode = self.openNodes[0]

            for node in self.openNodes:
                if node.fCost() < currentNode.fCost():
                    currentNode = node

            if currentNode in self.openNodes:
                self.openNodes.remove(currentNode)
            self.closedNodes.append(currentNode)
            if  (pygame.time.get_ticks() - begin_time > self.agent_time):
                return self.retracePath(self.startNode,currentNode)
            elif currentNode == targetNode: #or clusterId!=self.calculateClusterId(currentNode.get_pos())):
               self.openNodes=[]
               self.closedNodes=[]
               return self.retracePath(self.startNode,currentNode)

            for n in self.getNeighbours(currentNode, targetNode, maze):#otimizar
                if n not in self.closedNodes and n not in self.openNodes:
                    self.openNodes.append(n)

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


######################################################################################
######################################################################################
######################################################################################
class Cluster():
    def __init__(self,idCluster,point1,point2):
        self.id=idCluster   #(0,0) first cluster (0,1) # second cluster
        self.point1=point1
        self.point2=point2
    def __str__(self):
        return str(((self.point1[0],self.point2[1]),(self.point1[0],self.point2[1])))
    def getPoint1(self):
        return self.point1
    def getPoint2(self):
        return self.point2
    # def defineCluster(self):
    #     self.clusterLines=[]
    #     for x in range(self.horizontalNodesOfCluster):
    #         self.clusterLines.append((point1[0]+x,point1[1])
    #         self.clusterLines.append((point1[0]+x,point2[1]))
    #     for y in range(self.verticalNodesOfCluster):
    #         self.clusterLines.append((point2[0],point2[1]+y))
    #         self.clusterLines.append((point1[0],point2[1]+y))
    #     return self.clusterLines



    # def getId(position):
    #     x,y=self.getClustern(position)
    #     if x != self.getClustern((x+postion[0],postion[1])[0]:
    #         x=x+1
    #     if y != self.getClustern((position[0],postion[1]+y)[1]:
    #         y=y+1
    #     return x*y #id of cluster| os ids são de 1 para cima.
