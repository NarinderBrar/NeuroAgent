import numpy as np
import nest
import pylab

import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

w_prox_neu = 50.
w_neu_neu = 0.

tau_m = 1.0
tau_syn_ex = 20.
tau_syn_in = 20.
C_m = 250.0

nest.ResetKernel()
nest.SetKernelStatus({'resolution': 1.})

p = {
    'E_L': -60.05, 'V_th': -60., 'tau_m': tau_m, 'tau_syn_ex': tau_syn_ex, 'tau_syn_in': tau_syn_in, 'C_m': C_m
}

sensors0 = nest.Create('iaf_psc_exp', 1, params=p)
sensors1 = nest.Create('iaf_psc_exp', 1, params=p)
sensors2 = nest.Create('iaf_psc_exp', 1, params=p)

syn_con_main0 = nest.Connect(sensors0, sensors1, syn_spec={
                             'model': 'stdp_synapse',  'weight': w_neu_neu, 'Wmax': 5.0})
syn_con_main1 = nest.Connect(sensors0, sensors2, syn_spec={
                             'model': 'stdp_synapse',  'weight': w_neu_neu, 'Wmax': 5.0})
syn_con_main0 = nest.Connect(sensors1, sensors0, syn_spec={
                             'model': 'stdp_synapse',  'weight': w_neu_neu, 'Wmax': 5.0})
syn_con_main1 = nest.Connect(sensors1, sensors2, syn_spec={
                             'model': 'stdp_synapse',  'weight': w_neu_neu, 'Wmax': 5.0})
syn_con_main0 = nest.Connect(sensors2, sensors0, syn_spec={
                             'model': 'stdp_synapse',  'weight': w_neu_neu, 'Wmax': 5.0})
syn_con_main1 = nest.Connect(sensors2, sensors1, syn_spec={
                             'model': 'stdp_synapse',  'weight': w_neu_neu, 'Wmax': 5.0})


multimeterS0 = nest.Create("multimeter", 1)
nest.SetStatus(multimeterS0, {"withtime": True, "record_from": ["V_m"]})
nest.Connect(multimeterS0, sensors0)

multimeterS1 = nest.Create("multimeter")
nest.SetStatus(multimeterS1, {"withtime": True, "record_from": ["V_m"]})
nest.Connect(multimeterS1, sensors1)

multimeterS2 = nest.Create("multimeter")
nest.SetStatus(multimeterS2, {"withtime": True, "record_from": ["V_m"]})
nest.Connect(multimeterS2, sensors2)

spikedetectorS = nest.Create("spike_detector", params={
                             "withgid": True, "withtime": True})
nest.Connect(sensors0, spikedetectorS)

spikedetectorA0 = nest.Create("spike_detector", params={
                              "withgid": True, "withtime": True})
nest.Connect(sensors2, spikedetectorA0)

spikedetectorA1 = nest.Create("spike_detector", params={
                              "withgid": True, "withtime": True})
nest.Connect(sensors1, spikedetectorA1)

# s0
spikes = []
for i in range(100):
    spikes.append(float(i)+1.0)

for i in range(100):
    spikes.append(float(i)+500.0)

spikegenerator = nest.Create('spike_generator')
nest.SetStatus(spikegenerator, {'spike_times': spikes})
nest.Connect(spikegenerator, sensors0, syn_spec={'weight': w_prox_neu})

# s1
spikes = []
for i in range(100):
    spikes.append(float(i)+1.0)

spikegenerator = nest.Create('spike_generator')
nest.SetStatus(spikegenerator, {'spike_times': spikes})
nest.Connect(spikegenerator, sensors1, syn_spec={'weight': w_prox_neu})

nest.Simulate(1000.0)

fig, axs = pylab.subplots(4, figsize=(18, 10))
fig.suptitle('title')
pylab.grid(True)

# pylab.figure("Sensory")
dmm = nest.GetStatus(multimeterS0)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]
axs[0].plot(ts, Vms, "-b")

# pylab.figure("Actors")
dmm = nest.GetStatus(multimeterS1)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]
axs[1].plot(ts, Vms, "-g")

# pylab.figure("Actors3")
dmm = nest.GetStatus(multimeterS2)[0]
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

a = nest.GetDefaults("stdp_synapse")
print(a)

synIn = nest.GetConnections(sensors0, sensors1)
synInW = nest.GetStatus(synIn, keys='weight')
print('weight:s0-s1', synInW)

synIn = nest.GetConnections(sensors0, sensors2)
synInW = nest.GetStatus(synIn, keys='weight')
print('weight:s0-s2', synInW)

synIn = nest.GetConnections(sensors1, sensors2)
synInW = nest.GetStatus(synIn, keys='weight')
print('weight:s1-s2', synInW)
