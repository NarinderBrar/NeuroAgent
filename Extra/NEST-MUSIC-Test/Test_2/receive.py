#!/usr/bin/env python

import nest
nest.SetKernelStatus({"overwrite_files": True})

music_in = nest.Create("music_event_in_proxy", 2, params = {'port_name': 'p_in'})

for i, n in enumerate(music_in):
    nest.SetStatus([n], {'music_channel': i})

nest.SetAcceptableLatency('p_in', 2.0)

parrots = nest.Create("parrot_neuron", 2)

sdetector = nest.Create("spike_detector")
nest.SetStatus(sdetector, {"withgid": True, "withtime": True, "to_file": True,
    "label": "receive", "file_extension": "spikes"})

nest.Connect(music_in, parrots, 'one_to_one', {"weight":1.0, "delay": 2.0})
nest.Connect(parrots, sdetector)

nest.Simulate(1000.0)
