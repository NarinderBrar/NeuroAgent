import numpy as np
import gym
from gym import spaces
from simulation.unity_simulator import comm_unity

class FooEnv(gym.Env):

  metadata = {'render.modes': ['human']}

  def __init__(self, grid_size=10):
    super(FooEnv, self).__init__()

    YOUR_FILE_NAME = "/home/narinder/Documents/virtualhome/src/virtualhome/simulation/unity_simulator/linux_exec/linux_exec.v2.2.4.x86_64" # Your path to the simulator
    port= "8080"
    
    self.comm = comm_unity.UnityCommunication(file_name=YOUR_FILE_NAME, port=port)
    
    self.comm.reset(0)
    self.comm.add_character('Chars/Male2')

    self.obs = [1,0]
    self.act = [0,0]
    self.activity = "none"
    self.walkDone = False
    self.turnDone = False

    self.stepCount = 0
    
    n_actions = 2
    self.action_space = spaces.Discrete(n_actions)
    self.low = np.array([0, 0], dtype=np.float32)
    self.high = np.array([1, 1], dtype=np.float32)
        
    self.observation_space = spaces.Box(self.low, self.high, dtype=np.float32)

  def reset(self):
    print("reset")

    self.obs = [1,0]
    self.act = [0,0]
    self.activity = "none"
    self.walkDone = False
    self.turnDone = False

    self.stepCount = 0
    return np.array(self.obs).astype(np.float32)

  def step(self, action):
    self.act = action
    
    if self.stepCount > 1000:
        done = True

    if self.walkDone:
      self.obs = [0,1]
    if self.turnDone:
      self.obs = [0,0]

    done = False
    reward = 1
    info = {}
    
    self.stepCount+=1

    return np.array(self.obs).astype(np.float32), reward, done, info

  def render(self, mode='console'):
   if len(self.act)>1:
    if self.act[0] == 1 and not self.walkDone and self.activity !="walking":
      print("walking")
      print("\n")
      self.activity="walking"
      script = ['<char0> [WalkForward] ({})']
      self.walkDone, message = self.comm.render_script(script, recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])
      
    if self.act[1] == 1 and not self.turnDone and self.activity!="turning":
      script = ['<char0> [WalkForward] ({})']
      self.walkDone, message = self.comm.render_script(script, recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])
      self.activity="turning"
      print("turning")

  def close(self):
    pass
    