#!/usr/bin/env python

import time as time
import numpy as np
import zmq

from simulation.unity_simulator import comm_unity

class BodySimulation():

	def  __init__(self):
		self.preprocess = -1
		self.process = -1
		self.preprocessSend = "p-1"

		ctx = zmq.Context()

		self.sub = ctx.socket(zmq.SUB)
		self.sub.connect('tcp://localhost:5560')
		self.sub.setsockopt(zmq.SUBSCRIBE, b'')
		self.sub.RCVTIMEO = 1000

		self.pub = ctx.socket(zmq.PUB)
		self.pub.bind('tcp://*:5561')
		
		self.tmp = 0

		self.start()

		while True:
			self.sendData() 
			self.recData()

	def makeFree(self):
		self.busy = False
		#print("BodySimulation: MakeFree")
			
	def reset_Tasks(self):
		self.tasks = [False, False, False, False, False ] 
		#print("BodySimulation: ResetTasks")

	def start(self):
		self.tasks = [False, False, False, False, False ] 
		self.tao = ["0","1","2","3","4","walk","grab","open","putin","close","salmon","microwave"]

		self.busy = False

		self.comm = comm_unity.UnityCommunication()
		#print("BodySimulation: init")

	def trainingSetup(self):
		self.comm.reset(0)
		
		self.comm.add_character('Chars/Female2', initial_room='kitchen', position=[-3, 0, -3])
		self.comm.add_character('Chars/Male2', initial_room='kitchen', position=[-2, 0, -4])
		
		print("BodySimulation: trainingSetup")

	def train(self, taskId):

		if self.busy:
			return

		print("BodySimulation: Training: Task ", taskId)
		
		if taskId == 0:
			self.makeFree()
			self.busy = True

			script0 = ['<char0> [walk] <salmon> (328)']
			self.tasks[taskId] = self.comm.render_script(script0, recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])

		if taskId == 1:
			self.makeFree()
			self.busy = True

			script1 = ['<char0> [grab] <salmon> (328)']
			self.tasks[taskId] = self.comm.render_script(script1, recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])
			
		if taskId == 2:
			self.makeFree()
			self.busy = True

			script2 = ['<char0> [open] <microwave> (314)']
			self.tasks[taskId] = self.comm.render_script(script2, recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])

		if taskId == 3:
			self.makeFree()
			self.busy = True

			script3 = ['<char0> [putin] <salmon> (328) <microwave> (314) | <char1> [walkforward]']
			self.tasks[taskId] = self.comm.render_script(script3, recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])

		if taskId == 4:
			self.makeFree()
			self.busy = True

			script4 = ['<char0> [close] <microwave> (314) | <char1> [walkforward]  | <char1> [turnleft']
			self.tasks[taskId] = self.comm.render_script(script4, recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])
			
	def doingSetup(self):
			#print("BodySimulation: Doing: Setup ")
			self.comm.reset(0)

			self.comm.add_character('Chars/Male2', initial_room='kitchen', position=[-3, 0, -3])
			self.comm.add_character('Chars/Female2', initial_room='kitchen', position=[-2, 0, -4] )

	def doing(self, spks):

		if self.busy:
			return

		actSpikes = np.array(spks)

		tks = actSpikes[0:5]
		taskMax = np.amax(tks)
		if taskMax < 2: 
			return

		taskId = np.where(tks == taskMax)[0][0]

		#print("BodySimulation: Doing: Task ", taskId)
		
		acts = actSpikes[5:10]
		actMax = np.amax(acts)
		if actMax < 2: 
			return
		actionId = np.where(acts == actMax)[0][0]

		action = (self.tao[actionId+5])
		#print("BodySimulation: Doing: action ", actionId)

		objs = actSpikes[10:12]
		objMax = np.amax(objs)
		if objMax < 2:
			return
		objectId = np.where(objs == objMax)[0][0]
		object = (self.tao[objectId+10])
		#print("BodySimulation: Manipulating: object ", objectId)

		self.busy = True
		
		script0 = ['<char0> [' + action + '] <'+ object +'> (328)']
		
		if taskId == 3:
			script0 = ['<char0> [putin] <salmon> (328) <microwave> (314)']
		if taskId == 2:
			self.tasks[taskId] = self.comm.render_script(['<char0> [walk] <microwave> (314)'], recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])
		if taskId == 4:
			self.tasks[taskId] = self.comm.render_script(['<char0> [walk] <microwave> (314)'], recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])

		print(script0)
		self.tasks[taskId] = self.comm.render_script(script0, recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])

		if taskId == 4:
			s, graph = self.comm.environment_graph()
			sink_id = [node['id'] for node in graph['nodes'] if node['class_name'] == 'sink'][0]
			self.tasks[taskId] = self.comm.render_script(['<char0> [walk] <sink> ({})'.format(sink_id)], recording=True, frame_rate=10, camera_mode=["PERSON_FROM_BACK"])

	def recData(self):

		msg = {}
		try:
			msg = self.sub.recv_json()
		except zmq.error.Again: 
			return

		self.process = (int)(msg["process"])
		taskId = (int)(msg["taskId"])
		spikes = msg["spikes"]
		
		print("BodySimulation: process: ", self.process,"pre-process:" ,self.preprocess,"taskId:" ,taskId, "spikes: ",spikes )
		
		if self.process != self.preprocess:
			if self.process == 0:
				self.start()
				self.preprocessSend = "p0"
			elif self.process == 1:
				self.trainingSetup()
				self.preprocessSend = "p1"
			elif self.process == 2:
				self.train(taskId)
				self.preprocessSend = "p2"
			elif self.process == 3:
				self.doingSetup()
				self.preprocessSend = "p3"			
			elif self.process == 4:
				self.doing(spikes)
				self.preprocessSend = "p4"
			elif self.process == 5:
				self.makeFree()
				self.preprocessSend = "p5"
			elif self.process == 6:
				self.reset_Tasks()
				self.preprocessSend = "p6"
		
		# else:
		# 	if self.process==4:
		# 		self.tmp +=1
		# 		if self.tmp > 10:
		# 			self.doing(spikes)

		self.preprocess = self.process

	def sendData(self):
		msgS = {'is_busy': self.busy, 'tasks': self.tasks, 'preprocess': self.process }
		self.pub.send_json(msgS)

bodySimulation = BodySimulation()