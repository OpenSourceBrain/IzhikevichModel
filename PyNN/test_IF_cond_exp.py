

from pyNN.random import RandomDistribution, NumpyRNG
from pyNN.neuron import *
from pyNN.utility import get_script_args, Timer, ProgressBar, init_logging, normalized_filename
import matplotlib.pyplot as plt
import numpy as np


timeStep = 0.01

setup(timestep=timeStep, min_delay=0.5)




tau_m 		= 20.0	# [ms]
cm 		= 0.2 	# [nF]
v_rest 		= -60.0	# [mV]
v_thresh 	= -50.0 # [mV]
tau_syn_E 	= 5.0	# [ms]
tau_syn_I 	= 10.0	# [ms]
e_rev_E 	= 0.0	# [mV]
e_rev_I 	= -80.0	# [mV]
v_reset 	= -60.0	# [mV]
tau_refrac 	= 5.0	# [ms]
i_offset 	= 0.0	# [nA]


neuronParameters = 	{
			'tau_m':	tau_m,	
			'cm':		cm, 	
			'v_rest':	v_rest,	
			'v_thresh':	v_thresh, 	
			'tau_syn_E':	tau_syn_E,	
			'tau_syn_I':	tau_syn_I,	
			'e_rev_E':	e_rev_E,	
			'e_rev_I':	e_rev_I,	
			'v_reset':	v_reset,	
			'tau_refrac':	tau_refrac,	
			'i_offset': 	i_offset	
			}

cell_type = IF_cond_exp(**neuronParameters)

rand_distr = RandomDistribution('uniform', (v_reset, v_thresh), rng=NumpyRNG(seed=85524))


neuron = create(cell_type)

neuron.initialize(neuron=rand_distr)

neuron.record('v')


totalTimes = np.zeros(0)
totalAmps = np.zeros(0)

times = np.linspace(0.0, 30.0, int(1 + (30.0 - 0.0) / timeStep))
amps = np.linspace(0.0, 0.0, int(1 + (30.0 - 0.0) / timeStep))
totalTimes = np.append(totalTimes, times)
totalAmps = np.append(totalAmps, amps)

times = np.linspace(30 + timeStep, 300, int((300 - 30) / timeStep))
amps = np.linspace(0.005 * timeStep, 0.005 * (300 - 30), int((300 - 30) / timeStep))
totalTimes = np.append(totalTimes, times)
totalAmps = np.append(totalAmps, amps)

injectedCurrent = StepCurrentSource(times=totalTimes, amplitudes=totalAmps)
injectedCurrent.inject_into(neuron)



run(300)



data = neuron.get_data().segments[0]


plt.ion()
fig = plt.figure(1, facecolor='white')
ax1 = fig.add_subplot(5, 4, 7)
ax1.get_xaxis().set_visible(False)
ax1.get_yaxis().set_visible(False)
ax1.spines['left'].set_color('None')
ax1.spines['right'].set_color('None')
ax1.spines['bottom'].set_color('None')
ax1.spines['top'].set_color('None')

ax1.set_title('(G) Class 1 excitable')

vm = data.filter(name='v')[0]
plt.plot(vm.times, vm, [0, 30, 300, 300],[-90, -90, -70, -90])

plt.show(block=False)
fig.canvas.draw()





raw_input("Simulation finished... Press enter to exit...")










