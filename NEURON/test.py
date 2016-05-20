
import sys

from neuron import h, gui

plot = not '-nogui' in sys.argv

fih = []

# make a 2007b (section) cell
sec07b = h.Section('soma')
sec07b.L, sec07b.diam, sec07b.cm = 5, 6.3, 1
sec07b.L, sec07b.diam, sec07b.cm = 10, 10, 31.831 * 1
iz07b = h.Izhi2007b(0.5,sec=sec07b)
iz07b.Iin = 0
iz07b.C = 1


h("objref stim")
h(" stim = new IClamp(0.500000)  ")
h(" stim.del = 0  ")
h(" stim.dur = 10000  ")
h(" stim.amp = 0.1  ")

def iz07b_init(): sec07b.v=-60
fih.append(h.FInitializeHandler(iz07b_init))

h('forall psection()')

# vectors and plot
h.tstop=520


trec = h.Vector()
trec.record(h._ref_t)

h.dt = 0.0025

h.steps_per_ms = 1/h.dt

if plot:
    # Display: display_d1
    display_d1 = h.Graph(0)
    display_d1.size(0,h.tstop,-80.0,50.0)
    display_d1.view(0, -80.0, h.tstop, 130.0, 80, 330, 330, 250)
    h.graphList[0].append(display_d1)
    # Line, plotting: RS_pop[0]/v
    display_d1.addexpr("v(0.5)", "v(0.5)", 1, 1, 0.8, 0.9, 2)

    # Display: display_d2
    display_d2 = h.Graph(0)
    display_d2.size(0,h.tstop,-80.0,50.0)
    display_d2.view(0, -80.0, h.tstop, 130.0, 80, 330, 330, 250)
    h.graphList[0].append(display_d2)
    display_d2.addexpr("Izhi2007b[0].u", "Izhi2007b[0].u", 1, 1, 0.8, 0.9, 2)


# File to save: time
# Column: time
h(' objectvar v_time ')
h(' { v_time = new Vector() } ')
h(' v_time.record(&t) ')
h.v_time.resize((h.tstop * h.steps_per_ms) + 1)

# File to save: of0
# Column: RS_pop[0]/v
h(' objectvar v_v_of0 ')
h(' { v_v_of0 = new Vector() } ')
h(' v_v_of0.record(&v(0.5)) ')
h.v_v_of0.resize((h.tstop * h.steps_per_ms) + 1)
# Column: RS_pop[0]/u
h(' objectvar v_u_of0 ')
h(' { v_u_of0 = new Vector() } ')
h(' v_u_of0.record(&Izhi2007b[0].u) ')
h.v_u_of0.resize((h.tstop * h.steps_per_ms) + 1)


if plot:
    h.nrncontrolmenu()

h.run()


if plot:
    display_d1.exec_menu("View = plot")
    display_d2.exec_menu("View = plot")

py_v_time = [ t/1000 for t in h.v_time.to_python() ]  # Convert to Python list for speed...


# File to save: of0
py_v_v_of0 = [ float(x  / 1000.0) for x in h.v_v_of0.to_python() ]  # Convert to Python list for speed, variable has dim: voltage
py_v_u_of0 = [ float(x  / 1.0E9) for x in h.v_u_of0.to_python() ]  # Convert to Python list for speed, variable has dim: current

f_of0_f2 = open('RS_One.dat', 'w')
for i in range(int(h.tstop * h.steps_per_ms) + 1):
    f_of0_f2.write('%e\t'% py_v_time[i]  + '%e\t'%(py_v_v_of0[i])  + '%e\t'%(py_v_u_of0[i]) + '\n')
f_of0_f2.close()
print("Saved data to: RS_One.dat")