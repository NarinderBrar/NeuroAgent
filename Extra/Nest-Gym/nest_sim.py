#!/usr/bin/env python

import matplotlib.pyplot as plt
import nest
import numpy as np

from mpi4py import MPI
comm = MPI.COMM_WORLD

def get_current_offset(weight, rate, tau_m, tau_syn, C_m):
    return weight / C_m * rate * tau_m * tau_syn * 1e-3

simtime = 10000.
max_rate = 50.

tau_m = 1.
tau_syn = 20.
J = 10.

nest.ResetKernel()
nest.SetKernelStatus({'resolution': 1.})
C_m = nest.GetDefaults('iaf_psc_exp', 'C_m')

################################################
############### input neuron setup ##############
################################################
neuron_right = nest.Create('iaf_psc_exp', 1, {
    'E_L': -60. + get_current_offset(-J, max_rate / 2., tau_m, tau_syn, C_m),
    'V_th': -60., 'tau_m': tau_m, 'tau_syn_ex': tau_syn, 'tau_syn_in': tau_syn, 'C_m': C_m
})
neuron_right_2 = nest.Create('iaf_psc_exp', 1, {
    'E_L': -60. + get_current_offset(-J, max_rate / 2., tau_m, tau_syn, C_m),
    'V_th': -60., 'tau_m': tau_m, 'tau_syn_ex': tau_syn, 'tau_syn_in': tau_syn, 'C_m': C_m
})

################################################
############### input proxy setup ###############
################################################
music_in_proxy = nest.Create('music_event_in_proxy', 1, {'port_name': 'in'})
music_in_proxy_2 = nest.Create('music_event_in_proxy', 1, {'port_name': 'in'})

nest.SetStatus(music_in_proxy, {'music_channel': 0})
nest.SetStatus(music_in_proxy_2, {'music_channel': 1})

nest.Connect(music_in_proxy, neuron_right, syn_spec={'weight': J})
nest.Connect(music_in_proxy_2, neuron_right_2, syn_spec={'weight': J} )

################################################
############### output neuron setup ############
################################################
neuron_command = nest.Create('iaf_psc_exp', 1, {'E_L': -60., 'V_th': -60., 'tau_m': 10 * tau_m, 'tau_syn_ex': tau_syn, 'tau_syn_in': tau_syn})
neuron_command_2 = nest.Create('iaf_psc_exp', 1, {'E_L': -60., 'V_th': -60., 'tau_m': 10 * tau_m, 'tau_syn_ex': tau_syn, 'tau_syn_in': tau_syn})

################################################
############### output proxy setup ###############
################################################
music_out_proxy = nest.Create('music_event_out_proxy', 1, {'port_name': 'out'})
#music_out_proxy_2 = nest.Create('music_event_out_proxy', 1, {'port_name': 'out'})

nest.Connect(neuron_command, music_out_proxy, "one_to_one",{'music_channel': 0})
nest.Connect(neuron_command_2, music_out_proxy, "one_to_one",{'music_channel': 1})

################################################
############# neuron connectivity ##############
################################################
nest.Connect(neuron_right, neuron_command, syn_spec={'weight': J})
nest.Connect(neuron_right_2, neuron_command_2, syn_spec={'weight': J})

################################################
############# neuron connectivity ##############
################################################
sd = nest.Create('spike_detector')

nest.Connect(neuron_right, sd)
nest.Connect(neuron_right_2, sd)
nest.Connect(neuron_command, sd)

################################################
############### input multimeter ###############
################################################
mv_right = nest.Create('multimeter', 1, {'record_from': ['V_m']})
mv_right_2 = nest.Create('multimeter', 1, {'record_from': ['V_m']})
mv_command = nest.Create('multimeter', 2, {'record_from': ['V_m']})

nest.Connect(mv_right, neuron_right)
nest.Connect(mv_right_2, neuron_right_2)
nest.Connect(mv_command, neuron_command)

################################################
################### simulation #################
################################################
# necessary to synchronize with MUSIC
comm.Barrier()  
nest.Simulate(simtime)

################################################
################### voltimeter #################
################################################
# plot results
spikes = nest.GetStatus(sd, 'events')[0]

vm_right = nest.GetStatus(mv_right, 'events')[0]
vm_right_2 = nest.GetStatus(mv_right_2, 'events')[0]
vm_command = nest.GetStatus(mv_command, 'events')[0]

################################################
###################### plot ###################
################################################
fig = plt.figure()

ax = fig.add_subplot(221)
ax.set_xlim([0., simtime])
ax.set_ylim([neuron_right[0] - 1, neuron_command[0] + 1])
ax.set_yticks([neuron_right[0],neuron_right_2[0], neuron_command[0]])
ax.set_yticklabels(['Right','Right2','Command'])
ax.plot(spikes['times'], spikes['senders'], 'ko')

ax2 = fig.add_subplot(222)
ax2.set_xlabel('Time (ms)')
ax2.set_ylabel('Membrane potential (mV)')
ax2.plot(vm_right['times'], vm_right['V_m'], 'r', label='right')

ax3 = fig.add_subplot(223)
ax3.set_xlabel('Time (ms)')
ax2.set_ylabel('Membrane potential (mV)')
ax3.plot(vm_right_2['times'], vm_right_2['V_m'], 'b', label='right2')

ax5 = fig.add_subplot(224)
ax5.set_xlabel('Time (ms)')
ax5.set_ylabel('Membrane potential (mV)')
ax5.plot(vm_command['times'], vm_command['V_m'], 'm', label='command')

plt.legend()

fig.savefig('nest_output.png', dpi=300)
