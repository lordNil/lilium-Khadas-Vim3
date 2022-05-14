import time
import subprocess
import multiprocessing as MP
import random


# -------- Processes that are started -------------


def UI(world):
    print('Started UI Module')
    import UI as U
    time.sleep(2)
    U.create_API(world) 


def Motion(world):
    print('Started Motion Module')
    import Motion as M
    M.create_motion(world)
    print('Shutdown motors')

def Sound(world):
    print('Started Sound Module')
    import Sound as S
    S.create_sound(world)
    print('Shutdown Sound')

def Vision(world):
    print('Starting Vision Module')
    import Vision as V
    V.create_vision(world)
    print('shutdown vision')

def Animation(world):
    print('Started Sound Module')
    import Neural as N
    A.create_animation(world)
    print('Shutdown Animations')


# --------- Start the Brain ---------

if __name__ == '__main__':


    
    mgr = MP.Manager()
    world = mgr.dict()
    world[ 'overall state']= 'sleep'     # options are: sleep, awake, shutdown
    world[ 'errors' ]      = ''          # Error messages are passed here to UI
    world[ 'power on' ]    = 1           # shutdown switch
    world[ 'sound state' ] = 'sleep'     # options are: idle, sex, chatbot, books
    world[ 'vision state'] = 'sleep'      # options are: sleep, idle, face, objects
    world[ 'motion state'] = 'relax'     # options are: relax, lay1, sit1, curl, missionary, frontal, doggy, oral

    world[ 'motion port' ] = '/dev/ttyS3'
    world[ 'camera port' ] = 0
    world[ 'mic port'    ] = 13
    world[ 'stiff spine']  = 1           # if the spine is stiff or not (affects head and torso)
    world[ 'animate time'] = 130
    world[ 'breath on']    = 1
    world[ 'battery' ]     = 50          # the charge of the battery from 0-100
    world[ 'volume' ]      = 0.2         # volume from 0 to 1
    world[ 'sex lvl' ]     = 0           # Sex bar from 1 to 10
    world[ 'say_now' ]     = ""          # String to say now
    world[ 'head_target' ] = []#
    world[ 'face detect' ] = 1
    world[ 'l faces'     ] = []
    world[ 'r faces'     ] = []
    world[ 'object_mode' ] = []
    world[ 'func1_x']      = [0,0]
    world[ 'books' ]       = []
    world[ 'pick book' ]   = ''
    world[ 'pick chapter'] = ''
    world[ 'play book' ]   = ''          # option for playing book: '' , 'new chapter' , 'playing'
    world[ 'update sound'] = 0
    world[ 'chatbot type'] = 'GTP'       # options are AIML, GTP

        

    p1 = MP.Process(target=UI,     args=(world,))
    p2 = MP.Process(target=Motion, args=(world,))
    p3 = MP.Process(target=Sound,  args=(world,))
    p4 = MP.Process(target=Vision, args=(world,))
    #p5 = MP.Process(target=Animation, args=(World,))
    Process_list = [  p1, p2, p3, p4]

    for p in Process_list:
        p.start()
        
        
    for p in Process_list:
        p.join()
        
