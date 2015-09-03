## Izhikevich artificial neuron model from 2 different publications: 1) Izhikevich et al, 2003; and 2) Izhikevich, 2007.

**Files:**

[izhi2003a.mod](izhi2003a.mod) // integrates STATE {u, vv}; firing patterns in 2003,
2004 papers; POINT_PROCESS Izhi2003a

[izhi2003b.mod](izhi2003b.mod) // integrates STATE {u}; v calculated in a Section;
firing patterns in 2003, 2004 papers; POINT_PROCESS Izhi2003b

[izhi2007a.mod](izhi2007a.mod) // no STATE -- uses Euler explicit integration update
rule, includes synapses; cell types in 2007 book+syns; POINT_PROCESS
Izhi2007a

[izhi2007b.mod](izhi2007b.mod) // integrates STATE {u}; v calculated in a Section;
firing patterns in 2007 book; POINT_PROCESS Izhi2007b

[izhi2003.m](../MATLAB/izhi2003.m) // Matlab code to replicate firing patterns in 2003 paper
[izhi2007.m](../MATLAB/izhi2007.m) // Matlab code to replicate firing patterns in 2007 book

[simple.py](simple.py) // much brief example to just create 1 of each of the types + 1 additional example using izhi2007Wrapper
[izhiGUI.py](izhiGUI.py) // runs interactive demo of 6 Izhikevich cell models (3 parameter sets, 2 implementations of each)
[izhi2007Figs.py](izhi2007Figs.py) // uses python graphicss to graph firing patterns of 7 cell types in 2007 book
[izhi2007Wrapper.py](izhi2007Wrapper.py) // instantiates the 7 cell types in 2007 book


[izhi2003.png](izhi2003.png) // Illustration of  firing patterns in 2003 paper
[izhi2004.gif](izhi2004.gif) // Illustration of firing patterns in 2004 paper
[izhi2007Comparison.pdf](izhi2007Comparison.pdf) // Illustration of firing patterns in 2007 book
(and comparison to model)

[izhi2004a.hoc](izhi2004a.hoc) // hoc file retained for archaeological interest

[README](README) // original README file (can be read as an org-mode file in emacs)

### 2003-2004 Models

EM Izhikevich "Simple Model of Spiking Neurons" IEEE Transactions On Neural Networks, Vol. 14, No. 6, November 2003 pp 1569-1572

EM Izhikevich "Which model to use for cortical spiking neurons?" IEEE Transactions On Neural Networks, Vol. 15, No. 5, 2004 pp 1063-1070

This single parameterization was used in these 2 papers with different cell-sets being represented, although with some overlap.  We have separately replicated the cell-sets from each paper.

**Solves the following equations:**

     v' = e*v^2 + f*v + g - u + I;    RESET if (v>30) v=c
     u' = a*(b*v-u);                  RESET if (v>30) u=u+d
 
(note that vv is used in for voltage in izhi2003a.mod so doesn't
interfere with built-in v of cell -- the built-in v is used for
izhi2003b.mod)

**a,b,c,d,I are the major parameters; f,g are reset for 2 simulations (G-"Class 1" and L-"integrator")**

3 of the simulations shown in izhi2004.gif are not properly replicated:
Q: depolarizing afterpotential does not repolarize properly
R: accomodation requires an alteration of the functional forms to replicate
   (alternate functional form given on line 52 of izh.mod)
T: too unstable for Neuron integrators to handle
   (changing izh.hoc line 203 to Isend1(50,75) will crash simulator)

### 2007 Models description

Equations and parameter values taken from: Izhikevich EM (2007). "Dynamical systems in neuroscience" MIT Press
Equation for synaptic inputs built-in for izhi2007.mod were taken from: Izhikevich EM, Edelman GM (2008). "Large-scale model of  mammalian thalamocortical systems" PNAS 105 3593-3598.
(Note that this 2008 model is a multicompartmental model that we do not replicate here so we are using 2007 model with 2008 synapses.)

**Solves the following equations:**

    v' = v + (k*(v-vr)*(v-vt) - u - I)/C;  
    u' = u + (a*(b*(v-vr)-u); 
    RESET if v > vpeak: v = c ; u = u + d

(note that additional resets are used for particular models -- ie the
simulation is displaced in the phase plane to produce interruption and
create next stage of dynamics; see below)

**The following parameters specific to each cell type: C, k, vr, vt, vpeak, a, b, c, d and celltype**

Cell types available are based on Izhikevich, 2007 book (chapter
8). Here we include a description of each cell type, the model
parameters required to implement it, and the conditions to replicate
the 2007 book figures:

1. RS - Layer 5 regular spiking pyramidal cell (fig 8.12 from 2007
    book) Parameters: C=100; k=0.7; vr=-60; vt=-40; vpeak=35;
    a=0.03; b=-2; c=-50; d=100; celltype=1 Book fig: T = 520 ms;
    IinRange = [60,70,85,100] pA

2. IB - Layer 5 intrinsically bursting cell (fig 8.19 from 2007
    book) Parameters: C=150; k=1.2; vr=-75; vt=-45; vpeak=50;
    a=0.01; b=5; c=-56; d=130; celltype=2 Book fig: T = 600 ms;
    IinRange = [290,370,500,550] pA

3. CH - Cat primary visual cortex chattering cell (fig 8.23 from
    2007 book) Parameters: C=50; k=1.5; vr=-60; vt=-40; vpeak=25;
    a=0.03; b=1; c=-40; d=150; celltype=3 Book fig: T = 210 ms;
    IinRange = [200,300,400,600] pA

4. LTS - Rat barrel cortex Low-threshold spiking interneuron (fig
    8.25 from 2007 book) Parameters: C=100; k=1; vr=-56; vt=-42;
    vpeak=40; a=0.03; b=8; c=-53; d=20; celltype=4 Book fig: T =
    100 ms; IinRange = [100,125,200,300] pA

5. FS - Rat visual cortex layer 5 fast-spiking interneuron (fig
    8.27 from 2007 book) Parameters: C=20; k=1; vr=-55; vt=-40;
    vpeak=25; a=0.2; b=-2; c=-45; d=-55; celltype=5; Book fig: T =
    100 ms; IinRange = [73.2,100,200,400] pA

6. TC - Cat dorsal LGN thalamocortical (TC) cell (fig 8.31 from
    2007 book) C=200; k=1.6; vr=-60; vt=-50; vpeak=35; a=0.01;
    b=15; c=-60; d=10; celltype=6 Book fig: T = 650 ms; IinRange =
    [50,100,150] pA Book fig (burst mode): T0 = 120 ms; Iin0 =
    -1200 pA; T = 650 ms; IinRange = [0,50,100] pA

7. RTN - Rat reticular thalamic nucleus (RTN) cell (fig 8.32 from
	2007 book) Parameters: C=40; k=0.25; vr=-65; vt=-45;
	vpeak=0; a=0.015; b=10; c=-55; d=50; celltype=7 Book
	fig: T = 650 ms; IinRange = [50,70,110] pA Book fig
	(burst mode): T0 = 120 ms; Iin0 = -350 pA; T = 720 ms;
	IinRange = [30,50,90] pA


Note: The LTS, FS, TC and RTN cells require modifications to the
general equations -- additional resets on phase plane.
See the matlab (izhi2007.m) or the Python/Neuron (izhi2007.mod) for
details. For a full description see chapter 8 of Izhikevich, 2007.

### Compiling with nrnivmodl

    nrnivmodl izhi2003a izhi2003b izhi2007a izhi2007b

### GUI for exploring parameters

    python -i izhiGUI.py
    
Sets up menu to choose among 6 models using 2 different
parameterizations (2003/4 vs 2007) with 3 parameter sets illustrating
different cell dynamics (2003, 2004, 2007) and different
implementation types (voltage in a section vs both u,v calculated in
the mod file).

Each choice brings up a menu of all parameter settings as well as a
menu of standard choices based on cell types.

Simple simulation -- default parameter implementations in simple.py

    python
    import simple
    h.run()
    simple.show()

Sets up 5 models using default parameters in the .mod files:

2 versions of 2003/2004 parameterization: freestanding (3a); in section (3b)
3 versions of 2007/2008 parameterization: freestanding (7a); in section (7b); in sec using wrapper class (7bw) can graph u, v for any model

    simple.show('v3a','v3b') # compare voltage output for the 2 versions of the 2003/2004 parameterization; will NOT be identical

    simple.show('v7a','v7b','v7bw') # compare voltage output for 3 versions of the 2007 parameterization

### MATLAB/Octave versions

See [izhi2003.m](../MATLAB/izhi2003.m) and [izhi2007.m](../MATLAB/izhi2007.m):

	matlab izhi2003.m
	octave --persist izhi2003.m

### Old hoc version for 2004
	
	nrnivmodl izhi2003a
	nrngui izhi2004a.hoc

### Implementation 

Please ask any general questions on NEURON Forum

Salvador Dura-Bernal salvadordura@gmail.com
Cliff Kerr cliffk@neurosim.downstate.edu
Bill Lytton billl@neurosim.downstate.edu


### graphics of simulations -- names indicates which parameterization was used

[izh2003.gif](izh2003.gif) # figure taken from original paper 

[izhi2003.png](izhi2003.png)  # sim results

[izhi2004.gif](izhi2004.gif)  # figure taken from original paper 

[izhi2007Comparison.pdf](izhi2007Comparison.pdf) # side by side comparison of figures from paper
with these sims

