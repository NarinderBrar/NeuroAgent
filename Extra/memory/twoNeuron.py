import pylab
import nest
import nest.voltage_trace

weight = 2000.0
delay = 1.0
stim = 1000.0

neuron1 = nest.Create("iaf_psc_alpha")
neuron2 = nest.Create("iaf_psc_alpha")
neuron3 = nest.Create("iaf_psc_alpha")

nest.SetStatus(neuron1, {"I_e": 376.})
#nest.SetStatus(neuron2, {"I_e": 376.})

nest.Connect(neuron1, neuron2, syn_spec={'weight': weight, 'delay': delay})
nest.Connect(neuron2, neuron3, syn_spec={'weight': weight, 'delay': delay})

spikedetector = nest.Create("spike_detector", params={"withgid": True, "withtime": True})
nest.Connect(neuron3, spikedetector)
print(nest.GetDefaults("spike_detector"))

multimeter1 = nest.Create("multimeter")
nest.SetStatus(multimeter1, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeter1, neuron1)

multimeter2 = nest.Create("multimeter")
nest.SetStatus(multimeter2, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeter2, neuron2)

multimeter3 = nest.Create("multimeter")
nest.SetStatus(multimeter3, {"withtime":True, "record_from":["V_m"]})
nest.Connect(multimeter3, neuron3)

# spikegenerator = nest.Create('spike_generator')
# nest.SetStatus(spikegenerator, {'spike_times': [500.0, 510.0, 520.0, 530.0, 540.0, 550.0]})
# nest.Connect(spikegenerator, neuron2, syn_spec={'weight': 1e3})

nest.Simulate(1000.0)

pylab.figure(1)
dmm = nest.GetStatus(multimeter1)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]
pylab.plot(ts, Vms)

pylab.figure(1)
dmm = nest.GetStatus(multimeter2)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]
pylab.plot(ts, Vms)

pylab.figure(1)
dmm = nest.GetStatus(multimeter3)[0]
Vms = dmm["events"]["V_m"]
ts = dmm["events"]["times"]
pylab.plot(ts, Vms)

pylab.figure(2)
dSD = nest.GetStatus(spikedetector, keys="events")[0]
evs = dSD["senders"]
ts = dSD["times"]
pylab.plot(ts, evs, ".")
pylab.show()