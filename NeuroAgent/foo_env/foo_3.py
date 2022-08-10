import numpy as np
import gym
import time
from threading import Thread, Event
#import bodies

import zmq

from gym import spaces
from simulation.unity_simulator import comm_unity
import matplotlib.pyplot as plt

class FooEnv(gym.Env):

  metadata = {'render.modes': ['human']}

  def __init__(self, grid_size=10):
    super(FooEnv, self).__init__()

    self.start_time = time.time()
    self.task_start_time = time.time()
    self.wait_start_time = time.time()

    self.totalTime = 60
    self.seconds = self.totalTime
    self.size = 12

    self.obs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    self.act = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
    self.spikes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    self.preprocess = -1
    self.process = -1
    self.processQueue = [0]

    self.curTask = 0

    self.training = True
    self.done = False
    self.doing = False
    self.trainingBusy = False

    self.stepCount = 0

    n_actions = 7

    self.action_space = spaces.Discrete(n_actions)
    self.low = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.float32)
    self.high = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=np.float32)
    self.observation_space = spaces.Box(self.low, self.high, dtype=np.float32)

    ctx = zmq.Context()
    self.pub = ctx.socket(zmq.PUB)
    self.pub.bind('tcp://*:5560')

    self.sub = ctx.socket(zmq.SUB)
    self.sub.connect('tcp://localhost:5561')
    self.sub.setsockopt(zmq.SUBSCRIBE, b'')
    self.sub.RCVTIMEO = 1000

    print("Gym: init")

  def reset(self):

    self.start_time = time.time()
    self.seconds = self.totalTime

    self.task_start_time = time.time()

    if self.training:
      self.processQueue.append(1)
    else:
      self.processQueue.append(3)

    self.obs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.act = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.spikes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    self.curTask = 0

    self.done = False

    self.stepCount = 0

    print("Gym: reseting")

    return np.array(self.obs).astype(np.float32)

  def step(self, action):

    if not isinstance(action, int):
      self.act = action

    #Time
    current_time = time.time()

    self.elapsed_time = int(current_time - self.start_time)
    self.elapsed_task_time = int(current_time - self.task_start_time)

    current_time = time.time()
    self.elapsed_wait_time = (current_time - self.wait_start_time)

    # Training
    if self.training:
      if self.curTask == 0:
        self.obs = [1, 0, 0, 0, 0,  1, 0, 0, 0, 0,  1, 0]
      if self.curTask == 1:
        self.obs = [0, 1, 0, 0, 0,  0, 1, 0, 0, 0,  1, 0]
      if self.curTask == 2:
        self.obs = [0, 0, 1, 0, 0,  0, 0, 1, 0, 0,  0, 1]
      if self.curTask == 3:
        self.obs = [0, 0, 0, 1, 0,  0, 0, 0, 1, 0,  1, 1]
      if self.curTask == 4:
        self.obs = [0, 0, 0, 0, 1,  0, 0, 0, 0, 1,  0, 1]

    # Doing
    else :
      if self.curTask == 0:
        self.obs = [1, 0, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0]
      if self.curTask == 1:
        self.obs = [0, 1, 0, 0, 0,  0, 0, 0, 0, 0,  0, 0]
      if self.curTask == 2:
        self.obs = [0, 0, 1, 0, 0,  0, 0, 0, 0, 0,  0, 0]
      if self.curTask == 3:
        self.obs = [0, 0, 0, 1, 0,  0, 0, 0, 0, 0,  0, 0]
      if self.curTask == 4:
        self.obs = [0, 0, 0, 0, 1,  0, 0, 0, 0, 0,  0, 0]

    print(self.act)

    if len(self.act)==self.size:
      for i in range(self.size):
        self.spikes[i]+=self.act[i]

    if self.elapsed_time > self.seconds:
        print("Gym: Finished " + str(int(self.elapsed_time))  + " seconds")
        self.done = True
        exit()

    print("\n")
    print("observ:",self.obs)
    print("action:",self.act)
    print("spkise:",self.spikes)

    self.stepCount+=1

    reward = 1
    info = {}

    return np.array(self.obs).astype(np.float32), reward, self.done, info

  def render(self, mode='console'):

    if self.stepCount % 10 == 0:
      msg = {'process': self.process, 'taskId': self.curTask, 'spikes': self.spikes, 'stepCount': self.stepCount, 'obs': self.obs, 'act': self.act}
      print(msg)

      self.pub.send_json(msg)

      msg = {}
      try:
        msg = self.sub.recv_json()
      except zmq.error.Again:
        #print("waiting..")
        return

      is_busy = msg["is_busy"]
      tasks = msg["tasks"]
      self.preprocess = msg["preprocess"]

      print("Gym: process: ", self.process, "pre-process:" , self.preprocess, "tasks:" , tasks, "is_busy: ",is_busy,"curTask: ", self.curTask )

      # Training
      if self.training:
        if not tasks[self.curTask] and not self.trainingBusy:
            self.processQueue.append(2)
            print("Training Task: ", self.curTask)
            self.trainingBusy = True

        elif tasks[self.curTask] and is_busy and self.trainingBusy:
          self.processQueue.append(5)
          print("Training Reset: ", self.curTask)
          self.curTask +=1
          self.trainingBusy = False

          #End Training
          if self.curTask > 4:
            self.task_start_time = time.time()
            self.training = False
            self.done = True
            self.curTask = 0
            self.processQueue.append(6)
            print("Training End")
            return

      # Doing
      elif len(self.act)==self.size and not self.doing:
        if not tasks[self.curTask]:
          self.task_start_time = time.time()
          self.processQueue.append(4)
          print("Doing : ", self.curTask)
          print("Process Queue : ", self.processQueue)
          self.doing = True

      elif tasks[self.curTask] and is_busy and self.doing:
        self.processQueue.append(5)
        print("Doing : ", self.curTask)
        self.spikes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if self.curTask < 4:
          self.curTask +=1
          self.doing = False
        else:
          self.done = True

      if self.process == self.preprocess:
        if len(self.processQueue) > 0:
          if  self.elapsed_wait_time > 1:
            self.wait_start_time = time.time()
            self.process = self.processQueue.pop(0)


  def close(self):
    pass
    

