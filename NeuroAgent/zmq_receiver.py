#!/usr/bin/env python

import numpy as np
import time as tm
import zmq

ctx = zmq.Context()

sub = ctx.socket(zmq.SUB)
sub.connect('tcp://localhost:5560')
sub.setsockopt(zmq.SUBSCRIBE, b'')

sub.RCVTIMEO = 1000

while True:
    try:
        msg = sub.recv_json()
    except zmq.error.Again:
        continue
    print('recv', msg)
    print(msg["process"])
    print(msg["taskId"])
    print(msg["spikes"][0])
    tm.sleep(0.5)