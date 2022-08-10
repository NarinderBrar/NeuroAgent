#!/usr/bin/env python

################################################
#################### imports ###################
################################################
import nest
import pylab

import numpy as np

import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable

from mpi4py import MPI
comm = MPI.COMM_WORLD

import zmq

ctx = zmq.Context()
pub = ctx.socket(zmq.PUB)
pub.bind('tcp://*:5562')

################################################
################## parameters #################
################################################

sec = 60
simulation_time = sec*1000.

w_prox_neu = 20.0
w_neu_neu = 60.

C_m = 150.0
tau_m = 1.0
tau_syn_ex = 20.0
tau_syn_in = 20.0
################################################
################## NEST Settings ###############
################################################
nest.ResetKernel()
nest.SetKernelStatus({'resolution': 1.})

################################################
############### input proxy setup ###############
################################################
mpIn = []
mpOutAct = []
mpOutObj = []

for i in range(12):
    mpI = nest.Create('music_event_in_proxy', 1, {'port_name': 'in'})
    nest.SetStatus(mpI, {'music_channel': i})
    mpIn.append(mpI)

mpOO = nest.Create('music_event_out_proxy', 1, {'port_name': 'out'})

################################################
################## neuron setup ################
################################################
neuIn = []
neuOutAct = []
neuOutObj = []

p = {'E_L': -60.05, 'V_th': -60., 'tau_m': tau_m, 'tau_syn_ex': tau_syn_ex, 'tau_syn_in': tau_syn_in, 'C_m': C_m}

for i in range(5):
    inNeu = nest.Create('iaf_psc_exp', 1, params=p)
    neuIn.append(inNeu)

for i in range(5):
    outNeu = nest.Create('iaf_psc_exp', 1, params=p)
    neuOutAct.append(outNeu)

for i in range(2):
    outNeu = nest.Create('iaf_psc_exp', 1, params=p)
    neuOutObj.append(outNeu)

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
    mmI = nest.Create('multimeter', 1, {'record_from': ['V_m']})
    #mmI = nest.Create("multimeter")
    #nest.SetStatus(mmI, {"withtime":True, "record_from":["V_m"]})
    mmIn.append(mmI)

    mmOA = nest.Create('multimeter', 1, {'record_from': ['V_m']})
    #mmOA = nest.Create("multimeter")
    #nest.SetStatus(mmOA, {"withtime":True, "record_from":["V_m"]})
    mmOutAct.append(mmOA)

    mmOO = nest.Create('multimeter', 1, {'record_from': ['V_m']})
    #mmOO = nest.Create("multimeter")
    #nest.SetStatus(mmOO, {"withtime":True, "record_from":["V_m"]})
    mmOutObj.append(mmOO)

    #spikedetectorIn = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
    spikedetectorIn = nest.Create("spike_recorder")
    spkDecIn.append(spikedetectorIn)

    #sdOutAct = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
    sdOutAct = nest.Create("spike_recorder")
    spkDecOutAct.append(sdOutAct)

    #sdOutObj = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
    sdOutObj = nest.Create("spike_recorder")
    spkDecOutObj.append(sdOutObj)

################################################
##################### synapses #################
################################################

synoutAct = []
synoutObj = []
# for i in range(5):#in
#     for j in range(5):#OutAct
#         synoutAct.append (nest.Connect(neuIn[i], neuOutAct[j], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu}))
#     for k in range(2):#OutObj
#         synoutObj.append (nest.Connect(neuIn[i], neuOutObj[k], syn_spec={'model': 'stdp_synapse',  'weight': w_neu_neu}))

syn_dict = {"synapse_model": "stdp_synapse", "weight": w_neu_neu}

synoutAct.append (nest.Connect(neuIn[0], neuOutAct[0], syn_spec={'synapse_model': 'stdp_synapse',  'weight': w_neu_neu}))
synoutAct.append (nest.Connect(neuIn[1], neuOutAct[1], syn_spec={'synapse_model': 'stdp_synapse',  'weight': w_neu_neu}))
synoutAct.append (nest.Connect(neuIn[2], neuOutAct[2], syn_spec={'synapse_model': 'stdp_synapse',  'weight': w_neu_neu}))
synoutAct.append (nest.Connect(neuIn[3], neuOutAct[3], syn_spec={'synapse_model': 'stdp_synapse',  'weight': w_neu_neu}))
synoutAct.append (nest.Connect(neuIn[4], neuOutAct[4], syn_spec={'synapse_model': 'stdp_synapse',  'weight': w_neu_neu}))

synoutObj.append (nest.Connect(neuIn[0], neuOutObj[0], syn_spec={'synapse_model': 'stdp_synapse',  'weight': w_neu_neu}))
synoutObj.append (nest.Connect(neuIn[1], neuOutObj[0], syn_spec={'synapse_model': 'stdp_synapse',  'weight': w_neu_neu}))
synoutObj.append (nest.Connect(neuIn[2], neuOutObj[1], syn_spec={'synapse_model': 'stdp_synapse',  'weight': w_neu_neu}))
synoutObj.append (nest.Connect(neuIn[3], neuOutObj[0], syn_spec={'synapse_model': 'stdp_synapse',  'weight': w_neu_neu}))
synoutObj.append (nest.Connect(neuIn[3], neuOutObj[1], syn_spec={'synapse_model': 'stdp_synapse',  'weight': w_neu_neu}))
synoutObj.append (nest.Connect(neuIn[4], neuOutObj[1], syn_spec={'synapse_model': 'stdp_synapse',  'weight': w_neu_neu}))

################################################
##################connectivity #################
################################################
for i in range(5): 
    nest.Connect(mpIn[i], neuIn[i], syn_spec={'weight': w_prox_neu})
for i in range(5): 
    nest.Connect(mpIn[i+5], neuOutAct[i], syn_spec={'weight': w_prox_neu})
for i in range(2): 
    nest.Connect(mpIn[i+10], neuOutObj[i], syn_spec={'weight': w_prox_neu})

for i in range(5): 
    nest.Connect(neuIn[i], mpOO, "one_to_one",{'music_channel': i})

for i in range(5): 
    nest.Connect(neuOutAct[i], mpOO, "one_to_one",{'music_channel': (i+5)})

for i in range(2): 
    nest.Connect(neuOutObj[i], mpOO, "one_to_one",{'music_channel': (i+10)})


for i in range(5): 
    nest.Connect(mmIn[i], neuIn[i])
    nest.Connect(neuIn[i], spkDecIn[i])

    nest.Connect(mmOutAct[i], neuOutAct[i])
    nest.Connect( neuOutAct[i], spkDecOutAct[i])

for i in range(2):
    nest.Connect(mmOutObj[i], neuOutObj[i])
    nest.Connect( neuOutObj[i], spkDecOutObj[i])

comm.Barrier()  
#nest.Simulate(simulation_time)

# import matplotlib.pyplot as plt

i = 0
t = 0
for _ in range(6000):
    nest.Simulate(10)
    
    t+=10
    i+=1
    if i==35:
        dmm = nest.GetStatus(mmOutObj[0])[0]
        Vms1 = dmm["events"]["V_m"]
        Vms1 = Vms1[-150:]

        ts = dmm["events"]["times"]
        ts = ts[-150:]

        dmm = nest.GetStatus(mmOutObj[1])[0]
        Vms2 = dmm["events"]["V_m"]
        Vms2 = Vms2[-150:]

        w1 = []
        w2 = []
        tsW = [t]*25
        for i in range(5):#in
            for j in range(5):#OutAct
                synIn = nest.GetConnections(neuIn[i], neuOutAct[j])
                synInW = nest.GetStatus(synIn, keys='weight')
                if synInW:
                    w1.append(synInW[0])
                else:
                    w1.append(0)

        print('\n')

        for i in range(5):#in
            for j in range(2):#OutAct
                synIn = nest.GetConnections(neuIn[i], neuOutObj[j])
                synInW = nest.GetStatus(synIn, keys='weight')
                if synInW:
                    w2.append(synInW[0])
                else:
                    w2.append(0)
        
        msg = {'ts' : (list)(ts),'mmInV1': (list)(Vms1), 'mmInV2': (list)(Vms2),'w1': (w1), 'w2': (w2), 't' : (tsW)}
        pub.send_json(msg)

        i=0

# ################################################
# ##################### Plots ####################
# ################################################
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

for i in range(2):
    dmm = nest.GetStatus(mmOutObj[i])[0]
    Vms = dmm["events"]["V_m"]
    ts = dmm["events"]["times"]
    plotOutObjV[i].plot(ts, Vms, "-g")

figS, plotS = pylab.subplots(3, figsize=(9, 5))
figS.suptitle('figS')

print('\n')
for i in range(5):
    dSD = nest.GetStatus(spkDecIn[i], keys="events")[0]
    evs = dSD["senders"]
    ts = dSD["times"]
    plotS[0].plot(ts, evs, "|", color="red")
    tsN = [x for x in ts if x > 18500]
    evsN = evs[-len(tsN):]
    
print('\n')
for i in range(5):
    dSD = nest.GetStatus(spkDecOutAct[i], keys="events")[0]
    evs = dSD["senders"]
    ts = dSD["times"]
    plotS[1].plot(ts, evs, "|", color="blue")


print('\n')
for i in range(2):
    dSD = nest.GetStatus(spkDecOutObj[i], keys="events")[0]
    evs = dSD["senders"]
    ts = dSD["times"]
    plotS[2].plot(ts, evs, "|", color="green")


print('\n')

for i in range(5):#in
    for j in range(5):#OutAct
        synIn = nest.GetConnections(neuIn[i], neuOutAct[j])
        synInW = nest.GetStatus(synIn, keys='weight')
        print('weight:s',i,'-a', j ,':' ,synInW)

print('\n')

for i in range(5):#in
    for j in range(2):#OutAct
        synIn = nest.GetConnections(neuIn[i], neuOutObj[j])
        synInW = nest.GetStatus(synIn, keys='weight')
        print('weight:s',i,'-o', j ,':' ,synInW)

pylab.show()

