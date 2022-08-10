import numpy as np
import nest
import pylab

import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

synapse_weight = 10.0

tau_m = 1.
tau_syn = 20.
J = 10.
C_m = 250.0

max_rate = 50.

nest.ResetKernel()
nest.SetKernelStatus({'resolution': 1.})

def get_current_offset_0(weight, rate, tau_m, tau_syn, C_m):
    return weight / C_m * rate * tau_m * tau_syn * 1e-3

def get_current_offset_1(weight, rate, tau_m, tau_syn, C_m):
    return weight / C_m * rate * tau_m * tau_syn * 1e-2

sensors0 = nest.Create('iaf_psc_exp', 1, 
{
    'E_L': -60. + get_current_offset_0(-J, max_rate / 2., tau_m, tau_syn, C_m),
    'V_th': -60., 'tau_m': tau_m, 'tau_syn_ex': tau_syn, 'tau_syn_in': tau_syn, 'C_m': C_m
})

actors0 = nest.Create('iaf_psc_exp', 1, 
{
    'E_L': -60., 'V_th': -60., 'tau_m': 10 * tau_m, 'tau_syn_ex': 2.2, 'tau_syn_in': 2.0
})

sensors1 = nest.Create('iaf_psc_exp', 1, 
{
    'E_L': -60.1,
    'V_th': -60., 'tau_m': tau_m, 'tau_syn_ex': tau_syn, 'tau_syn_in': tau_syn, 'C_m': C_m
})

syn_con_main0 = nest.Connect(sensors0, actors0, syn_spec={'model': 'stdp_synapse',  'weight': synapse_weight})
syn_con_main1 = nest.Connect(sensors0, sensors1, syn_spec={'model': 'stdp_synapse',  'weight': synapse_weight})

multimeterS = nest.Create("multimeter",1)
nest.SetStatus(multimeterS, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeterS, sensors0)

multimeterA0 = nest.Create("multimeter")
nest.SetStatus(multimeterA0, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeterA0, actors0)

multimeterA1 = nest.Create("multimeter")
nest.SetStatus(multimeterA1, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeterA1, sensors1)

spikedetectorS = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
nest.Connect(sensors0, spikedetectorS)

spikedetectorA0 = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
nest.Connect(actors0, spikedetectorA0)

spikedetectorA1 = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
nest.Connect(sensors1, spikedetectorA1)

#spike fo 0
spikes = []
for i in range(10):
   spikes.append(float(i)+1.0)

# for i in range(10):
#    spikes.append(float(i)+20.0)

spikegenerator = nest.Create('spike_generator')
nest.SetStatus(spikegenerator, {'spike_times': spikes})
nest.Connect(spikegenerator, sensors0, syn_spec={'weight': 10})

#spike fo 1
# spikes1 = []
# for i in range(100):
#    spikes1.append(float(i)+1.0)

# spikegenerator = nest.Create('spike_generator')
# nest.SetStatus(spikegenerator, {'spike_times': spikes1})
# nest.Connect(spikegenerator, actors0, syn_spec={'weight': 10})
# nest.Connect(spikegenerator, sensors1, syn_spec={'weight': 10})

nest.Simulate(200.0)

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

# a = nest.GetStatus(sensors0, keys='E_L')
# print(a)