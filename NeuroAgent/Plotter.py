#!/usr/bin/env python

import time as time
import numpy as np
import zmq

import matplotlib.pyplot as plt

class Plotter():

	def  __init__(self):

		ctx = zmq.Context()

		self.sub = ctx.socket(zmq.SUB)
		self.sub.connect('tcp://localhost:5560')
		self.sub.setsockopt(zmq.SUBSCRIBE, b'')
		self.sub.RCVTIMEO = 1000

		self.size = 12
		self.stepCount = 0
		self.canRefresh = False

		self.i = 0
		self.start()

		while True:
			self.recData()
			self.plot()

	def start(self):
		self.t_=[[0,0,0,0,0,0,0,0,0,0,0,0]]
		self.o_=[[1,2,3,4,5,6,7,8,9,10,11,12]]
		self.a_=[[14,15,16,17,18,19,20,21,22,23,24,25]]

		self.obs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
		self.act = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

		plt.style.use('fivethirtyeight') # For better style

	def plot(self):
		
		t = [self.stepCount]*self.size
		self.t_.append(t)
		self.t_=self.t_[-100:]

		self.o_.append(self.obs)      
		self.o_=self.o_[-100:]

		self.a_.append(self.act)      
		self.a_=self.a_[-100:]

		plt.plot(self.t_, self.o_, '|', color='r')
		plt.plot(self.t_, self.a_, '|', color='b')

		plt.draw()
		plt.pause(0.001)

	def recData(self):
		self.i+=1
		self.stepCount+=1

		# if self.i < 10:
		# 	return
		# self.i = 0

		msg = {}
		try:
			msg = self.sub.recv_json()
		except zmq.error.Again: 
			return

		self.obs = msg["obs"]
		self.act = msg["act"]

		print(self.obs)
		print(self.act)

		if len(self.act)==self.size:
			for k in range(1,self.size):
				v = (float)(self.obs[k-1]*k)
				if self.obs[k-1] == 0.0:
					self.obs[k-1] = None
				else:
					self.obs[k-1] = v

			for k in range(1,self.size):
				v = (float)((self.act[k-1]*k)+14)
				if self.act[k-1] == 0.0:
					self.act[k-1] = None
				else:
					self.act[k-1] = v

		print(self.obs)
		print(self.act)


plotter = Plotter()