"""
izh.py

Python/NEURON GUI for the different celltypes of Izhikevich neuron (versions from 2 publications). 

* 2003 Izhikevich artificial neuron model from 
EM Izhikevich "Simple Model of Spiking Neurons"
IEEE Transactions On Neural Networks, Vol. 14, No. 6, November 2003 pp 1569-1572

* 2007 Izhikevich artificial neuron model from 
EM Izhikevich (2007)  "Dynamical systems in neuroscience" MIT Press

Cell types available from Izhikevich, 2007 book:
    1. RS - Layer 5 regular spiking pyramidal cell (fig 8.12 from 2007 book)
    2. IB - Layer 5 intrinsically bursting cell (fig 8.19 from 2007 book)
    3. CH - Cat primary visual cortex chattering cell (fig8.23 from 2007 book)
    4. LTS - Rat barrel cortex Low-threshold  spiking interneuron (fig8.25 from 2007 book)
    5. FS - Rat visual cortex layer 5 fast-spiking interneuron (fig8.27 from 2007 book)
    6. TC - Cat dorsal LGN thalamocortical (TC) cell (fig8.31 from 2007 book)
    7. RTN - Rat reticular thalamic nucleus (RTN) cell  (fig8.32 from 2007 book)

Implementation by: Salvador Dura-Bernal, Cliff Kerr, Bill Lytton 
(salvadordura@gmail.com; cliffk@neurosim.downstate.edu; billl@neurosim.downstate.edu)
"""

# adapted from /u/billl/nrniv/sync/izh.hoc
import os, sys, collections
import numpy as np
from neuron import h, gui
h.load_file('stdrun.hoc')
import izhi2007Figs as iz07fig
import izhi2007Wrapper as izh07
import __main__
py = __main__
h.tstop=500
h.cvode_active(0)
h.dt=0.1
izh, cell07 = None, None # must be declared here since needs to be imported elsewhere


type2003 = collections.OrderedDict([
  #                                 a         b     c         d    vviv      tstop
 ('regular spiking (RS)'        , (0.02   ,  0.2 , -65.0 ,   8.0 , -63.0 ,   150.0)) ,
 ('intrinsically bursting (IB)' , (0.02   ,  0.2 , -55.0 ,   4.0 , -70.0 ,   150.0)) ,
 ('chattering (CH)'             , (0.02   ,  0.2 , -50.0 ,   2.0 , -70.0 ,   150.0)) ,
 ('fast spiking (FS)'           , (0.1    ,  0.2 , -65.0 ,   2.0 , -70.0 ,   150.0)) ,
 ('thalamo-cortical (TC)'       , (0.02   , 0.25,  -65.0 , 0.05 , -63.0 ,   150.0)) ,
 ('thalamo-cortical burst (TC)' , (0.02   , 0.25,  -65.0 , 0.05 , -87.0 ,   150.0)) ,
 ('resonator (RZ)'              , (0.1   ,  0.26 , -65.0 ,   2.0 , -70.0 ,   100.0)) ,
 ('low-threshold spiking (LTS)' , (0.02   , 0.25 , -65.0 ,   2.0 , -63.0 ,   250.0))])

type2004 = collections.OrderedDict([
  #                                 a         b     c         d    vviv      tstop
 ('tonic spiking'               , (0.02   ,  0.2 , -65.0 ,   6.0 , -70.0 ,   100.0)) ,
 ('mixed mode'                  , (0.02   ,  0.2 , -55.0 ,   4.0 , -70.0 ,   160.0)) ,
 ('spike latency'               , (0.02   ,  0.2 , -65.0 ,   6.0 , -70.0 ,   100.0)) ,
 ('rebound spike'               , (0.03   , 0.25 , -60.0 ,   4.0 , -64.0 ,   200.0)) ,
 ('Depolarizing afterpotential' , (1.0    ,  0.2 , -60.0 , -21.0 , -70.0 ,    50.0)) ,
 ('phasic spiking'              , (0.02   , 0.25 , -65.0 ,   6.0 , -64.0 ,   200.0)) ,
 ('spike frequency adaptation'  , (0.01   ,  0.2 , -65.0 ,   8.0 , -70.0 ,    85.0)) ,
 ('subthreshold oscillations'   , (0.05   , 0.26 , -60.0 ,   0.0 , -62.0 ,   200.0)) ,
 ('rebound burst'               , (0.03   , 0.25 , -52.0 ,   0.0 , -64.0 ,   200.0)) ,
 ('accomodation'                , (0.02   ,  1.0 , -55.0 ,   4.0 , -65.0 ,   400.0)) ,
 ('tonic bursting'              , (0.02   ,  0.2 , -50.0 ,   2.0 , -70.0 ,   220.0)) ,
 ('Class 1'                     , (0.02   , -0.1 , -55.0 ,   6.0 , -60.0 ,   300.0)) ,
 ('resonator'                   , (0.1    , 0.26 , -60.0 ,  -1.0 , -62.0 ,   400.0)) ,
 ('threshold variability'       , (0.03   , 0.25 , -60.0 ,   4.0 , -64.0 ,   100.0)) ,
 ('inhibition-induced spiking'  , (-0.02  , -1.0 , -60.0 ,   8.0 , -63.8 ,   350.0)) ,
 ('phasic bursting'             , (0.02   , 0.25 , -55.0 ,  0.05 , -64.0 ,   200.0)) ,
 ('Class 2'                     , (0.2    , 0.26 , -65.0 ,   0.0 , -64.0 ,   300.0)) ,
 ('integrator'                  , (0.02   , -0.1 , -55.0 ,   6.0 , -60.0 ,   100.0)) ,
 ('bistability'                 , (0.1    , 0.26 , -60.0 ,   0.0 , -61.0 ,   300.0)) ,
 ('inhibition-induced bursting' , (-0.026 , -1.0 , -45.0 ,  -2.0 , -63.8 , 350.0))])

choices = collections.OrderedDict([
  ('2003 PP model' ,  (lambda: h.Izhi2003a(0.5,sec=cell03),  lambda: izh._ref_V,      type2003)),
  ('2003 Sec model',  (lambda: h.Izhi2003b(0.5,sec=cell03), lambda: cell03(0.5)._ref_v, type2003)),
  ('2004 PP model' ,  (lambda: h.Izhi2003a(0.5,sec=cell03),  lambda: izh._ref_V,      type2004)),
  ('2004 Sec model',  (lambda: h.Izhi2003b(0.5,sec=cell03), lambda: cell03(0.5)._ref_v, type2004)),
  ('2007 PP model' ,  (lambda: izh07.IzhiCell(host=izh07.dummy), lambda: izh._ref_V, izh07.type2007)),
  ('2007 Sec model' , (lambda: izh07.IzhiCell(), lambda: cell07.sec(0.5)._ref_v, izh07.type2007))])

ch=choices.keys()
def newmodel (ty=None) : 
  "2003,2004 was the orig model; 2007 is the redesign; look at global izhtype if no "
  return izhtype.find('2007') > -1 if ty is None else ty.find('2007') > -1

#* setup the cell
izhtype='2004 PP model'
def cellset ():
  global cell07, cell03, izh, vref, uvvset, fih, izhtype
  if newmodel():
    cell07 =  choices[izhtype][0]()
    izh = cell07.izh
    def uvvset () : pass
  else: 
    cell03 = h.Section(name="cell2003") # this cell will be used for 2003/4; different cell created in izhi2007Wrapper for those
    izh =  choices[izhtype][0]()
    def uvvset () : vref[0], izh.u = vviv, vviv*izh.b
    cell03.L, cell03.diam = 6.37, 5 # empirically tuned -- cell size only used for Izh1
  fih = [h.FInitializeHandler(uvvset), h.FInitializeHandler(0,Isend)]
  vref = choices[izhtype][1]() # can define this afterwards even though used in uvvset above
  # h('objref izh'); h.izh = izh # if need to access from hoc

#* parameters for different cell types
playvec, playtvec = [h.Vector() for x in range(2)]

# initialization routines
name, params = None, None

def p (nm, pm=None) :
  global name, vviv, params, vvset
  if pm is None : pm = choices[izhtype][2][nm]
  name, params = nm, pm
  if newmodel():
    izh.C, izh.k, izh.vr, izh.vt, izh.vpeak, izh.a, izh.b, izh.c, izh.d, izh.celltype = params
    h.tstop=1000
  else: 
    izh.a, izh.b, izh.c, izh.d, vviv, h.tstop = params
  g.size(0,h.tstop,-100,50)
  try: 
    if newmodel():
      graphx() # interviews graphics
      iz07fig.recorder(cell07, choices[izhtype][1]()) # vectors to draw under matplotlib
      iz07fig.test1(cell07, nm, izhtype)
    else:
      iz07fig.closeFig()
      graphx()
      playinit()
      h.run()
  except: print sys.exc_info()[0],' :',sys.exc_info()[1]

def ivwrap (func, label=''):
  wrapper = h.VBox()
  wrapper.intercept(1)
  func()
  wrapper.intercept(0)
  wrapper.map(label)
  return wrapper

def graphx ():
  g.erase_all()
  g.addvar("v", choices[izhtype][1](), 2,2)
  g.addvar("u", izh._ref_u, 3,1)
  g.addvar("Iin", izh._ref_Iin if newmodel() else izh._ref_Iin, 4,2)
  try: g.addvar("gsyn", izh._ref_gsyn, 1, 1)
  except: pass

I0=I1=T1=0
def playinit () : 
  global I0,I1,T1
  try: izh.f, izh.g= 5, 140 # standard params: V'=0.04*V^2 + 5*V + 140 - u + Iin
  except: pass
  bub.label[0] = '%s'%(name)
  if name=='Depolarizing afterpotential': bub.label[0] = "%s -- REPEATED SPIKING"%(bub.label[0])
  if name=='accomodation': bub.label[0] = "%s -- NOT IMPLEMENTED (different functional form;see izh.mod)"%(bub.label[0])
  if name=='inhibition-induced bursting': bub.label[0] = "%s -- NOT IMPLEMENTED (convergence problems)"%(bub.label[0])
  g.label(0.1,0.9,bub.label[0])
  print bub.label[0]
  playvec.play_remove()
  playtvec.resize(0); playvec.resize(0)
  if name=='Class 1' :
    T1=30
    playtvec.append(0,T1,h.tstop)
    playvec.append(0,0,0.075*(h.tstop-T1))
  elif name=='Class 2' : #  (H) Class 2 exc.
    T1=30
    playtvec.append(0,T1,h.tstop)
    playvec.append(-0.5, -0.5,-0.05+0.015*(h.tstop-T1))
  elif name=='accomodation' : #  (R) accomodation
    playtvec.append(0, 200,    200.001, 300,     312.5, 312.501, h.tstop)
    playvec.append( 0, 200/25, 0      , 0      , 4    , 0      , 0)
  if name in ['Class 1', 'Class 2', 'accomodation'] : playvec.play(izh._ref_Iin, playtvec, 1)
  if name in ['Class 1', 'integrator'] :
    try: izh.f, izh.g = 4.1, 108 # don't exist in all the models
    except: pass

def synon () : 
  "Turn on a synapse"
  global ns, nc
  ns = h.NetStim()
  nc = h.NetCon(ns,izh,0,1,10)
  ns.start, ns.interval, ns.number = 10, 10, 10
  nc.weight[0] = 2
  izh.taug = 3

#* box of buttons
class Bubox :

  def __init__ (self, type, li) :
    self.izhtype = type
    vbox, hbox, hbox1 = h.VBox(), h.HBox(), h.HBox()
    self.vbox = vbox
    lil = len(li)
    self.cols, self.rows = {20:(4,5), 8:(4,2), 9:(3,3)}[lil]
    self.label=h.ref('================================================================================')
    vbox.intercept(1)
    h.xpanel("")
    h.xvarlabel(self.label)
    if newmodel(self.izhtype):
      h.xlabel("V' = (k*(V-vr)*(V-vt) - u + Iin)/C     if (V>vpeak) V=c  [reset]")
      h.xlabel("u' = a*(b*(V-vr) - u)                  if (V>vpeak) u=u+d")
    else: 
      h.xlabel("v' = 0.04*v*v + f*v + g - u + Iin;     if (v>thresh) v=c [reset]")
      h.xlabel("u' = a*(b*v - u);                    if (v>thresh) u=u+d")
    h.xpanel()
    hbox1.intercept(1)
    h.xpanel(""); h.xbutton("RUN",h.run); h.xpanel()
    self.xvalue('I0','I0')
    self.xvalue('I1','I1')
    self.xvalue('T1','T1')
    hbox1.intercept(0); hbox1.map("")
    hbox.intercept(1)
    for ii,(k,v) in enumerate(li.iteritems()):
      if ii%self.rows==0: h.xpanel("")
      h.xbutton(k, (lambda f, arg1, arg2: lambda: f(arg1,arg2))(p, k, v)) # alternative is to use functools.partial
      if ii%self.rows==self.rows-1: h.xpanel()
    hbox.intercept(0); hbox.map("")
    vbox.intercept(0); vbox.map("Spike patterns")
    self.label[0]=""

  def pr (): pass

  def xvalue (self,name,var,obj=py,runner=pr):
    h.xpanel("")
    h.xvalue(name,(obj, var),0,runner)
    h.xpanel()

  def xpvalue (self,name,ptr,runner=pr):
    "Doesn't work currently"
    h.xpanel("")
    h.xpvalue(name,ptr,1,runner)
    h.xpanel()

  def transpose (self,x) : return int(x/self.rows) + x%self.rows*self.cols
# end class Bubox

# current injections for specific models
def Isend () :
  global T1,I0,I1
  if I0!=0 or I1!=0:
    Iin = I0
    Isend1(T1,I1)
    return
  T1=h.tstop/10
  if not newmodel(): izh.Iin=0
  if name=='tonic spiking':   #  (A) tonic spiking
    Isend1(T1,14)
  elif name=='phasic spiking':  #  (B) phasic spiking
    T1=20
    Isend1(T1,0.5)
  elif name=='tonic bursting':  #  (C) tonic bursting
    T1=22
    Isend1(T1,15)
  elif name=='phasic bursting':  #  (D) phasic bursting
    T1=20
    Isend1(T1,0.6)
  elif name=='mixed mode':  #  (E) mixed mode
    Isend1(T1,10)
  elif name=='spike frequency adaptation':  #  (F) spike freq. adapt
    Isend1(T1,30)
  elif name=='Class 1':  #  (G) Class 1 exc. -- playvec
    pass
  elif name=='Class 2':  #  (H) Class 2 exc. -- playvec
    pass
  elif name=='spike latency':  #  (izh.Iin) spike latency
    Isend1(T1,7.04)
    Isend1(T1+3,0.0)
  elif name=='subthreshold oscillations':  #  (J) subthresh. osc.
    Isend1(T1,2)
    Isend1(T1+5,0)
  elif name=='resonator':  #  (K) resonator
    T2, T3 = T1+20, 0.7*h.tstop
    T4 = T3+40
    Isend1(T1,0.65) ;   Isend1(T2,0.65)  ;  Isend1(T3,0.65)  ;  Isend1(T4,0.65)
    Isend1(T1+4,0.) ;   Isend1(T2+4,0.)  ;  Isend1(T3+4,0.)  ;  Isend1(T4+4,0.)
  elif name=='integrator':  #  (L) integrator
    T1, T3 = h.tstop/11, 0.7*h.tstop
    T2, T4 = T1+5, T3+10
    Isend1(T1,9)    ; Isend1(T2,9)    ; Isend1(T3,9)    ; Isend1(T4,9)
    Isend1(T1+2,0.) ; Isend1(T2+2,0.) ; Isend1(T3+2,0.) ; Isend1(T4+4,0.)
  elif name=='rebound spike':  #  (M) rebound spike
    T1=20
    Isend1(T1,-15)
    Isend1(T1+5,0)
  elif name=='rebound burst':  #  (N) rebound burst
    T1=20
    Isend1(T1,-15)
    Isend1(T1+5,0)
  elif name=='threshold variability':  #  (O) thresh. variability
    T1, T2, T3 =10, 70, 80
    Isend1(T1,1)    ; Isend1(T2,-6)   ; Isend1(T3,1)
    Isend1(T1+5,0.) ; Isend1(T2+5,0.) ; Isend1(T3+5,0.)
  elif name=='bistability':  #  (P) bistability
    T1, T2, izh.Iin = h.tstop/8, 216, 0.24
    Isend1(T1,1.24) ;   Isend1(T2,1.24)
    Isend1(T1+5,0.24);  Isend1(T2+5,0.24)
  elif name=='Depolarizing afterpotential':  #  (Q) DAP depolarizing afterpotential
    T1 = 10
    Isend1(T1-1,20)
    Isend1(T1+1,0)
  elif name=='accomodation':  #  (R) accomodation -- playvec
    pass
  elif name=='inhibition-induced spiking':  #  (S) inhibition induced spiking
    izh.Iin=80
    Isend1(50,75)
    Isend1(250,80)
  elif name=='inhibition-induced bursting':  #  (T) inhibition induced bursting
    izh.Iin=80
    Isend1(50,80) # Isend1(50,75) -- will crash simulator
    Isend1(250,80)
  elif name=='regular spiking (RS)':  #  regular spiking (RS)
    Isend1(T1,14)
  elif name=='intrinsically bursting (IB)':  #  intrinsically bursting (IB)
    Isend1(T1,11)
  elif name=='chattering (CH)':  #  chattering (CH)
    Isend1(T1,10)
  elif name=='fast spiking (FS)':  #  fast spiking (FS)
    Isend1(T1,10)
  elif name=='thalamo-cortical (TC)':  #  thalamo-cortical (TC)
    Isend1(2*T1,1.5)
  elif name=='thalamo-cortical burst (TC)':  #  thalamo-cortical burst (TC)
    Isend1(0,-25)
    Isend1(3*T1,0)
  elif name=='resonator (RZ)':  #  resonator (RZ)
    Isend1(0,-2)
    Isend1(T1,-0.5)
    Isend1(T1+50,10)
    Isend1(T1+55,-0.5)
  elif name=='low-threshold spiking (LTS)':  #  low-threshold spiking (LTS)
    Isend1(T1,10)    
  elif name == 'TC_burst': # thalamo-cortical burst (TC) (2007)
    Isend1(0,-1200) 
    Isend1(120,110)
  elif name == 'RTN_burst': # reticular thalamic nucleus burst (TC) (2007)
    Isend1(0,-350) 
    Isend1(120,90)

def Isend1 (tm, Iin) :
  def my_event():
    izh.Iin = Iin
    h.CVode().re_init()
  h.cvode.event(tm, my_event)

# izhstim() sets up a single stim into izh cell
# effect easily seen by running "Class 1"
def izhstim () :
  stim=h.NetStim(0.5)
  stim.number = stim.start = 1
  nc = h.NetCon(stim,izh)
  nc.delay = 2
  nc.weight = 0.1
  izh.erev = -5

#* plotting & printing
g, nmenu, bub = None, None, None
def isinstanceh (objref,objtype) : return objref.hname().startswith(objtype.hname()[:-2])

def winup (izht=izhtype):
  global bub, g, nmenu, izhtype
  izhtype = izht  # swap in the new one
  cellset()
  if g is None: 
    g=h.Graph(0)
    h.graphList[0].append(g)
  if g.view_count()<1: 
    g.view(-0.1*h.tstop,-90,1.2*h.tstop,150,300,200,400,200)
    g.size(0,h.tstop,-80,40)
  if not bub is None: bub.vbox.unmap()
  bub = Bubox(izhtype,choices[izhtype][2])
  bub.label[0] = izhtype
  if not nmenu is None: nmenu.unmap()
  nmenu = ivwrap(lambda: h.nrnpointmenu(izh), izh.hname())

def chwin ():
  "Launch windows from model list"
  h.xpanel("Izhikevich models")
  # outer lambda returns inner lambda so as to pass arg to winup() -- the innermost routine
  for c in ch:
    h.xbutton(c, (lambda f, arg1: lambda: f(arg1))(winup,c)) 
  h.xpanel()

def vtvec(vv): return np.linspace(0, len(vv)*h.dt, len(vv), endpoint=True)

if __name__ == '__main__': chwin()
