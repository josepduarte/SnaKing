from snake import Snake
from constants import *

class Agent2(Snake):
    def __init__(self,body=[(0,0)] , direction=(1,0), name="Agent_jose"):
        super().__init__(body,direction,name=name)

    def pathlen(self,a,b):
        return int( ((a[0]-b[0])**2 + (a[1]-b[1])**2 )**0.5)

    def pathcost(self,a, olddir, maze):
        print("POSITION: " + str(a))
        print("FOOD: " + str(maze.foodpos))
        if a==maze.foodpos:
            return 0
        complement=[(up,down),(down,up),(right,left),(left,right)]
        invaliddir=[x for (x,y) in complement if y==olddir]
        validdir=[dir for dir in directions if not ( dir in invaliddir )]
        
        validdir=[dir for dir in validdir if not (self.add(a,dir) in maze.obstacles or self.add(a,dir) in maze.playerpos)]
        olddir= olddir if olddir in validdir or len(validdir)==0 else validdir[0]
        cheaper=self.pathcost(self.add(a,olddir), olddir, maze) 
        for dir in validdir:
            newpos = self.add(a,dir)
            newcost = self.pathcost(newpos, dir, maze)
            if newcost < cheapless:
                cheaper = newcost
        return cheaper

    def add(self,a,b):
        return a[0]+b[0],a[1]+b[1]
    
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
        validdir=[dir for dir in validdir if not (self.add(position,dir) in maze.obstacles or self.add(position,dir) in maze.playerpos)]
        #if we collide then set olddir to first move of validdir (if validdir is empty then leave it to olddir)
        olddir= olddir if olddir in validdir or len(validdir)==0 else validdir[0]
        #shortest path.....we assume that the direction we are currently going now gives the shortest path
        shortest=self.pathlen(self.add(position,olddir) , maze.foodpos) + self.pathcost(self.add(position, olddir), olddir, maze)#length
        for dir in validdir:
            newpos=self.add(position,dir)
            newlen=self.pathlen(newpos , maze.foodpos)#length in shortest path
            newcost=self.pathcost(newpos , maze) #cost
            if newlen + newcost < shortest:
                olddir=dir
                shortest=newlen
        self.direction=olddir
 
