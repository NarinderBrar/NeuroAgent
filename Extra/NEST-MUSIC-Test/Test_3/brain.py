#!/usr/bin/env python

import nest
import music
import numpy

#music_in_proxy = nest.Create('music_event_in_proxy', 1, {'port_name': 'in'})

proxy = nest.Create('music_cont_out_proxy', 1)

nest.SetStatus(proxy, {'port_name': 'out'})
nest.SetStatus(proxy, {'record_from': ["V_m"], 'interval': 0.1})

neuron_grp = nest.Create('iaf_cond_exp', 2)

#nest.Connect(music_in_proxy, neuron_grp, syn_spec={'weight': 10.0})

nest.SetStatus(proxy, {'targets': neuron_grp})

nest.SetStatus([neuron_grp[0]], "I_e", 300.)
nest.SetStatus([neuron_grp[1]], "I_e", 600.)

nest.Simulate(200)