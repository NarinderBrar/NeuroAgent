#!/usr/bin/env python

import nest
nest.SetKernelStatus({"overwrite_files": True})

neurons = nest.Create('iaf_psc_alpha', 1, {'I_e': 400.0})

music_out = nest.Create('music_event_out_proxy', 1, params = {'port_name':'p_out'})

for i, n in enumerate(neurons):
    nest.Connect([n], music_out, "one_to_one",{'music_channel': i})

sdetector = nest.Create("spike_detector")

nest.SetStatus(sdetector, {"withgid": True, "withtime": True, "to_file": True,
    "label": "send", "file_extension": "spikes"})

nest.Connect(neurons, sdetector)

nest.Simulate(1000.0)
