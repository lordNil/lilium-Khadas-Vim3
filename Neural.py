import gym
import numpy as np
from stable_baselines.ppo1 import PPO1
#import bullet
import time
import os

#------------------ Initialize------------------

# size of action and observation
HEIGHT = 1
WIDTH = 30

action_size = [ 6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6 ]
current_action = []
current_state = np.zeros((HEIGHT, WIDTH))
current_reward = 1

save = True
load = True

#-------------------- functions-------------------------
















## custom environment to work with their code
## this code runs and times when the neural network will get its data
class CustomEnv(gym.Env):
  #"""Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self):
    super(CustomEnv, self).__init__()

    #bullet.start_sim()

    self.action_space = gym.spaces.MultiDiscrete(  action_size  )

    self.observation_space = gym.spaces.Box(low=0, high=255, shape=
                    (HEIGHT, WIDTH ), dtype=np.uint8)

  def step(self, action):
    #result = bullet.step_sim( action )  needs action reformatted to list
    global current_action
    current_action = action
    observation = current_state
    reward = current_reward
    done = False
    info = {}
    time.sleep(0.2)
    return observation, reward, done, info

  def reset(self):
    #bullet.end_sim()
    #bullet.start_sim()
    action = []
    #result = bullet.step_sim( action )
    observation = current_state
    return observation

  def render(self, mode='human'):
    AA = 0
    #print(f'Step: {self.current_step}')

  def close (self):
    AA = []
    #bullet.end_sim()






#------------------ Running the Code ------------------

env = CustomEnv()

if ((load == True) and os.path.exists('PPOmodel.zip')):
    print('loading model')
    model = PPO1.load('PPOmodel.zip',env, verbose = 0)
else:
    print('Making New model')
    model = PPO1('MlpPolicy',env, verbose = 0)

print('training model')
t1 = time.time()
model.learn(total_timesteps=2000)
t2 = time.time()

if (save == True):
    model.save('PPOmodel.zip')

obs = env.reset()
t3 = time.time()
for i in range(2000):
  action, _states = model.predict(obs)
  obs, rewards, done, info = env.step(action)
t4 = time.time()


step_time = (t4-t3)/2000
update_time = (t2-t1) - (t4-t3)
print(" the step time is : " + str(step_time))
print(" the model update time is: " + str(update_time))
