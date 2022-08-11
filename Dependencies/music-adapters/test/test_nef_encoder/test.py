#!/usr/bin/python
import nest
from nest import raster_plot as rplt
from nest import voltage_trace as volt
import pylab as plt
import os
import time
import numpy as np
import yaml

from mpi4py import MPI

comm = MPI.COMM_WORLD

nest.ResetKernel()
startbuild = time.time()


nest.SetKernelStatus({"resolution": 1., "print_time": True, "overwrite_files": True})
nest.set_verbosity("M_FATAL")

proxy_sensory = nest.Create('music_event_in_proxy', 100)
nest.SetStatus(proxy_sensory, [{'port_name': 'sensory', 'music_channel': c} for c in range(100)])
nest.SetAcceptableLatency('sensory', 2.0)

print("Create devices")

sd_sensory = nest.Create("spike_detector", 1)


print("Connect")

# proxy to sd
nest.Connect(proxy_sensory, sd_sensory)


print("Simulate")

comm.Barrier()

nest.Simulate(10000)


print("Done")

rplt.from_device(sd_sensory)
rplt.show()





