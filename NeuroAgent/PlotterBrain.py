#!/usr/bin/env python

import time as time
import numpy as np
import zmq
from cycler import cycler
import matplotlib.pyplot as plt

class PlotterBrain():

	def  __init__(self):

		ctx = zmq.Context()

		self.sub = ctx.socket(zmq.SUB)
		self.sub.connect('tcp://localhost:5562')
		self.sub.setsockopt(zmq.SUBSCRIBE, b'')
		self.sub.RCVTIMEO = 1000

		self.ts = []
		self.t = []
		self.t2 = []
		self.mmInV1 = []
		self.mmInV2 = []
		self.w1 = []
		self.w2 = []

		fig,self.a =  plt.subplots(2,2)

		plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))
		plt.style.use('fivethirtyeight')

		self.a[0][0].set_xlabel('mp : salmon')
		self.a[0][0].set_ylabel('time')
		self.a[1][0].set_xlabel('mp : microwave')
		self.a[1][0].set_ylabel('time')

		self.a[0][1].set_xlabel('sw : actions')
		self.a[0][1].set_ylabel('time')
		self.a[1][1].set_xlabel('sw : objects')
		self.a[1][1].set_ylabel('time')
		while True:
			self.recData()
			self.plot()
			

	def plot(self):
		
		#plt.plot(self.ts, self.mmInV1, color='r')
		self.a[0][0].clear()
		self.a[0][0].plot(self.ts, self.mmInV1, linewidth=2)
		self.a[1][0].clear()
		self.a[1][0].plot(self.ts, self.mmInV2,linewidth=2)

		self.a[0][1].clear()
		self.a[0][1].plot(self.t, self.w1, linewidth=2)
		self.a[1][1].clear()
		self.a[1][1].plot(self.t2, self.w2, linewidth=2)

		plt.draw()
		plt.pause(0.001)
		#plt.clf()

	def recData(self):

		msg = {}
		try:
			msg = self.sub.recv_json()
		except zmq.error.Again: 
			return

		self.ts = msg["ts"]
		self.t.append(msg["t"])
		self.t2.append(msg["t"][-10:])
		self.mmInV1 = msg["mmInV1"]
		self.mmInV2 = msg["mmInV2"]
		self.w1.append(msg["w1"])
		self.w2.append(msg["w2"])

		print(msg["w1"])

plotterBrain = PlotterBrain()