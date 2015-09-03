''' izhitest.py
Script to test izhikevich cell model from Izhikevich (2007) "Neural Dynamical Systems" MIT Press 

Cell parameters taken from figures of Izhikevich, 2007 book and implemented using the general eqns (8.5) and (8,6)

Python wrappers and parameters of each cell type defined in izhi.py

Model implemented using NEURON simulator NMDOL in izhi2007.mod

Cell types available are based on Izhikevich, 2007 book:
    1. RS - Layer 5 regular spiking pyramidal cell (fig 8.12 from 2007 book)
    2. IB - Layer 5 intrinsically bursting cell (fig 8.19 from 2007 book)
    3. CH - Cat primary visual cortex chattering cell (fig 8.23 from 2007 book)
    4. LTS - Rat barrel cortex Low-threshold  spiking interneuron (fig 8.25 from 2007 book)
    5. FS - Rat visual cortex layer 5 fast-spiking interneuron (fig 8.27 from 2007 book)
    6. TC and TC_burst - Cat dorsal LGN thalamocortical (TC) cell (fig 8.31 from 2007 book)
    7. RTN and RTN_burst - Rat reticular thalamic nucleus (RTN) cell  (fig 8.32 from 2007 book)

Usage: 
nrniv -python izhi2007Figs.py 
test1(name of cell) eg. test1('RS') or test1('TC_burst')
'''

from neuron import h,gui
import pylab as plt
plt.ion()
import izhi2007Wrapper as izh07
from izhiGUI import choices, izhtype, izh, cell07 # need to make sure can also access everything that will be seen from within 'choices'

## Code to  reproduce figs from Izhikevich, 2007 (book)
testModel = 'RS' # cell type to reproduce (RS, IB, CH, LTS, FS, TC, RTN)
burstMode = 0 # tests bursting mode for TC and RTN cells
save = False # whether to save 
IinRange = []
IinHyper = 0
title = ''
fig1 = None

def test1 (ce, name, izhtype):
  global testModel, burstMode, IinRange, IinHyper, legendLabels, title
  testModel = name
  burstMode = 0
  C, izhm = ce, ce.izh

  if C.type is not testModel:
    C.reparam(testModel)

  legendLabels = ['%s'%(izhtype)]
  # RS
  if testModel == 'RS': 
    h.tstop = 520
    IinRange = [60,70,85,100]           
    title = 'Layer 5 regular spiking (RS) pyramidal cell (fig 8.12)'

  # IB
  elif testModel == 'IB': 
    h.tstop = 600
    IinRange = [290,370,500,550]
    title = 'Layer 5 intrinsic bursting (IB) pyramidal cell (fig 8.19)'

  # CH
  elif testModel == 'CH': 
    h.tstop = 210
    IinRange = [200,300,400,600]
    title = 'Cortical chattering (CH) cell  (fig 8.23)'

  # LTS
  elif testModel == 'LTS': 
    h.tstop = 320
    IinRange = [100,125,200,300]
    title = 'Low-threshold spiking (LTS) interneuron (fig 8.25) '

    # FS
  elif testModel == 'FS': 
    h.tstop = 100
    IinRange = [73.2,100,200,400]
    title = 'Fast-spiking (FS) interneuron (fig 8.27) '

    # TC
  elif testModel == 'TC':
    h.tstop = 650
    IinRange = [50,100,150]
    title = 'Thalamocortical (TC) cell (fig 8.31) '
    
    # TC burst
  elif testModel == 'TC_burst':
    burstMode = 1
    h.tstop = 650
    IinHyper = -1200
    IinRange = [0,50,100]
    title = 'Thalamocortical (TC) cell burst mode (fig 8.31) '

    # RTN
  elif testModel == 'RTN':
    IinRange = [50,70,110]
    h.tstop=650
    title = 'Reticular thalamic nucleus (RTN) cell (fig 8.32) '

    # RTN burst
  elif testModel == 'RTN_burst':
    burstMode = 1
    IinHyper = -350
    IinRange = [30,50,90]
    h.tstop=720
    title = 'Reticular thalamic nucleus (RTN) cell (fig 8.32) '
  runsim(izhm)

nquantities=4
spikevec = h.Vector()
recvecs = [h.Vector() for q in range(nquantities)] # Initialize vectors
def recorder (ce, vloc):
  izhm = ce.izh
  #record spikes
  spikerecorder = h.NetCon(izhm, None)
  spikerecorder.record(spikevec)
  # record V,u,Iin
  recvecs[0].record(h._ref_t) # Record simulation time
  recvecs[1].record(vloc) # Record cell voltage
  recvecs[2].record(izhm._ref_u) # Record cell recovery variable
  recvecs[3].record(izhm._ref_Iin) # input

## Run sim
def runsim (izhm):
  global Iin, ax1, recvecs
  h.dt = 0.025
  f1 = []
  ax1=None
  if fig1 is not None: plt.clf()
  for Iin in IinRange:
    izhm.Iin=Iin
    h.init()

    if burstMode:
            izhm.Iin=IinHyper
            h.init()
            h.continuerun(120)
            izhm.Iin=Iin
            h.run()
    else:
            h.run()
    plotall()

ax1=None
def plotall ():
    global fig1, Iin, ax1, legend
    if fig1 is None: fig1 = plt.figure(figsize=(6,10), tight_layout=True)
    ax = fig1.add_subplot(len(IinRange),1,len(IinRange)-IinRange.index(Iin),sharex=ax1)
    if not ax1: ax1=ax
    ax.plot(recvecs[0], recvecs[1])
    ax.set_xlabel('t (ms)     (for Iin=%d pA)'%int(Iin))
    ax.set_xlim([0,h.tstop])
    ax.set_ylabel('V (mV)')
    if IinRange.index(Iin)==0: 
            plt.legend(legendLabels)
    if IinRange.index(Iin)==len(IinRange)-1: 
            ax.set_title(title)
    plt.draw()
    if save: 
      burstText=['', '_burstMode']
      fig1.savefig('%s%s.png'%(testModel,burstText[burstMode]))
    plt.show()

def closeFig():
  global fig1
  plt.close('all')
  fig1 = None
