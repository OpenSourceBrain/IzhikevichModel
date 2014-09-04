"""
Model implementation in PyNN by Vitor Chaud, Andrew Davison and Padraig Gleeson (August 2013 and February 2014).
This is a re-implementation of the models described in the following references to reproduce Fig. 1 of Izhikevich (2004).

Original implementation references:

        Izhikevich E.M. (2004) Which Model to Use for Cortical Spiking Neurons?
        IEEE Transactions on Neural Networks, 15:1063-1070 (special issue on temporal coding)

        Izhikevich E.M. (2003) Simple Model of Spiking Neurons.
        IEEE Transactions on Neural Networks, 14:1569- 1572

        http://www.izhikevich.org/publications/whichmod.htm


Version 0.1 - original script written by Vitor Chaud during Google Summer of Code 2013
Version 0.2 - script condensed and updated to use latest development version of PyNN by Andrew Davison, February 2014
"""

from __future__ import division
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pyNN.utility import get_simulator, normalized_filename

sim, options = get_simulator()

globalTimeStep = 0.01

plt.rcParams.update({
    'lines.linewidth': 0.5,
    'legend.fontsize': 'small',
    'axes.titlesize': 'small',
    'font.size': 6,
    'savefig.dpi': 200,
})

# v represents the membrane potential of the neuron
# u represents a membrane recovery variable
# Synaptic currents or injected dc-currents are delivered via the variable I.

# Dimensionless parameters

# The parameter a describes the time scale of the recovery variable u

# The parameter b describes the sensitivity of the recovery variable
# u to the subthreshold fluctuations of the membrane potential v.

# The parameter c describes the after-spike reset value of the membrane
# potential v caused by the fast high-threshold K+ conductances.

# The parameter d describes after-spike reset of the recovery variable
# u caused by slow high-threshold Na+ and K+ conductances.

j = 0

plt.ion()
fig = plt.figure(1, facecolor='white', figsize=(6, 6))
gs = gridspec.GridSpec(5, 4)
gs.update(hspace=0.5, wspace=0.4)


def run_simulation(timestep=globalTimeStep, a=0.02, b=0.2, c=-65.0, d=6.0,
                   u_init=None, v_init=-70.0,
                   waveform=None, tstop=100.0,
                   title="", scalebar_level=0, label_scalebar=False):
    global j, fig, gs
    sim.setup(timestep=timestep, min_delay=timestep)

    if u_init is None:
        u_init = b * v_init
    initialValues = {'u': u_init, 'v': v_init}

    cell_type = sim.Izhikevich(a=a, b=b, c=c, d=d, i_offset=0.0)
    neuron = sim.create(cell_type)
    neuron.initialize(**initialValues)

    neuron.record('v')

    times, amps = waveform
    injectedCurrent = sim.StepCurrentSource(times=times, amplitudes=amps)
    injectedCurrent.inject_into(neuron)

    sim.run(tstop)

    data = neuron.get_data().segments[0]

    gs1 = gridspec.GridSpecFromSubplotSpec(2, 1,
                                           subplot_spec=gs[j//4, j%4],
                                           height_ratios=[8, 1],
                                           hspace=0.0)
    ax1 = plt.subplot(gs1[0])
    ax2 = plt.subplot(gs1[1])

    j += 1
    for ax in (ax1, ax2):
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.spines['left'].set_color('None')
        ax.spines['right'].set_color('None')
        ax.spines['bottom'].set_color('None')
        ax.spines['top'].set_color('None')
        ax.set_xlim(0.0, t_stop)

    ax1.set_title(title)

    vm = data.filter(name='v')[0]
    i_times, i_vars = stepify(times, amps)

    ax1.plot(vm.times, vm)
    ax1.set_ylim(-90, 30)

    ax2.plot(i_times, i_vars, 'g')
    ymin, ymax = amps.min(), amps.max()
    padding = (ymax - ymin)/10
    ax2.set_ylim(ymin - padding, ymax + padding)

    # scale bar
    scalebar_y = ymin + (ymax - ymin) * scalebar_level
    ax2.plot([tstop - 20, tstop], [scalebar_y, scalebar_y],
             color='k', linestyle='-', linewidth=1)
    if label_scalebar:
        ax.text(tstop, ymin + padding, "20 ms", fontsize=4, horizontalalignment='right')

    plt.show(block=False)
    fig.canvas.draw()


def step(amplitude, t_stop):
    times = np.array([0, t_stop/10, t_stop])
    amps = np.array([0, amplitude, amplitude])
    return times, amps


def pulse(amplitude, onsets, width, t_stop, baseline=0.0):
    times = [0]
    amps = [baseline]
    for onset in onsets:
        times += [onset, onset + width]
        amps += [amplitude, baseline]
    times += [t_stop]
    amps += [baseline]
    return np.array(times), np.array(amps)


def ramp(amplitude, onset, t_stop, baseline=0.0, timeStep=globalTimeStep, t_start=0.0):
    if onset > t_start:
        times = np.hstack((np.array((t_start, onset)),  # flat part
                           np.arange(onset + timeStep, t_stop + timeStep, timeStep)))  # ramp part
    else:
        times = np.arange(t_start, t_stop + timeStep, timeStep)
    amps = baseline + amplitude*(times - onset) * (times > onset)
    return times, amps


def stepify(times, values):
    new_times = np.empty((2*times.size - 1,))
    new_values = np.empty_like(new_times)
    new_times[::2] = times
    new_times[1::2] = times[1:]
    new_values[::2] = values
    new_values[1::2] = values[:-1]
    return new_times, new_values


#############################################
##      Sub-plot A: Tonic spiking
#############################################

t_stop = 100.0
run_simulation(a=0.02, b=0.2, c=-65.0, d=6.0, v_init=-70.0,
               waveform=step(0.014, t_stop),
               tstop=t_stop, title='(A) Tonic spiking',
               label_scalebar=True)

#############################################
##      Sub-plot B: Phasic spiking
#############################################

t_stop = 200.0
run_simulation(a=0.02, b=0.25, c=-65.0, d=6.0, v_init=-64.0,
               waveform=step(0.0005, t_stop),
               tstop=t_stop, title='(B) Phasic spiking')

#############################################
##      Sub-plot C: Tonic bursting
#############################################

t_stop = 220.0
run_simulation(a=0.02, b=0.2, c=-50.0, d=2.0, v_init=-70.0,
               waveform=step(0.015, t_stop),
               tstop=t_stop, title='(C) Tonic bursting')

#############################################
##      Sub-plot D: Phasic bursting
#############################################

t_stop = 200.0
run_simulation(a=0.02, b=0.25, c=-55.0, d=0.05, v_init=-64.0,
               waveform=step(0.0006, t_stop),
               tstop=t_stop, title='(D) Phasic bursting')

#############################################
##      Sub-plot E: Mixed mode
#############################################

t_stop = 160.0
run_simulation(a=0.02, b=0.2, c=-55.0, d=4.0, v_init=-70.0,
               waveform=step(0.01, t_stop),
               tstop=t_stop, title='(E) Mixed mode')

#######################################################
##      Sub-plot F: Spike Frequency Adaptation (SFA)
#######################################################

t_stop = 85.0
run_simulation(a=0.01, b=0.2, c=-65.0, d=8.0, v_init=-70.0,
               waveform=step(0.03, t_stop),
               tstop=t_stop, title='(F) SFA')

############################################
##      Sub-plot G: Class 1 excitable
############################################

'''
         Note eqn for this cell is:
            V = V + tau*(0.04*V^2+4.1*V+108-u+I);
         as opposed to
            V = V + tau*(0.04*V^2+5*V+140-u+I);
         in figure1.m
'''


t_stop = 300.0
run_simulation(a=0.02, b=0.2, c=-65.0, d=6.0, v_init=-70.0,
               waveform=ramp(0.000075, 30.0, t_stop),
               tstop=t_stop, title='(G) Class 1 excitable')

############################################
##      Sub-plot H: Class 2 excitable
############################################

t_stop = 300.0
run_simulation(a=0.2, b=0.26, c=-65.0, d=0.0, v_init=-64.0,
               waveform=ramp(0.000015, 30.0, t_stop, baseline=-0.0005),
               tstop=t_stop, title='(H) Class 2 excitable')

#########################################
##      Sub-plot I: Spike latency
#########################################

t_stop = 100.0
run_simulation(a=0.02, b=0.2, c=-65.0, d=6.0, v_init=-70.0,
               waveform=pulse(0.00671,  # 0.00704 in original
                              [10], 3, t_stop),
               tstop=t_stop, title='(I) Spike latency',
               scalebar_level=0.5)

#################################################
##      Sub-plot J: Subthreshold oscillation
#################################################

t_stop = 200.0
run_simulation(a=0.05, b=0.26, c=-60.0, d=0.0, v_init=-62.0,
               waveform=pulse(0.002, [20], 5, t_stop),
               tstop=t_stop, title='(J) Subthreshold oscillation',
               scalebar_level=0.5)

####################################
##      Sub-plot K: Resonator
####################################

t_stop = 400.0
T1 = t_stop / 10
T2 = T1 + 20
T3 = 0.7 * t_stop
T4 = T3 + 40
run_simulation(a=0.1, b=0.26, c=-60.0, d=-1.0, v_init=-62.0,
               waveform=pulse(0.00065, [T1, T2, T3, T4], 4, t_stop),
               tstop=t_stop, title='(K) Resonator',
               scalebar_level=0.5)


####################################
##      Sub-plot L: Integrator
####################################

'''
         Note eqn for this cell is:
            V = V + tau*(0.04*V^2+4.1*V+108-u+I);
         as opposed to
            V = V + tau*(0.04*V^2+5*V+140-u+I);
         in figure1.m
'''

t_stop = 100.0
T1 = t_stop / 11
T2 = T1 + 5
T3 = 0.7 * t_stop
T4 = T3 + 10
run_simulation(a=0.02, b=-0.1, c=-55.0, d=6.0, v_init=-60.0,
               waveform=pulse(0.009, [T1, T2, T3, T4], 2, t_stop),
               tstop=t_stop, title='(L) Integrator',
               scalebar_level=0.5)


######################################
##      Sub-plot M: Rebound spike
######################################

t_stop = 200.0
run_simulation(a=0.03, b=0.25, c=-60.0, d=4.0, v_init=-64.0,
               waveform=pulse(-0.015, [20], 5, t_stop),
               tstop=t_stop, title='(M) Rebound spike')

######################################
##      Sub-plot N: Rebound burst
######################################

t_stop = 200.0
run_simulation(a=0.03, b=0.25, c=-52.0, d=0.0, v_init=-64.0,
               waveform=pulse(-0.015, [20], 5, t_stop),
               tstop=t_stop, title='(N) Rebound burst')

###############################################
##      Sub-plot O: Threshold variability
###############################################

t_stop = 100.0
times = np.array([0, 10, 15, 70, 75, 80, 85, t_stop])
amps = np.array([0, 0.001, 0, -0.006, 0, 0.001, 0, 0])
run_simulation(a=0.03, b=0.25, c=-60.0, d=4.0, v_init=-64.0,
               waveform=(times, amps),
               tstop=t_stop, title='(O) Threshold variability')

######################################
##      Sub-plot P: Bistability
######################################

t_stop = 300.0
T1 = t_stop/8
T2 = 208  # 216.0 in original
run_simulation(a=0.1, b=0.26, c=-60.0, d=0.0, v_init=-61.0,
               waveform=pulse(0.00124, [T1, T2], 5, t_stop, baseline=0.00024),
               tstop=t_stop, title='(P) Bistability',
               scalebar_level=0.5)

#####################################################
##      Sub-plot Q: Depolarizing after-potential
#####################################################

t_stop = 50.0
run_simulation(a=1.0, b=0.18, c=-60.0, d=-21.0, v_init=-70.0,
               waveform=pulse(0.02, [9], 2, t_stop),
               tstop=t_stop, title='(Q) DAP',
               scalebar_level=0.5)

#####################################################
##      Sub-plot R: Accomodation
#####################################################

# different model
#    u = u + tau*a*(b*(V+65))

t_stop = 400.0

parts = (ramp(0.00004, 0.0, 200.0),
         (np.array([200.0 + globalTimeStep, 300.0 - globalTimeStep]), np.array([0.0, 0.0])),
         ramp(0.00032, 300.0, 312.5, t_start=300.0),
         (np.array([312.5 + globalTimeStep, t_stop]), np.array([0.0, 0.0])))
totalTimes, totalAmps = np.hstack(parts)

run_simulation(a=0.02, b=1.0, c=-55.0, d=4.0, v_init=-65.0, u_init=-16.0,
               waveform=(totalTimes, totalAmps),
               tstop=t_stop, title='(R) Accomodation',
               scalebar_level=0.5)

#####################################################
##      Sub-plot S: Inhibition-induced spiking
#####################################################

t_stop = 350.0
run_simulation(a=-0.02, b=-1.0, c=-60.0, d=8.0, v_init=-63.8,
               waveform=pulse(0.075, [50], 170, t_stop, baseline=0.08),
               tstop=t_stop, title='(S) Inhibition-induced spiking')

#####################################################
##      Sub-plot T: Inhibition-induced bursting
#####################################################

'''
Modifying parameter d from -2.0 to -0.7 in order to reproduce Fig. 1
'''

t_stop = 350.0
run_simulation(a=-0.026, b=-1.0, c=-45.0, d=-0.7, v_init=-63.8,
               waveform=pulse(0.075, [50], 200, t_stop, baseline=0.08),
               tstop=t_stop, title='(T) Inhibition-induced bursting')


filename = normalized_filename("results", "izhikevich2004", "png", options.simulator)
try:
    os.makedirs(os.path.dirname(filename))
except OSError:
    pass
fig.savefig(filename)
