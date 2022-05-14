
####### Control of the servos   ###############


####### Initialization  #############

import os
import time
import random
import serial

'''
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
'''


from motion.servos import *                 # Uses SCServo SDK library located in servos folder


####### Settings and variables  ##########

SCS_ID                  = 1                 # Servo ID for testing
BAUDRATE                = 1000000           # SCServo default baudrate : 1000000


# Register Adresses for motors
torque       = 40    # torque enable - 1 or 0 (also write 128 here to set motor to mid position)
goal_acc     = 41    # goal acceleration
goal_pos     = 42    # goal position
goal_speed   = 46    # goal speed  (in position values / second)
curr_pos     = 56    # current position
curr_load    = 60    # current PWM load_image_file
curr_curr    = 69    # current Current up to 3.5A

packID = 0

# Servos
# the servos are organized as a list of sevos, and each servo is a list of data
# left and right are from perspective of robot. (abbreviated as L and R)
# clockwise and counterclockwise abbreviated as CW and CCW

servoname ="Test Motor" # describes servo motion going from limit B to A
ID      = 0              # the ID number of the servo
typee   = 0              # 0 is for sms or sts and 1 is for scs
limitA  = 100            # limits of servo position (moving in direction)
limitB  = 1000
mid     = 500           # The middle position of the motion
direct  = -1            # direction: position value goes up or down with motion ( 1 or -1)
enable  =  0            # If motor torque is enabled/disabled (1 for enable)
pos     = -1            # current position (if not known then -1)
speed   = -1            # current speed    (if not known then -1)

# The data table for each of the motors.
# Index:    0            1     2      3       4         5        6      7       8     9
m0  = [  servoname     , ID, typee, limitA, limitB,   mid    , direct,enable, pos, speed ]
m50 = [ "Jaw  up"      , 50,     0,   2100,   1950,      2050,      1,   -1,   -1,    -1 ]
m51 = [ "Eyes up"      , 51,     1,    380,    580,       450,      1,   -1,   -1,    -1 ]
m1  = [ "Head CW"      ,  1,     0,   1400,   3100,      2050,      1,   -1,   -1,    -1 ]
m2  = [ "Head forward" ,  2,     0,   1400,   3100,      2050,     -1,   -1,   -1,    -1 ]
m3  = [ "Neck CW"      ,  3,     0,    770,   3500,      2050,      1,   -1,   -1,    -1 ]
m4  = [ "Torso CW"     ,  4,     0,   2850,   1350,      2050,      1,   -1,   -1,    -1 ]
m5  = [ "Torso forward",  5,     0,    900,   3300,      2000,     -1,   -1,   -1,    -1 ]
m6  = [ "Torso left"   ,  6,     0,   1700,   2300,      2000,      1,   -1,   -1,    -1 ]

m10 = [ "R Shoulder fw", 10,     0,    100,   2740,      2000,     -1,   -1,   -1,    -1 ]
m11 = [ "R Arm out"    , 11,     0,   1050,   3000,      1200,      1,   -1,   -1,    -1 ]
m12 = [ "R Arm CW"     , 12,     0,   3150,   1030,      2000,     -1,   -1,   -1,    -1 ]
m13 = [ "R Elbow curl" , 13,     0,    690,   2150,      2000,     -1,   -1,   -1,    -1 ]
m14 = [ "R Hand CW"    , 14,     1,    770,    210,       500,     -1,   -1,   -1,    -1 ]
m15 = [ "R Hand curl"  , 15,     1,    265,    830,       500,      1,   -1,   -1,    -1 ]
m16 = [ "R Hand finger", 16,     1,    100,   1000,       500,      1,   -1,   -1,    -1 ]

m20 = [ "L Shoulder fw", 20,     0,   3890,   1265,      2000,     -1,   -1,   -1,    -1 ]
m21 = [ "L Arm out"    , 21,     0,   3050,   1150,      2900,     -1,   -1,   -1,    -1 ]
m22 = [ "L Arm CW"     , 22,     0,   1038,   3115,      2000,      1,   -1,   -1,    -1 ]
m23 = [ "L Elbow curl" , 23,     0,   3380,   1950,      2000,     -1,   -1,   -1,    -1 ]
m24 = [ "L Hand CW"    , 24,     1,    200,    760,       500,     -1,   -1,   -1,    -1 ]
m25 = [ "L Hand curl"  , 25,     1,    235,    835,       500,      1,   -1,   -1,    -1 ]
m26 = [ "L Hand finger", 26,     1,    800,    200,       500,      1,   -1,   -1,    -1 ]

m30 = [ "R Hip CW"     , 30,     0,    711,   2370,      2050,     -1,   -1,   -1,    -1 ]
m31 = [ "R Leg up"     , 31,     0,   3540,    100,       800,      2,   -1,   -1,    -1 ]
m32 = [ "R Leg CW"     , 32,     0,   1640,   3200,      2050,     -1,   -1,   -1,    -1 ]
m33 = [ "R Knee Bend"  , 33,     0,    440,   2100,      2000,     -1,   -1,   -1,    -1 ]
m34 = [ "R Foot up"    , 34,     1,    280,    780,       500,     -1,   -1,   -1,    -1 ]

m40 = [ "L Hip CW"     , 40,     0,   3500,   1000,      1950,      1,   -1,   -1,    -1 ]
m41 = [ "L Leg up"     , 41,     0,    180,   3900,      3000,     -2,   -1,   -1,    -1 ]
m42 = [ "L Leg CW"     , 42,     0,    800,   2480,      2050,     -1,   -1,   -1,    -1 ]
m43 = [ "L Knee Bend"  , 43,     0,   3700,   2050,      2000,      1,   -1,   -1,    -1 ]
m44 = [ "L Foot up"    , 44,     1,    750,    230,       500,      1,   -1,   -1,    -1 ]

# The list of all the motors
# the Motors global variable is updated with new data
Motors = [  m50, m51,  m2, m3, m4, m5, m10, m11, m12, m13, m14, m15,  m20, m21, m22, m23, m24, m25, m30, m31, m32, m33, m34, m40, m41, m42, m43, m44 ]

#------- the ANimations folder
movements = os.listdir('motion/')

##----------------------------------Main Function-----------------------------------

def create_motion( world ):

    init_servos(world['motion port'])

    while world['power on']:
    
    ##----------------------------------- Head Movements
        head = world['vision state']
        if head  == 'idle':
            base = 1800
            if world['motion state'] == 'sit1':
                base = 2000
            head_random_move(base, 5, world['stiff spine'] )
        if head  == 'face':
            face_target(  world['l faces'] , world['r faces'] )
        if head  == 'sleep':
            vv = 1
            
        if world['motion state']  == 'oral':
            oral_sex( 1, 400, world['stiff spine']) # moves with rate of 1 and magnitude 400
            
     ### -------------------------------- Body Movements
            
        breath( 2, 40, world['stiff spine'] )

        # moves single motor randomly
        #random_move([], 70, 20)

        play_animation( world['motion state'], world['animate time'] )

        #check_torque()

        time.sleep(0.1)

    relax_all()
    closeport()


##---------------------------------------------------------------------------------

## this function plays an animation, and randomly plays down the animation tree
## input is: relax, lay1, sit1, curl, missionary, frontal, doggy, oral
# these are the main states, and then variations on them are .1 ect  ( lay1.3, curl.5 )
time_animate = time.time() ## timer for playing animation varients
playing = 0   ## if an animation is playing or not
prev_animation = 'X'

def play_animation(state, interval):
 
    # detects if transitioning to new state
    global prev_animation
    state_transition = False
    same = state in prev_animation
    if not same:
        state_transition = True

    # triggers animation if timmer or state transition occurs
    global time_animate
    diff = time.time() - time_animate
    if (diff> interval) or state_transition:
        time_animate = time.time()

        list_animations = []
        if state_transition:
            play_me = state
            list_animations.append(play_me)
        else:
            # extract the relevant animations from movement folder
            for mov in movements:
                if state in mov:
                    if mov != prev_animation:
                        list_animations.append(mov)
        if list_animations == []:
            play_me = ''
        else:
            play_me = random.choice(list_animations)
            print('playing: '+ play_me)
            prev_animation = play_me
            play_simple(play_me)




### this function changes the torso and the head slightly to mimic breathing
# breathrate in seconds/move
## only moves when timmer is triggered. otherwise does nothing

breath_time = time.monotonic()
up = 1
def breath( breath_rate, steps, stiff_torso ):
    global breath_time
    delta = time.monotonic() - breath_time
    #print(delta)
    if (delta > breath_rate):
        global up
        torso_base_pos = read(5, curr_pos)
        if torso_base_pos is not None:
            #print('breath')
            write(5, goal_pos, int(torso_base_pos + steps* up))
        up = up * -1
        breath_time = time.monotonic()
        if not stiff_torso:
            time.sleep(1)
            relax(5)
        #print(up)
        


# this moves the head to a random target in list
def Head_target(target_list):
    target = random.choice(target_list)
    x_diff = -1*( 700 - target[0]  )   # midpoint at 700 pix, converted to degrees
    h_diff = -1* ( 1300 - target[1] )
    if (abs(x_diff) > 100):
        head_x = read(1, curr_pos)
        goal = head_x + x_diff/4
        x,y = head_box(goal, 2000)
        move(m1, int( x ) )
    if (abs(h_diff)>100):
        head_h = read(2, curr_pos)
        goal = head_h + h_diff/6
        x,y = head_box(2000, goal)
        move(m2, int(y) )

# this function take as input the faces found from left and right eyes
## tries to move the head to the location
def face_target( lfaces , rfaces ):
    target_face = [0.5 , 0.5]
    target_score = 0
    for lface in lfaces:
        if lface[2] > target_score:
            target_face[0] = lface[0]
            target_face[1] = lface[1]
            target_score = lface[2]
    for lface in rfaces:
        if lface[2] > target_score:
            target_face[0] = lface[0]
            target_face[1] = lface[1]
            target_score = lface[2]
    #print( 'targeting face' + str(target_face))
    
    x_diff = 1 * (0.5- target_face[0]) * 1111    # x values of face go from -50degrees to +50 Degrees. for the motors, 4000/360 steps/degree = 1111 steps /100degree
    y_diff = 1 * (0.5- target_face[1]) * 833  # for y the resolution is 640x480 thus it is scaled down by 0.75 = 833 steps/framey
    
    move_head = 0
    if (abs(x_diff) > 1):
        head_x = read(3, curr_pos)
        goal = head_x + x_diff/2
        write(3, goal_pos , goal)
        move_head = 1
    if (abs(y_diff)>1):
        head_y = read(2, curr_pos)
        goal = head_y + y_diff/2
        write(2 , goal_pos, goal)
        move_head = 1
    if move_head == 1:
        time.sleep(0.7)

### this moves the head randomly within a box around the base positions
# only moves if timmer is triggered, otherwise it does nothing
head_rand_time = time.time()
head_base_y = 2000

def head_random_move(head_base_pos, timer, stiff_torso):
    global head_rand_time
    range_m3 = 300
    range_m2 = 100
    t2 = time.time() - head_rand_time
    randt = 2*random.random()
    if (t2 > (timer+ randt)):
        #print('head random move')
        off_m3 = (random.random()-0.5)*2 * range_m3
        off_m2 = (random.random()-0.5)*2 * range_m2
        write(3, goal_pos, int(head_base_y + off_m3))
        write(2, goal_pos, int(head_base_pos + off_m2))

        head_rand_time = time.time()

        if not stiff_torso:
            time.sleep(2)
            relax(2)
            relax(3)

### This function controls the eye movement
## mid is 450 and 500 to go down, 430 to go up 580 is close. eyes sometimes get stuck
### if state is sleep, then close eyes, else move eyes randomly depending on time 'timer'

eyetime = time.time()
eye_base = 2000
eye_positions = [450, 500, 475, 420]

def move_eyes(state, timer):
    global eyetime
    t2 = time.time() - eyetime
    randt = 2*random.random()
    if (t2 > (timer+ randt)) and (state != 'sleep'):
        print('eye random move')
        target = random.choice(eye_positions)
        write(51, goal_pos, target)
        eyetime = time.time()
    
    if state == 'sleep' :
        write(51, goal_pos, 580)

### This function controls the mouth movement
## states are: close , open, sex, and talk

mouthtime = time.time()
mouth_base = 2050
mouth_close = 2080
mouth_open = 1980

def move_mouth(state):
    
    if state == 'talk':
        global mouthtime
        t2 = time.time() - mouthtime
        randt = 0.5*random.random() + 0.3
        if (t2 > (randt)) :
            #print('talking mouth')
            target = mouth_base + 100 * random.random() - 50
            write(50, goal_pos, target)
            mouthtime = time.time()
        
    if state == 'open' :
        write(50, goal_pos, mouth_open)

    if state == 'close' :
        write(50, goal_pos, mouth_close)

# this puts the x and h of head position within a box around the head base position
def head_box(head_base_pos, x, h):
    x_up = head_base_pos + 200
    x_down = head_base_pos - 200
    y_up = head_base_pos +100
    y_down = head_base_pos - 100
    if x > x_up:
        x = x_up
    if x < x_down:
        x = x_down
    if h > y_up:
        h=y_up
    if h< y_down:
        h = y_down
    return x, h

### this function moves the head up and down
# breathrate in seconds/move
## only moves when timmer is triggered. otherwise does nothing

oral_time = time.time()
up_oral = 0
def oral_sex( breath_rate, magnitude, stiff_torso):

    global oral_time
    global up_oral
    up = up_oral
    t2 = time.time() - oral_time

    if (t2 > breath_rate)and (up==0):
        h_base_pos = read(2, curr_pos)
        set_speed_rand(2, 300)
        write(2, goal_pos, int(h_base_pos + magnitude*(random.random()+ 0.5)))
        up = 1
        oral_time = time.time()
        time.sleep(breath_rate * 0.7)
        relax(2)

    if (t2 > breath_rate)and (up==1):
        h_base_pos = read(2, curr_pos)
        set_speed_rand(2, 300)
        write(2, goal_pos, int(h_base_pos - magnitude *(random.random()+0.5)))
        up = 0
        oral_time = time.time()
        time.sleep(breath_rate * 0.7)
        relax(2)



# This checks for overload condition and relaxes motor if overlaod
def check_torque():
    global Motors
    moving_motors = []
    for x in Motors:
        if x[7] == 1:
            moving_motors.append(x)
    for x in moving_motors:
        load = read(x[1], curr_load)
        #print("motor " + str(x[1]) + " has load "+ str(load))
        if load == False:
            write(x[1], 40, 0 )


### Open port
### if imput port is '' then it tests and finds available port
def init_servos( port ):
    if port == '':
        com_ports = list_ports()
        port = test_ports( com_ports)
        if port == '':
            port = com_ports[0]

    global packetHandler
    global portHandler
    portHandler = PortHandler(port)
    packetHandler = PacketHandler(0)
    condition = False
    if portHandler.openPort():
         print("Succeeded to open the port")
    else:
        print("Failed to open the port")
 
        quit()
    # Set port baudrate
    if portHandler.setBaudRate(BAUDRATE):
        print("Succeeded to change the baudrate")
        condition = True
    else:
        print("Failed to change the baudrate")
        quit()

    relax_all()
    # set protective torque time to 0.3s ( value * 10ms)
    #write_Motors(Motors, 35, 30)
    #write_Motors(Motors, 38, 30)
    # set output torque after overload triggered ( value from 0-100)
    #write_Motors(Motors, 34, 0)
    # sets the speed to a lower value in steps/s
    set_speed_all(400)

    # test the motors to see condition
    errors = 0
    for m in Motors:
        ID = m[1] 
        result = read(ID, curr_pos )
        if result is None:
            errors = errors +1
        result = read(ID, curr_pos )
        if result is None:
            errors = errors +1
    percent = 100* errors /( len(Motors)*2)
    print( ' Percentage of Motor read errors: ' + str(percent))

    return condition


#### Ping the servo with ID x
# Function returns true if ping or false if no ping

def ping(IDD):
    print("Try to Ping Motor: " + str(IDD) )
    data, com, error = packetHandler.ping(portHandler, IDD)

    if com != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(com))
        return False
    elif error != 0:
        print("%s" % packetHandler.getRxPacketError(error))
        return False
    else:
        print("[ID:%03d] ping Succeeded. SCServo model number : %d" % (IDD, data))
        return True


#### Write to register
# IDD is the servo ID
# reg is the register ( like torque = 40 )
# data is what to write to register
# returns true if sucessful

def write(IDD, reg, data):
    #print('writing motor '+str(IDD)+ ' register ' +str(reg) )
    # finds the motor from global variableF.
    motorr = m1
    global Motors
    for x in Motors:
        if x[1] == IDD:
            motorr = x
# if we are relaxing motor, set movement to -1
            if reg == 40:
                if data == 0:
                    x[7] = -1
                if data == 1:
                    x[7] = 1
# if we are moving motor, set movement to 1, and check limits
            if reg == 42:
                x[7] = 1
                limit_up = x[3]
                limit_down = x[4]
                if limit_up < limit_down:
                    x = limit_up
                    limit_up = limit_down
                    limit_down = x
                if data > limit_up:
                    data = limit_up
                if data < limit_down:
                    data = limit_down

    motor_typee = motorr[2]
    #print( "writing to motor " + str(motorr[1]))

    global packID
    if (motor_typee != packID ):   # different packet handler for different motor types
        global packetHandler
        packetHandler = PacketHandler(motor_typee)
        packID = motor_typee
    
    try:
        com, error= packetHandler.write2ByteTxRx(portHandler, IDD, reg, int(data))
        if com != COMM_SUCCESS:
           # print(str(IDD) + ' comm error: ' + str(com)  )
            com, error= packetHandler.write2ByteTxRx(portHandler, IDD, reg, int(data))
            
        if error != 0:
            #print(str(IDD) + ' error code: ' + str(error))
            com, error= packetHandler.write2ByteTxRx(portHandler, IDD, reg, int(data))
            
        else:
            return True
    except:
        print('serial write error')
        return False

#### Read from register
# IDD is the servo ID
# reg is the register ( like torque = 40 )
# returns the data or returns False

def read(IDD, reg):
    motorr = m1
    for x in Motors:
        if x[1] == IDD:
            motorr = x
    motor_typee = motorr[2]
    #print( "reading from motor " + str(motorr[1]))

    global packID
    if (motor_typee != packID ):   # different packet handler for different motor types
        global packetHandler
        packetHandler = PacketHandler(motor_typee)
        packID = motor_typee
    try:
        data, com, error= packetHandler.read2ByteTxRx(portHandler, IDD, reg)
        if com != COMM_SUCCESS:
            #print(str(IDD) + ' comm error: ' + str(com))
            data, com, error= packetHandler.read2ByteTxRx(portHandler, IDD, reg)
            
        elif error != 0:
            #print(str(IDD) + ' error code: ' + str(error))
            data, com, error= packetHandler.read2ByteTxRx(portHandler, IDD, reg)
            
        else:
            if reg == curr_pos:
                if ( motor_typee == 1 ):
                    scs_present_position = SCS_LOWORD(data)
                    scs_present_speed = SCS_HIWORD(data)
                    return scs_present_position
                else:
                    return data
            else:
                return data
    except: 
        print('serial read error')
        return False


#### Set motor position to middle (only for 360 rotation motors)
# middle position is 2047
# IDD is the servo ID
# returns true if sucessful

def set_mid(IDD):
    result = write(IDD, 40, 128)
    return result

def set_all_mid():
    for m in Motors:
        set_mid( m[1] )

## sets the speed of the Motors
def set_speed_all(speed):
    write_Motors(Motors, 46, speed)
    write(5, 46, speed*2)    ## some motors gear ratio of two
    write(31, 46, speed*2)
    write(41, 46, speed*2)

## sets a random set_speed
def set_speed_rand(IDD, speed):
    speed = speed* (random.random() + 0.5)
    write(IDD, 46, speed)

#### Pings all the motors in Motors list

def ping_all():
    for x in Motors:
        ping(x[1])

#### Write to same register for many motors
# motor_list = list of motor ID's
# reg = the register
# data_list =  the data to write to each motor

def write_motors( motor_list, reg , data_list ):
    for index, item in enumerate(motor_list):
        print(item)
        write( item , reg , data_list[index] )

# this one is for a list of motor objects
def write_Motors( motor_list, reg, data):
    for mm in motor_list:
        ID = mm[1]
        write(ID, reg, data)

#### Read from same register for many motors
# motor_list = list of motor ID's
# reg = the register
# data_list =  the data read from each motor

def read_motors( motor_list, reg ):
    data_list = []
    for index, item in enumerate(motor_list):
        data_list.append( read( item , reg ) )
    return data_list

#### Read Position
# IDD = the motor ID


### keeps reading a motor position updating every 0.5 seconds
def poll_pos( IDD ):
    while 1:

        data = read( IDD, curr_pos )
        print(" Motor "+ str(IDD)+" is at " + str(data))
        time.sleep(0.5)

def poll_all():
    t1 = time.time()
    while (time.time() - t1) < 10:
        datalist = []
        for m in Motors:
            data = read( m[1], curr_pos )
            short = " Motor "+ str(m[1])+" is at " + str(data)
            print(short)
        print(datalist)
        time.sleep(0.1)

#### relax all the motors
def relax(motID):
    write(motID, 40, 0)

def relax_all():
    for m in Motors:
        write( m[1] , 40, 0)

# relaxes all motors except motors in list_stiff
def relax_some( list_stiff ):
    for m in Motors:
        if m[1] not in list_stiff:
            write(m[1],40, 0)

def stiff_all():
    for m in Motors:
        write( m[1] , 40, 1)

def relax_motors( list_mot):
    for mm in list_mot:
        ID = mm[1]
        write(ID, 40, 0)

#### records motion data for given list of motors objects.
#### Duration is the length of recording
#### each frame of recording is around 500ms
#### returns a list of lists with [ID, position]
fps = 0.1                         
def record( list_m , duration):
    result = []
    t1 = time.time()
    while ( (time.time() - t1) < duration ):
        t2 = time.time()
        frame = []
        for mm in list_m:
            ID = mm[1]
            pos = read( ID, curr_pos )
            Item = [ID, pos]
            frame.append(Item)
        result.append(frame)
        delta = time.time() - t2
        delta = fps - delta        # time between frames determined by fps variable
        if delta > 0 :
            time.sleep(delta)
    return result


##### reads the serial ports
import glob
def list_ports():

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


### Close port
def closeport():
    portHandler.closePort()

## this function tries a list of serial ports and attempts to ping motor
## if one of the ports has motors, then it returns that port. 

def test_ports( list_ports ):
    global packetHandler
    global portHandler
    valid_port = ''
    

    for port in list_ports:    
        portHandler = PortHandler(port)
        packetHandler = PacketHandler(0)
        portHandler.setPacketTimeoutMillis(1000)
        
        if portHandler.openPort():
            if portHandler.setBaudRate(BAUDRATE):
                result = ping(2)
                if result == True:
                    valid_port = port
    
    return valid_port
                    

######## Movement Functions #############

import json

cur_path = os.path.dirname(__file__)

#### Gets data from the motion folder
# give the file name like: walk.txt
# files are found in motion folder

def get_data( name:str ):
    new_path = "motion/" + name
    data = open(new_path, 'r')
    result = eval( data.read() )
    data.close()
    return result

def save_data( name:str , data):
    new_path = "motion/" + name
    file = open(new_path, 'w')
    file.write( str(data))
    file.close()

### positions motors according data file (simple motions only)
# input is a list of lists [ Motor ID , position ]
# each frame is is played 500ms apart
# if we get position of -1, that means relax the motor,
#if position -2, means keep stiff after animation
# the data may not read properly and return False

def play_simple( name:str ):
    data = get_data( name )
    stiff_list = []
    # play each frame
    for frame in data:
        t1 = time.time()
        for m in frame:
            if m[1] == -1:    
                write(m[0], 40, 0)
            if m[1] == -2:
                stiff_list.append(m[0])
            x = 0
            if m[1] is False or m[1] is None:
                x = 1
            if m[1] != -1 and m[1] != -2 and x != 1 :  
                write( m[0] , goal_pos , m[1] )
        # make sure motors are not overloaded
        #time.sleep(0.2)
        #check_torque()

        t2 = time.time()
        diff = t2-t1
        diff = fps - diff   # time between frames is determined by fps variable
        if (diff >0):
            time.sleep(diff)
    relax_some(stiff_list)

# this function randomly moves a motor
# input: list of motors, move length, wait time
rrtime = time.time()
def random_move(move_list, length, wtime):
    global rrtime
    delta = time.time() - rrtime
    if delta > wtime :
        rrtime = time.time()

        if len(move_list) == 0:
            move_list = [2, 3, 4,10, 11, 12,13, 14, 15, 20, 21, 22, 23, 24, 25, 30, 31, 32, 33, 34, 40, 41, 42, 43, 44]
        mot = random.choice(move_list)
        current_pos = read(mot, curr_pos)
        delta = (random.random()-0.5 )* 2 * length
        goal = current_pos + delta
        #print('random motor move')
        write(mot, goal_pos, goal)
        time.sleep(0.5)
        check_torque()
        time.sleep(0.5)
        write(mot, 40, 0)


## ----------- Accelerometer Code for Khadas

def poll_acc():
    import subprocess 
    acc = subprocess.call('motion/accelerometer/acc')
    while 1:
        print(acc)
        time.sleep(0.2)




#### ------------ Test code ---------------
larm = [ m20, m21, m22, m23, m24, m25]
rarm = [m10, m11, m12, m13, m14, m15]
arms = larm + rarm
lleg = [ m40, m41, m42, m43, m44]
rleg = [m30, m31, m32, m33, m34]
legs = lleg + rleg
Torso = [m2, m3, m4, m5]
core =  [m2, m5, m10, m11, m20, m21, m30, m31, m40, m41]
core2 = core + [m3, m4, m12, m13, m22, m23, m32, m33, m42, m43 ]

if __name__ == "__main__":
    init_servos('/dev/ttyS3')
    animate_list = []
    record_time = 0.1
    control_on = True
    while control_on:
        command = input(" enter command: ")
        time.sleep(0.1)
        
        if (command == 'body'):
            time.sleep(1)
            print('start')
            result = record(Motors, record_time)
            animate_list = animate_list + result
            print('ok')
            
        if (command == 'core'):
            time.sleep(1)
            print('start')
            result = record(core, record_time)
            animate_list = animate_list + result
            print('ok')
            
        if (command == 'core2'):
            time.sleep(1)
            print('start')
            result = record(core2, record_time)
            animate_list = animate_list + result
            print('ok')

        if (command == 'arms'):
            time.sleep(1)
            print('start')
            result = record(arms, record_time)
            animate_list = animate_list + result
            print('ok')
            
        if (command == 'larm'):
            time.sleep(1)
            print('start')
            result = record(larm, record_time)
            animate_list = animate_list + result
            print('ok')
            
        if (command == 'rarm'):
            time.sleep(1)
            print('start')
            result = record(rarm, record_time)
            animate_list = animate_list + result
            print('ok')
            
        if (command == 'legs'):
            time.sleep(1)
            print('start')
            result = record(legs, record_time)
            animate_list = animate_list + result
            print('ok')
            
        if (command == 'lleg'):
            time.sleep(1)
            print('start')
            result = record(lleg, record_time)
            animate_list = animate_list + result
            print('ok')
            
        if (command == 'rleg'):
            time.sleep(1)
            print('start')
            result = record(rleg, record_time)
            animate_list = animate_list + result
            print('ok')
            
        if (command == 'torso'):
            time.sleep(1)
            print('start')
            result = record(Torso, record_time)
            animate_list = animate_list + result
            print('ok')


        if (command == 'relax'):
            relax_all()
            print('relaxed motors')

        if (command == 'stiff torso'):
            for mot in Torso:
                write(mot[1], 40, 1)
            print('torso torque on')

            # give command like 'play 2D0.m'
        if (command[0:4] == 'play'):
            X = command[5:]
            play_simple(X)
            print('playing: '+ str(X))

        # polls the position for 10s
        if (command == 'pollall'):
            poll_all()
        
        # polls the position for 10s
        if (command[0:4] == 'poll'):
            X = command[5:]
            t = 0
            while t< 50:
                t = t+0.5
                data = read(int(X), curr_pos)
                print('position: '+ str(data))
                time.sleep(0.1)

            # give a command like 'save 3C2' to save data in animate_list
        if (command[0:4] == 'save'):
            X = command[5:]
            save_data(X, animate_list)
            print('saving: '+ str(X))
            animate_list = []

        if (command[0:3] == 'mid'):
            X = command[4:]
            set_mid(int(X))
            print('setting to mid position: '+ str(X))

# this records a list of motors - write the ID with spaces in between
        if (command[0:6] == 'record'):
            X = command[7:]
            list_M = []
            list_m = X.split()
            for m in list_m:
                mot_ID = int(m)
                for M in Motors:
                    if M[1] == mot_ID:
                        list_M.append(M)

            result = record(list_M, record_time)
            animate_list = animate_list + result
            print(result)


        if (command == 'clear'):
            animate_list = []
            print('cleared animation data')

        if (command == 'ping'):
            ping_all()
            print('cleared aniamtion data')

           
        if (command[0:4] == 'time'):
            X = command[5:]
            record_time = float(X)
            print('Recording time Set to: '+ X)

        if (command == 'exit'):
            control_on = False
            
        if (command[0:4] == 'move' ):
            strings = command.split()
            motorid = int(strings[1])
            position = int(strings[2])
            write( motorid , goal_pos , position )
            print('ok')
        
        if (command[0:4] == 'read' ):
            strings = command.split()
            motorid = int(strings[1])
            try:
                register = int(strings[2])
            except:
                register = curr_pos
            dat = read( motorid , register )
            print( 'motor ' + strings[1] + ' says: ' + str(dat))
            print('ok')
            
        ## command for testing some random functions
        if (command == 'test' ):
            while 1:
                move_mouth( 'close' )
                time.sleep(0.1)
            

        if command == 'commands':
            print('time t , ping m, clear, record m1 m2 , mid m , save A, read m r ')
            print( 'poll m, allpoll, play A, stiff torso, relax, exit, move m p, test' )
            print(' body, rarm, larm, arms, lleg, rleg, legs, torso, core, core2 ')
