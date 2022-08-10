#!/usr/bin/env python

import sys
import music
import numpy
from itertools import takewhile, dropwhile

setup = music.Setup()

stoptime = setup.config("stoptime")
timestep = setup.config("timestep")

comm = setup.comm
rank = comm.Get_rank()

print("00000")

pin = setup.publishContInput("in")
data = numpy.array([0.0, 0.0], dtype=numpy.double)
pin.map(data, interpolate=False)

print("111111")

# out = setup.publishEventOutput("out")
# dataOut = numpy.array([-1], dtype=numpy.int)
# out.map(dataOut, base=rank)

print("22222")

runtime = setup.runtime(timestep)
mintime = timestep
maxtime = stoptime+timestep

print("33333")

start = dropwhile(lambda t: t < mintime, runtime)
times = takewhile(lambda t: t < maxtime, start)

for time in times:
    val = data
    sys.stdout.write("t={}\treceiver {}: received {}\n". format(time, rank, val))
    
    # dataOut[0] = rank
    # sys.stdout.write("t={}\tsender {}: Hello!\n".format(time, rank))