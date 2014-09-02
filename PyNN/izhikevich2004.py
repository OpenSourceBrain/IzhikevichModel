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
import numpy as np
import matplotlib.pyplot as plt
from pyNN.utility import get_simulator

sim, args = get_simulator()

globalTimeStep = 0.01


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

j = 1


def run_simulation(timestep=0.01, a=0.02, b=0.2, c=-65.0, d=6.0,
                   u_init=None, v_init=-70.0,
                   waveform=None, tstop=100.0,
                   title="", p_waveform=None,
                   xlim=None, ylim=None):
    global j
    sim.setup(timestep=timestep, min_delay=0.5)

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

    plt.ion()
    fig = plt.figure(1, facecolor='white')
    ax1 = fig.add_subplot(5, 4, j)
    j += 1
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    ax1.spines['left'].set_color('None')
    ax1.spines['right'].set_color('None')
    ax1.spines['bottom'].set_color('None')
    ax1.spines['top'].set_color('None')

    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    ax1.set_title(title)

    vm = data.filter(name='v')[0]
    i_times, i_vars = p_waveform
    plt.plot(vm.times, vm, i_times, i_vars)

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


def ramp(amplitude, onset, t_stop, baseline=0.0, timeStep=0.01):
    times = np.arange(0.0, t_stop + timeStep, timeStep)
    amps = baseline + amplitude*(times - onset) * (times > onset)
    return times, amps


#############################################
##	Sub-plot A: Tonic spiking
#############################################

t_stop = 100.0
run_simulation(a=0.02, b=0.2, c=-65.0, d=6.0, v_init=-70.0,
               waveform=step(0.014, t_stop),
               tstop=t_stop, title='(A) Tonic spiking',
               p_waveform=([0, 10, 10, 100], [-90, -90, -80, -80]))

#############################################
##	Sub-plot B: Phasic spiking
#############################################

t_stop = 200.0
run_simulation(a=0.02, b=0.25, c=-65.0, d=6.0, v_init=-64.0,
               waveform=step(0.0005, t_stop),
               tstop=t_stop, title='(B) Phasic spiking',
               p_waveform=([0, 20, 20, 200], [-90, -90, -80, -80]))

#############################################
##	Sub-plot C: Tonic bursting
#############################################

t_stop = 220.0
run_simulation(a=0.02, b=0.2, c=-50.0, d=2.0, v_init=-70.0,
               waveform=step(0.015, t_stop),
               tstop=t_stop, title='(C) Tonic bursting',
               p_waveform=([0, 22, 22, 220], [-90, -90, -80, -80]))

#############################################
##	Sub-plot D: Phasic bursting
#############################################

t_stop = 200.0
run_simulation(a=0.02, b=0.25, c=-55.0, d=0.05, v_init=-64.0,
               waveform=step(0.0006, t_stop),
               tstop=t_stop, title='(D) Phasic bursting',
               p_waveform=([0, 20, 20, 200], [-90, -90, -80, -80]))

#############################################
##	Sub-plot E: Mixed mode
#############################################

t_stop = 160.0
run_simulation(a=0.02, b=0.2, c=-55.0, d=4.0, v_init=-70.0,
               waveform=step(0.01, t_stop),
               tstop=t_stop, title='(E) Mixed mode',
               p_waveform=([0, 16, 16, 160], [-90, -90, -80, -80]))

#######################################################
##	Sub-plot F: Spike Frequency Adaptation (SFA)
#######################################################

t_stop = 85.0
run_simulation(a=0.01, b=0.2, c=-65.0, d=8.0, v_init=-70.0,
               waveform=step(0.03, t_stop),
               tstop=t_stop, title='(F) SFA',
               p_waveform=([0, 8.5, 8.5, 85], [-90, -90, -80, -80]))

############################################
##	Sub-plot G: Class 1 excitable
############################################

'''
         Note eqn for this cell is:
            V = V + tau*(0.04*V^2+4.1*V+108-u+I);
         as opposed to
            V = V + tau*(0.04*V^2+5*V+140-u+I);
         in figure1.m
'''


t_stop = 300.0

#timeStep = globalTimeStep
#totalTimes = np.zeros(0)
#totalAmps = np.zeros(0)
#times = np.linspace(0.0, 30.0, int(1 + (30.0 - 0.0) / timeStep))
#amps = np.linspace(0.0, 0.0, int(1 + (30.0 - 0.0) / timeStep))
#totalTimes = np.append(totalTimes, times)
#totalAmps = np.append(totalAmps, amps)
#times = np.linspace(30 + timeStep, t_stop, int((t_stop - 30) / timeStep))
#amps = np.linspace(0.000075 * timeStep, 0.000075 * (t_stop - 30), int((t_stop - 30) / timeStep))
#totalTimes = np.append(totalTimes, times)
#totalAmps = np.append(totalAmps, amps)




#alt_times, alt_amps = ramp(0.000075, 30.0, t_stop)
#assert (totalTimes == alt_times)
#assert (totalAmps == alt_amps)

run_simulation(a=0.02, b=0.2, c=-65.0, d=6.0, v_init=-70.0,
               waveform=ramp(0.000075, 30.0, t_stop),
               tstop=t_stop, title='(G) Class 1 excitable',
               p_waveform=([0, 30, 300, 300], [-90, -90, -70, -90]),
               xlim=(0.0, 300.0), ylim=(-95.0, 30.0))

############################################
##	Sub-plot H: Class 2 excitable
############################################

t_stop = 300.0
#timeStep = globalTimeStep
#totalTimes = np.zeros(0)
#totalAmps = np.zeros(0)
#times = np.linspace(0.0, 30.0, int(1 + (30.0 - 0.0) / timeStep))
#amps = np.linspace(-0.0005, -0.0005, int(1 + (30.0 - 0.0) / timeStep))
#totalTimes = np.append(totalTimes, times)
#totalAmps = np.append(totalAmps, amps)
#times = np.linspace(30 + timeStep, t_stop, int((t_stop - 30) / timeStep))
#amps = np.linspace(-0.0005 + 0.000015 * timeStep, -0.0005 + 0.000015 * (t_stop - 30), int((t_stop - 30) / timeStep))
#totalTimes = np.append(totalTimes, times)
#totalAmps = np.append(totalAmps, amps)
#
#alt_times, alt_amps = ramp(0.000015, 30.0, t_stop, baseline=-0.0005)
#assert (totalTimes == alt_times)
#assert (totalAmps == alt_amps)

run_simulation(a=0.2, b=0.26, c=-65.0, d=0.0, v_init=-64.0,
               waveform=ramp(0.000015, 30.0, t_stop, baseline=-0.0005),
               tstop=t_stop, title='(H) Class 2 excitable',
               p_waveform=([0, 30, 300, 300], [-90, -90, -70, -90]))

#########################################
##	Sub-plot I: Spike latency
#########################################

t_stop = 100.0
run_simulation(a=0.02, b=0.2, c=-65.0, d=6.0, v_init=-70.0,
               waveform=pulse(0.00671,  # 0.00704 in original
                              [10], 3, t_stop),
               tstop=t_stop, title='(I) Spike latency',
               p_waveform=([0, 10, 10, 13, 13, 100], [-90, -90, -80, -80, -90, -90]))

#################################################
##	Sub-plot J: Subthreshold oscillation
#################################################

t_stop = 200.0
run_simulation(a=0.05, b=0.26, c=-60.0, d=0.0, v_init=-62.0,
               waveform=pulse(0.002, [20], 5, t_stop),
               tstop=t_stop, title='(J) Subthreshold oscillation',
               p_waveform=([0, 20, 20, 25, 25, 200], [-90, -90, -80, -80, -90, -90]))

####################################
##	Sub-plot K: Resonator
####################################

t_stop = 400.0
T1 = t_stop / 10
T2 = T1 + 20
T3 = 0.7 * t_stop
T4 = T3 + 40
run_simulation(a=0.1, b=0.26, c=-60.0, d=-1.0, v_init=-62.0,
               waveform=pulse(0.00065, [T1, T2, T3, T4], 4, t_stop),
               tstop=t_stop, title='(K) Resonator',
               p_waveform=([0, T1, T1, (T1+8), (T1+8), T2, T2, (T2+8), (T2+8), T3, T3, (T3+8), (T3+8), T4, T4, (T4+8), (T4+8), 400],
                           [-90, -90, -80, -80, -90, -90, -80, -80, -90, -90, -80, -80, -90, -90, -80, -80, -90, -90]))


####################################
##	Sub-plot L: Integrator
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
               p_waveform=([0, T1, T1, (T1+2), (T1+2), T2, T2, (T2+2), (T2+2), T3, T3, (T3+2), (T3+2), T4, T4, (T4+2), (T4+2), 100],
                           [-90, -90, -80, -80, -90, -90, -80, -80, -90, -90, -80, -80, -90, -90, -80, -80, -90, -90]))


######################################
##	Sub-plot M: Rebound spike
######################################

t_stop = 200.0
run_simulation(a=0.03, b=0.25, c=-60.0, d=4.0, v_init=-64.0,
               waveform=pulse(-0.015, [20], 5, t_stop),
               tstop=t_stop, title='(M) Rebound spike',
               p_waveform=([0, 20, 20, 25, 25, 200],
                           [-85, -85, -90, -90, -85, -85]))

######################################
##	Sub-plot N: Rebound burst
######################################

t_stop = 200.0
run_simulation(a=0.03, b=0.25, c=-52.0, d=0.0, v_init=-64.0,
               waveform=pulse(-0.015, [20], 5, t_stop),
               tstop=t_stop, title='(N) Rebound burst',
               p_waveform=([0, 20, 20, 25, 25, 200], [-85, -85, -90, -90, -85, -85]))

###############################################
##	Sub-plot O: Threshold variability
###############################################

t_stop = 100.0
times = np.array([0, 10, 15, 70, 75, 80, 85, t_stop])
amps = np.array([0, 0.001, 0, -0.006, 0, 0.001, 0, 0])
run_simulation(a=0.03, b=0.25, c=-60.0, d=4.0, v_init=-64.0,
               waveform=(times, amps),
               tstop=t_stop, title='(O) Threshold variability',
               p_waveform=([0, 10, 10, 15, 15, 70, 70, 75, 75, 80, 80, 85, 85, 100],
                           [-85, -85, -80, -80, -85, -85, -90, -90, -85, -85, -80, -80, -85, -85]))

######################################
##	Sub-plot P: Bistability
######################################

t_stop = 300.0
T1 = t_stop/8
T2 = 208  # 216.0 in original
run_simulation(a=0.1, b=0.26, c=-60.0, d=0.0, v_init=-61.0,
               waveform=pulse(0.00124, [T1, T2], 5, t_stop, baseline=0.00024),
               tstop=t_stop, title='(P) Bistability',
               p_waveform=([0, 300.0/8, 300.0/8, (300.0/8 + 5), (300.0/8 + 5), 216, 216, 221, 221, 300],
                           [-90, -90, -80, -80, -90, -90, -80, -80, -90, -90]))

#####################################################
##	Sub-plot Q: Depolarizing after-potential
#####################################################

t_stop = 50.0
run_simulation(a=1.0, b=0.18, c=-60.0, d=-21.0, v_init=-70.0,
               waveform=pulse(0.02, [9], 2, t_stop),
               tstop=t_stop, title='(Q) DAP',
               p_waveform=([0, 9, 9, 11, 11, 50],
                           [-90, -90, -80, -80, -90, -90]))

#####################################################
##	Sub-plot R: Accomodation
#####################################################

# different model
#    u = u + tau*a*(b*(V+65))

t_stop = 400.0

timeStep = globalTimeStep
totalTimes = np.zeros(0)
totalAmps = np.zeros(0)

times = np.linspace(0.0, 200.0, int(1 + (200.0 - 0.0) / timeStep))
amps = np.linspace(0.0, 0.008, int(1 + (200.0 - 0.0) / timeStep))
totalTimes = np.append(totalTimes, times)
totalAmps = np.append(totalAmps, amps)

times = np.linspace(200 + timeStep, 300, int((300 - 200) / timeStep))
amps = np.linspace(0.0, 0.0, int((300 - 200) / timeStep))
totalTimes = np.append(totalTimes, times)
totalAmps = np.append(totalAmps, amps)

times = np.linspace(300 + timeStep, 312.5, int((312.5 - 300) / timeStep))
amps = np.linspace(0.0, 0.004, int((312.5 - 300) / timeStep))
totalTimes = np.append(totalTimes, times)
totalAmps = np.append(totalAmps, amps)

times = np.linspace(312.5 + timeStep, 400, int((400 - 312.5) / timeStep))
amps = np.linspace(0.0, 0.0, int((400 - 312.5) / timeStep))
totalTimes = np.append(totalTimes, times)
totalAmps = np.append(totalAmps, amps)

parts = (ramp(0.00004, 0.0, 200.0),
         (np.array([200.0, 300.0]), np.array([0.0, 0.0])),
         ramp(0.00032, 300.0, 312.5),
         (np.array([312.5, t_stop]), np.array([0.0, 0.0])))
alt_times, alt_amps = np.hstack(parts)

#assert alt_times == totalTimes
#assert alt_amps == totalAmps

fig2 = plt.figure(2)
plt.plot(totalTimes, totalAmps)
fig3 = plt.figure(3)
plt.plot(alt_times, alt_amps)

run_simulation(a=0.02, b=1.0, c=-55.0, d=4.0, v_init=-65.0, u_init=-16.0,
               waveform=(totalTimes, totalAmps),
               tstop=t_stop, title='(R) Accomodation',
               p_waveform=(totalTimes, 1500 * totalAmps - 90),
               xlim=(0.0, 400.0), ylim=(-95.0, 30.0))

#####################################################
##	Sub-plot S: Inhibition-induced spiking
#####################################################

t_stop = 350.0
run_simulation(a=-0.02, b=-1.0, c=-60.0, d=8.0, v_init=-63.8,
               waveform=pulse(0.075, [50], 170, t_stop, baseline=0.08),
               tstop=t_stop, title='(S) Inhibition-induced spiking',
               p_waveform=([0, 50, 50, 250, 250, 350],
                           [-80, -80, -90, -90, -80, -80]))

#####################################################
##	Sub-plot T: Inhibition-induced bursting
#####################################################

'''
Modifying parameter d from -2.0 to -0.7 in order to reproduce Fig. 1
'''

t_stop = 350.0
run_simulation(a=-0.026, b=-1.0, c=-45.0, d=-0.7, v_init=-63.8,
               waveform=pulse(0.075, [50], 200, t_stop, baseline=0.08),
               tstop=t_stop, title='(T) Inhibition-induced bursting',
               p_waveform=([0, 50, 50, 250, 250, 350],
                           [-80, -80, -90, -90, -80, -80]))

raw_input("Simulation finished... Press enter to exit...")
