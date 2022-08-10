#!/usr/bin/env python

################################################
#################### imports ###################
################################################
import nest
import pylab

import numpy as np

import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

################################################
################## parameters #################
################################################

simulation_time = 1000.

tau_m = 1.
tau_syn = 20.

w_prox_neu = 10.
w_neu_neu = 0.

C_m = 250.0
################################################
################## NEST Settings ###############
################################################
nest.ResetKernel()
nest.SetKernelStatus({'resolution': 1.})

################################################
################# Input Spikes #################
################################################
spikeGrp = []

spikes = []
for i in range(100):
    spikes.append(float(i)+1.0)
for i in range(100):
    spikes.append(float(i)+500.0)
spikeGrp.append(spikes)

spikes = []
for i in range(100):
    spikes.append(float(i)+1.0)
spikeGrp.append(spikes)

spikes = []
for i in range(100):
    spikes.append(float(i)+1.0)
spikeGrp.append(spikes)

spikes = []
for i in range(100):
    spikes.append(float(i)+1.0)
spikeGrp.append(spikes)

spikes = []
for i in range(100):
    spikes.append(float(i)+1.0)
spikeGrp.append(spikes)

################################################
################## neuron setup ################
################################################
neuIn = []
neuOutAct = []
neuOutObj = []

#62 spikes = E_L -60.1
#59 spikes = E_L -60.2

for i in range(5):
    inNeu = nest.Create('iaf_psc_exp',1, 
    {
        'E_L': -60.00,
        'V_th': -60., 'tau_m': tau_m, 'tau_syn_ex': tau_syn, 'tau_syn_in': tau_syn, 'C_m': C_m
        })
    neuIn.append(inNeu)

for i in range(5):
    outNeu = nest.Create('iaf_psc_exp', 1, 
    {
        'E_L': -60., 'V_th': -60., 'tau_m': 10 * tau_m, 'tau_syn_ex': 2.2, 'tau_syn_in': 2.0
    })
    neuOutAct.append(outNeu)

for i in range(3):
    outNeu = nest.Create('iaf_psc_exp', 1, 
    {
        'E_L': -60., 'V_th': -60., 'tau_m': 10 * tau_m, 'tau_syn_ex': 2.2, 'tau_syn_in': 2.0
    })
    neuOutObj.append(outNeu)

nest.SetStatus(neuIn[0], {"E_L": -60.01}) #62
nest.SetStatus(neuIn[1], {"E_L": -60.02}) #86
nest.SetStatus(neuIn[2], {"E_L": -60.03}) #112
nest.SetStatus(neuIn[3], {"E_L": -60.04}) #148
nest.SetStatus(neuIn[4], {"E_L": -60.05}) #176

################################################
##################### devices ##################
################################################

spkGenIn =[]
mmIn = []
mmOutAct = []
mmOutObj = []
spkDecIn =[]
spkDecOutAct =[]
spkDecOutObj =[]

for i in range(5):
    spikegenerator = nest.Create('spike_generator')
    spkGenIn.append(spikegenerator)
    nest.SetStatus(spkGenIn[i], {'spike_times': spikeGrp[i]})
    nest.Connect(spkGenIn[i], neuIn[i],syn_spec={'weight': w_prox_neu})

    mmI = nest.Create("multimeter")
    nest.SetStatus(mmI, {"withtime":True, "record_from":["V_m"]})
    mmIn.append(mmI)

    mmOA = nest.Create("multimeter")
    nest.SetStatus(mmOA, {"withtime":True, "record_from":["V_m"]})
    mmOutAct.append(mmOA)

    mmOO = nest.Create("multimeter")
    nest.SetStatus(mmOO, {"withtime":True, "record_from":["V_m"]})
    mmOutObj.append(mmOO)

    spikedetectorIn = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
    spkDecIn.append(spikedetectorIn)

    sdOutAct = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
    spkDecOutAct.append(sdOutAct)

    sdOutObj = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
    spkDecOutObj.append(sdOutObj)


################################################
##################### synapses #################
################################################
nest.Connect(neuIn[0], neuIn[1], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu})
nest.Connect(neuIn[0], neuIn[2], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu})
nest.Connect(neuIn[0], neuIn[3], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu})
nest.Connect(neuIn[0], neuIn[4], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu})

nest.Connect(neuIn[1], neuIn[2], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu})
nest.Connect(neuIn[1], neuIn[3], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu})
nest.Connect(neuIn[1], neuIn[4], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu})

nest.Connect(neuIn[2], neuIn[3], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu})
nest.Connect(neuIn[2], neuIn[4], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu})

nest.Connect(neuIn[3], neuIn[4], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu})

synoutAct = []
synoutObj = []
for i in range(5):#in
    for j in range(5):#OutAct
        synoutAct.append (nest.Connect(neuIn[i], neuOutAct[j], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu}))
    for k in range(3):#OutObj
        synoutObj.append (nest.Connect(neuIn[i], neuOutObj[k], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu}))


################################################
##################connectivity #################
################################################
for i in range(5):    
    nest.Connect(mmIn[i], neuIn[i])
    nest.Connect(neuIn[i], spkDecIn[i])

    nest.Connect(mmOutAct[i], neuOutAct[i])
    nest.Connect( neuOutAct[i], spkDecOutAct[i])

for i in range(3):
    nest.Connect(mmOutObj[i], neuOutObj[i])
    nest.Connect( neuOutObj[i], spkDecOutObj[i])

nest.Simulate(simulation_time)

################################################
##################### Plots ####################
################################################
figInV, plotInV = pylab.subplots(5, figsize=(9, 5))
figInV.suptitle('figInV')
# pylab.grid(True)

for i in range(5):
    dmm = nest.GetStatus(mmIn[i])[0]
    Vms = dmm["events"]["V_m"]
    ts = dmm["events"]["times"]
    plotInV[i].plot(ts, Vms, "-r")

figOutActV, plotOutActV = pylab.subplots(5, figsize=(9, 5))
figOutActV.suptitle('figOutActV')
# pylab.grid(True)

for i in range(5):
    dmm = nest.GetStatus(mmOutAct[i])[0]
    Vms = dmm["events"]["V_m"]
    ts = dmm["events"]["times"]
    plotOutActV[i].plot(ts, Vms, "-b")


figOutObjV, plotOutObjV = pylab.subplots(3, figsize=(9, 5))
figOutObjV.suptitle('figOutObjV')
# pylab.grid(True)

for i in range(3):
    dmm = nest.GetStatus(mmOutObj[i])[0]
    Vms = dmm["events"]["V_m"]
    ts = dmm["events"]["times"]
    plotOutObjV[i].plot(ts, Vms, "-g")

figS, plotS = pylab.subplots(3, figsize=(9, 5))
figS.suptitle('figS')

for i in range(5):
    dSD = nest.GetStatus(spkDecIn[i], keys="events")[0]
    evs = dSD["senders"]
    ts = dSD["times"]
    plotS[0].plot(ts, evs, "|", color="red")
    print('spike',len(evs))

for i in range(5):
    dSD = nest.GetStatus(spkDecOutAct[i], keys="events")[0]
    evs = dSD["senders"]
    ts = dSD["times"]
    # ts = [x for x in ts if x > 500]
    plotS[1].plot(ts, evs, "|", color="blue")

for i in range(3):
    dSD = nest.GetStatus(spkDecOutObj[i], keys="events")[0]
    evs = dSD["senders"]
    ts = dSD["times"]
    # ts = [x for x in ts if x > 500]
    plotS[2].plot(ts, evs, "|", color="green")

synIn = nest.GetConnections(neuIn[0], neuIn[4])
synInW = nest.GetStatus(synIn, keys='weight')
print('weight:',synInW)

# synoutActW = nest.GetStatus(synoutAct, keys='weight')
# print(synoutActW)

# synoutObjW = nest.GetStatus(synoutObj, keys='weight')
# print(synoutObjW)

pylab.show()
