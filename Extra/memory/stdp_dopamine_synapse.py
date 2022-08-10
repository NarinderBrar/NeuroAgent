import numpy as np
import nest
import pylab

import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

w0_min = 0.1
w0_max = 1.0

nest.ResetKernel()

INPUT_OUTPUT_PARAMS = {'V_reset': -70.0,
                       'C_m': 250.0,
                       't_ref': 20.0,
                       'tau_syn_ex': 2.5,
                       'tau_syn_in': 2.5,
                       'E_ex': 0.0,
                       'E_in': -75.0,
                       'V_th': -60.0,}

sensors = nest.Create("iaf_cond_alpha", params = INPUT_OUTPUT_PARAMS)
dopamine = nest.Create("iaf_cond_alpha", params = INPUT_OUTPUT_PARAMS)
actors = nest.Create("iaf_cond_alpha", params = INPUT_OUTPUT_PARAMS)

print(nest.GetDefaults("iaf_cond_alpha"))


nest.SetStatus(sensors, {"I_e": 376.0})
#nest.SetStatus(dopamine, {"I_e": 376.0})

vt = nest.Create('volume_transmitter')

nest.CopyModel('stdp_dopamine_synapse', 'syn_main',
               {'Wmax': 2500.0,
                'Wmin': -2500.0,
                'tau_plus': 20.0,
                'A_minus': 1.0,
                'A_plus': -1.0,
                'b': 0.01,
                'tau_c': 10.0,
                'tau_n': 5.0,
                'vt': vt[0]})

syn_con_main = nest.Connect(sensors, actors, syn_spec={'model': 'syn_main',  'weight': {'distribution': 'uniform', 'low': w0_min, 'high': w0_max}})
nest.Connect(dopamine, vt[0:1])

multimeterS = nest.Create("multimeter")
nest.SetStatus(multimeterS, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeterS, sensors)

multimeterD = nest.Create("multimeter")
nest.SetStatus(multimeterD, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeterD, dopamine)

multimeterA = nest.Create("multimeter")
nest.SetStatus(multimeterA, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeterA, actors)

spikedetector = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
nest.Connect(actors, spikedetector)

pgenerator = nest.Create("poisson_generator", params={"rate":1000., "origin":0., "start":0., "stop": 10000.})
nest.Connect(pgenerator, dopamine)

# a_EE = nest.GetConnections(sensors, actors)
# c_EE = nest.GetStatus(a_EE, keys='weight')
# print(c_EE)

nest.Simulate(10000.0)

pylab.figure("Sensory")
dmm = nest.GetStatus(multimeterS)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]
pylab.plot(ts, Vms)

pylab.figure("Dopamine")
dmm = nest.GetStatus(multimeterD)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]
pylab.plot(ts, Vms)

pylab.figure("Actors")
dmm = nest.GetStatus(multimeterA)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]
pylab.plot(ts, Vms)

pylab.figure("Actors Spikes")
dSD = nest.GetStatus(spikedetector,keys="events")[0]
evs = dSD["senders"]
ts = dSD["times"]
pylab.plot(ts, evs, ".")
pylab.show()

#print(nest.GetDefaults("stdp_dopamine_synapse"))

a_EE = nest.GetConnections(sensors, actors)
c_EE = nest.GetStatus(a_EE, keys='weight')
print(c_EE)