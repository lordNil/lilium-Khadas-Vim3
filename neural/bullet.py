import pybullet as p
import time
import pybullet_data
import random
import time

robotID = 0
startPos = [0,0,1.3]
startOrientation = p.getQuaternionFromEuler([0,0,0])
joint_list = [0,1,2,3,4,5,6,7,8,9,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
joint_data = []
joint_pos  = []
joint_vel  = []
joint_goal = []

t1 = 0
t2 = 0

random.seed()




# start the simulation and returns the robot object
def start_sim():

    physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version or p.GUI for graphical
    p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
    p.setGravity(0,0,-10)
    robotID = p.loadURDF("human.urdf",startPos, startOrientation)
    planeId = p.loadURDF("plane.urdf")
    #p.setTimeStep(0.0166) default is 240hz, the 0.0166 is 60hz
    joint_num = p.getNumJoints(bodyUniqueId = robotID)
    #print(joint_num)
    print('simulation initialized')


# step the simulation with the robot object and joint position goals
# joint goals is a list of 31 elements with each joint position
# if joint goals =[] then will not be moved
# returns the joint positions as list
def step_sim( joint_goal):
    t1 = time.time()
    joint_data = p.getJointStates(bodyUniqueId = robotID, jointIndices = joint_list)
    joint_pos  = []
    joint_vel = []
    for x in joint_data:
        joint_pos.append(x[0])
        joint_vel.append(x[1])
#    for j in joint_pos:
#        rand = random.randint(-5,5)/50
#        joint_goal.append([float(j + rand)])
    if (len(joint_goal) != 0):
        p.setJointMotorControlMultiDofArray(bodyUniqueId = robotID, jointIndices = joint_list, controlMode = p.POSITION_CONTROL, targetPositions = joint_goal)
    
    t2 = time.time()
    t2 = t2-t1
    #print(" simulation calc time = " + str(t2))
    t1 = time.time()
    
    p.stepSimulation()
    t2 = time.time()
    t2 = t2-t1
    #print(" simulation step time = " + str(t2))

    return joint_pos
 

def end_sim():
    p.disconnect()


# ------------- test code --------



