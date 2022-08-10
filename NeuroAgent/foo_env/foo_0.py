import numpy as np
import gym
import time
from gym import spaces
from simulation.unity_simulator import comm_unity

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class FooEnv(gym.Env):

  metadata = {'render.modes': ['human']}

  def __init__(self, grid_size=10):
    super(FooEnv, self).__init__()

    print("Gym: init")

    self.start_time = time.time()
    self.totalTime = 25
    self.seconds = self.totalTime
    self.size = 12

    self.obs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    self.act = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    self.spikes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    self.spiked = False

    # self.x_=[[0,0,0,0,0,0,0,0,0,0,0,0,0]]
    # self.y_=[[1,2,3,4,5,6,7,8,9,10,11,12,13]]
    # self.z_=[[1.25,2.25,3.25,4.25,5.25,6.25,7.25,8.25,9.25,10.25,11.25,12.25,13.25]]

    self.stepCount = 0
    
    n_actions = 7

    self.action_space = spaces.Discrete(n_actions)
    self.low = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.float32)
    self.high = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=np.float32)
    self.observation_space = spaces.Box(self.low, self.high, dtype=np.float32)

  def reset(self):
    print("Gym: reset")
    self.start_time = time.time()
    self.seconds = self.totalTime
  
    self.obs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.act = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.spikes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.spiked = False

    self.stepCount = 0
    return np.array(self.obs).astype(np.float32)

  def step(self, action):
    self.act = action
  
    current_time = time.time()
    elapsed_time = int(current_time - self.start_time)

    s = 5
    tt = 1
    # Training
    if elapsed_time == s:
      self.obs = [1, 0, 0, 0, 0,  1, 0, 0, 0, 0,  1, 0]
    if elapsed_time == (s+tt*1):
      self.obs = [0] * self.size

    if elapsed_time == (s+tt*32):
      self.obs = [0, 1, 0, 0, 0,  0, 1, 0, 0, 0,  1, 0]
    if elapsed_time == (s+tt*3):
      self.obs = [0] * self.size

    if elapsed_time == (s+tt*4):
      self.obs = [0, 0, 1, 0, 0,  0, 0, 1, 0, 0,  0, 1]
    if elapsed_time == (s+tt*5):
      self.obs = [0] * self.size

    if elapsed_time == (s+tt*6):
      self.obs = [0, 0, 0, 1, 0,  0, 0, 0, 1, 0,  1, 0]
    if elapsed_time == (s+tt*7):
      self.obs = [0] * self.size

    if elapsed_time == (s+tt*8):
      self.obs = [0, 0, 0, 0, 1,  0, 0, 0, 0, 1,  0, 1]
    if elapsed_time == (s+tt*9):
      self.obs = [0] * self.size

    # Activating
    if elapsed_time == (s+tt*10) and not self.spiked:
      self.obs = [0, 0, 1, 0, 0,  0, 0, 0, 0, 0,  0, 0]
      self.spiked = True

    # Activating
    if self.spiked:
      if len(self.act)==self.size:
        for i in range(self.size):
          self.spikes[i]+=self.act[i]
    
    done = False
    if elapsed_time > self.seconds:
        print("Gym: Finished " + str(int(elapsed_time))  + " seconds")
        print(self.spikes)
        done = True
        exit()

    reward = 1
    info = {}
    
    self.stepCount+=1

    return np.array(self.obs).astype(np.float32), reward, done, info

  def render(self, mode='console'):
  #  if len(self.act)==self.size:
  #   t = [self.stepCount]*self.size
  #   self.x_.append(t)
  #   self.x_=self.x_[-100:]

  #   for k in range(1,self.size):
  #      self.obs[k-1] = (self.obs[k-1]*k)
  #   self.z_.append(self.obs)      
  #   self.z_=self.z_[-100:]
  #   plt.plot(self.x_, self.z_, '|', color='r')

  #   for k in range(1,self.size):
  #      self.act[k-1] = (self.act[k-1]*k)+0.30 
  #   self.y_.append(self.act)      
  #   self.y_=self.y_[-100:]
  #   plt.plot(self.x_, self.y_, '|', color='b')

  #   plt.draw()
  #   plt.pause(0.01)
  #   plt.clf()
    pass
  
  def close(self):
    pass
    