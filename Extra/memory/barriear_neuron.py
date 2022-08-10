import numpy as np
import nest
import pylab

import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

w0_max = 2500.0

nest.ResetKernel()

sensors_params = {
    'V_m': -70.0,
    'V_th': -55.0,
    'V_reset': -70.0,

    'tau_syn_ex': 0.2,
    'tau_syn_in': 2.0,
    }

actor_params_0 = {
    'V_m': -70.0,
    'V_th': -65.0,
    'V_reset': -70.0,
    
    'tau_syn_ex': 2.5,
    'tau_syn_in': 2.0,
    }

actor_params_1 = {
    'V_m': -70.0,
    'V_th': -55.0,
    'V_reset': -70.0,

    'tau_syn_ex': 0.2,
    'tau_syn_in': 2.0,
    }

sensors = nest.Create("iaf_psc_exp", params = sensors_params)
actors0 = nest.Create("iaf_psc_exp", params = actor_params_0)
actors1 = nest.Create("iaf_psc_exp", params = actor_params_1)
# actors2 = nest.Create("iaf_cond_alpha", params = INPUT_OUTPUT_PARAMS1)
# actors3 = nest.Create("iaf_cond_alpha", params = INPUT_OUTPUT_PARAMS1)

print(nest.GetDefaults("aeif_psc_exp"))

#nest.SetStatus(sensors, {"I_e": 376.0})
#nest.SetStatus(actors0, {"I_e": 376.0})

syn_con_main0 = nest.Connect(sensors, actors0, syn_spec={'model': 'stdp_synapse',  'weight': w0_max})
syn_con_main1 = nest.Connect(actors0, actors1, syn_spec={'model': 'stdp_synapse',  'weight': w0_max})
# syn_con_main2 = nest.Connect(actors1, actors2, syn_spec={'model': 'stdp_synapse',  'weight': w0_max})
# syn_con_main3 = nest.Connect(actors2, actors3, syn_spec={'model': 'stdp_synapse',  'weight': w0_max})

multimeterS = nest.Create("multimeter")
nest.SetStatus(multimeterS, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeterS, sensors)

multimeterA0 = nest.Create("multimeter")
nest.SetStatus(multimeterA0, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeterA0, actors0)

multimeterA1 = nest.Create("multimeter")
nest.SetStatus(multimeterA1, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeterA1, actors1)

spikedetectorS = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
nest.Connect(sensors, spikedetectorS)

spikedetectorA0 = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
nest.Connect(actors0, spikedetectorA0)

spikedetectorA1 = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
nest.Connect(actors1, spikedetectorA1)

spikes = []
for i in range(1000):
   spikes.append(float(i)+1.0)

spikegenerator = nest.Create('spike_generator')
nest.SetStatus(spikegenerator, {'spike_times': spikes})
nest.Connect(spikegenerator, sensors, syn_spec={'weight': 2500})

# spikes0 = []

# for i in range(100):    
#    spikes0.append(float(i)+1.0)

# spikegenerator1 = nest.Create('spike_generator')
# nest.SetStatus(spikegenerator1, {'spike_times': spikes0})
# nest.Connect(spikegenerator1, actors0, syn_spec={'weight': 2500})

#pgenerator = nest.Create("sinusoidal_poisson_generator ", params={"rate":200., "origin":0., "start":500., "stop": 2000., "amplitude":1.0,  })
#nest.Connect(pgenerator, sensors)

# a_EE = nest.GetConnections(sensors, actors)
# c_EE = nest.GetStatus(a_EE, keys='weight')
# print(c_EE)

nest.Simulate(1000.0)

fig, axs = pylab.subplots(4, figsize=(18, 10))
fig.suptitle('title')
pylab.grid(True)

# pylab.figure("Sensory")
dmm = nest.GetStatus(multimeterS)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]
axs[0].plot(ts, Vms, "-b")

#pylab.figure("Actors")
dmm = nest.GetStatus(multimeterA0)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]
axs[1].plot(ts, Vms, "-g")

#pylab.figure("Actors3")
dmm = nest.GetStatus(multimeterA1)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]
axs[2].plot(ts, Vms, "-r")

# pylab.figure("Actors ")
dSD = nest.GetStatus(spikedetectorS, keys="events")[0]
evs = dSD["senders"]
ts = dSD["times"]
axs[3].plot(ts, evs, ".", color="blue")

# pylab.figure("Actors1 Spikes")
dSD = nest.GetStatus(spikedetectorA0, keys="events")[0]
evs = dSD["senders"]
ts = dSD["times"]
axs[3].plot(ts, evs, ".", color="green")

# pylab.figure("Actors1 Spikes")
dSD = nest.GetStatus(spikedetectorA1, keys="events")[0]
evs = dSD["senders"]
ts = dSD["times"]
evs = np.insert(evs, 0, 0)
ts = np.insert(ts, 0, 0)
axs[3].plot(ts, evs, ".", color="red")

pylab.show()

#print(nest.GetDefaults("stdp_dopamine_synapse"))

# a_EE = nest.GetConnections(sensors, actors)
# c_EE = nest.GetStatus(a_EE, keys='weight')
# print(c_EE)