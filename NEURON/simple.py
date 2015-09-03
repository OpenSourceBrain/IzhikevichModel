'''Usage: 
import simple
h.run()
simple.show()

Sets up 5 models using default parameters in the .mod files
2 versions of 2003/2004 parameterization: freestanding (3a); in section (3b)
3 versions of 2007/2008 parameterization: freestanding (7a); in section (7b); in sec using wrapper class (7bw)
can graph u, v for any model
simple.show('v3a','v3b') # compare voltage output for the 2 versions of the 2003/2004 parameterization; will NOT be identical
simple.show('v7a','v7b','v7bw') # compare voltage output for 3 versions of the 2007 parameterization
'''

from neuron import h, gui
import numpy as np
import izhi2007Wrapper as izh07
import pylab as plt
import pprint as pp
plt.ion()
fih = []
dummy=h.Section()

# make a 2003a STATE {u,vv} cell (used for 2003, 2004)
iz03a = h.Izhi2003a(0.5,sec=dummy)
iz03a.Iin = 4

# make a 2003b (Section v) cell
sec03b = h.Section() # this section will actually be used
sec03b.L, sec03b.diam = 5, 6.3 # empirically tuned
iz03b = h.Izhi2003b(0.5,sec=sec03b)
iz03b.Iin = 4
def iz03b_init (): sec03b(0.5).v, iz03b.u = -65, -65*iz03b.b
fih.append(h.FInitializeHandler(iz03b_init))

# make a 2007a (NMODL) cell
iz07a = h.Izhi2007a(0.5,sec=dummy)
iz07a.Iin = 70

# make a 2007b (section) cell
sec07b = h.Section()
sec07b.L, sec07b.diam = 5, 6.3
iz07b = h.Izhi2007b(0.5,sec=sec07b)
iz07b.Iin = 70
def iz07b_init(): sec07b.v=-60
fih.append(h.FInitializeHandler(iz07b_init))

# make a 2007b (section) cell using the Wrapper
iz07bw = izh07.IzhiCell() # defaults to RS
iz07bw.izh.Iin = 70
fih.append(h.FInitializeHandler(iz07bw.init))

# vectors and plot
h.tstop=1250
recd = {'u3a':[iz03a._ref_u], 'v3a':[iz03a._ref_V], 'u3b':[iz03b._ref_u], 'v3b':[sec03b(0.5)._ref_v], 
        'u7a':[iz07a._ref_u], 'v7a':[iz07a._ref_V], 'u7b':[iz07b._ref_u], 'v7b':[sec07b(0.5)._ref_v],
        'u7bw':[iz07bw.izh._ref_u], 'v7bw':[iz07bw.sec(0.5)._ref_v]}
[(v.append(h.Vector(h.tstop/h.dt+100)),v[1].record(v[0])) for x,v in recd.iteritems()]
def vtvec(vv): return np.linspace(0, len(vv)*h.dt, len(vv), endpoint=True)

# run and plot
fig = None
def show (*vars):
  pp.pprint(recd.keys())
  global fig,tvec
  if fig is None: fig = plt.figure(figsize=(10,6), tight_layout=True)
  if len(vars)==0: vars=recd.keys()
  tvec=vtvec(recd['v7a'][1])
  plt.clf()
  [plt.plot(tvec,v[1]) for x,v in recd.iteritems() if x in vars]
  pp.pprint([v[1].as_numpy()[-5:] for x,v in recd.iteritems() if x in vars])
  plt.xlim(0,h.tstop)

# h.run()
# show()
