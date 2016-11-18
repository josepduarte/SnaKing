from game import *
from human import HumanSnake
from agent1 import Agent1
from maze import Maze
import importlib
import asyncio
import websockets
import json
import logging
import sys, getopt


#start the game
def main(argv):
    inputfile = None
    visual = True
    network = False
    url = 'ws://localhost:8765' 
    url = None
    StudentAgent = Agent1
    studentAgent_name = "Agent1"
    student_url = None
    OponentAgent = Agent1
    sponentAgent_name = "Agent1"
    oponent_url = None
    try:
        opts, args = getopt.getopt(argv,"hm:s:o:p",["help","map=","disable-video","student-agent=","oponent-agent=","proxy"])
    except getopt.GetoptError as e:
        print(e)
        print('start.py [-h/--help -m/--map <mapfile> --disable-video -p/--proxy -s/--student-agent AgentName,Name[,websocket] -o/--oponent-name AgentName,Name[,websocket]]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('start.py [-h/--help -m/--map <mapfile> --disable-video -p/--proxy -s/--student-agent AgentName,Name[,websocket] -o/--oponent-name AgentName,Name[,websocket]]')
            sys.exit()
        elif opt in ("-m", "--map"):
            inputfile = arg
        elif opt in ("--disable-video"):
            visual = False 
        elif opt in ("-p", "--proxy"):
            network = True
        elif opt in ("-s", "--student-agent"):
            a = arg.split(',')
            classmodule = importlib.import_module(a[0].lower())
            classInst = getattr(classmodule, a[0])
            StudentAgent = classInst
            studentAgent_name = a[1]
            if len(a) > 2:
                student_url = a[2]
        elif opt in ("-o", "--oponent-agent"):
            a = arg.split(',')
            classmodule = importlib.import_module(a[0].lower())
            classInst = getattr(classmodule, a[0])
            OponentAgent = classInst 
            oponentAgent_name = a[1]
            if len(a) > 2:
                oponent_url = a[2]

    if network:
        if student_url == None:
            print("Must specify --student-agent Agent,name,websocket")
            sys.exit(1)
        print("Connecting to {}".format(url))
        asyncio.get_event_loop().run_until_complete(proxy(student_url,StudentAgent, studentAgent_name))
    else:
        snake=SnakeGame(hor=60, ver=40, fps=20, visual=visual, obstacles=15, mapa=inputfile)
        snake.setPlayers([  
            StudentAgent([snake.playerPos()], name=studentAgent_name) if student_url == None else StudentAgent([snake.playerPos()], name=student_name, url=student_url),
            OponentAgent([snake.playerPos()], name=oponentAgent_name) if oponent_url == None else OponentAgent([snake.playerPos()], name=oponentAgent_name, url=oponent_url),
        ])
        snake.start()

async def proxy(url, StudentAgent, agent_name):
    async with websockets.connect(url) as websocket:
        logger = logging.getLogger('websockets')
        logger.setLevel(logging.ERROR)
        logger.addHandler(logging.StreamHandler())

        #connect to proxy, get init values and announce ourselves through the agent name
        await websocket.send(json.dumps({'cmd': 'AGENT', 'agent_name': agent_name}))
        init = json.loads(await websocket.recv())
        agent = StudentAgent([(b[0], b[1]) for b in init['body']],(init['direction'][0], init['direction'][1]), name = agent_name)
        await websocket.send(agent.name)

        while True:
            m = await websocket.recv()
            msg = json.loads(m)
            if msg['cmd'] == 'updateBody':
                agent.updateBody([(b[0], b[1]) for b in msg['body']])
            if msg['cmd'] == 'update':
                logging.info(msg['points'])
                agent.update(points=[(p[0], p[1]) for p in msg['points']], mapsize=(msg['mapsize'][0],msg['mapsize'][1]), count=msg['count'], agent_time=msg['agent_time'])
            elif msg['cmd'] == 'updateDirection':
                maze = Maze(None, None, None) #create void maze before loading the real one
                maze.fromNetwork(msg['maze'])
                agent.updateDirection(maze)
                await websocket.send(json.dumps(agent.direction))

if __name__ == "__main__":
   main(sys.argv[1:])

