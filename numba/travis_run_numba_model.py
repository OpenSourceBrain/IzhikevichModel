#!/usr/bin/env python
# coding: utf-8

# # This is a reproduction of the MATLAB script 2007.m
#
# The code is implemented in pure python. Performance of the model is atypically good as the model utilizes numba Just In Time compilation.



import matplotlib.pyplot as plt
import collections
import quantities as pq
import izhikevich as izhi
import numpy as np
#get_ipython().run_line_magic('matplotlib', 'inline')
from utils import reduced_cells, transform_input, plot_model
DELAY = 0*pq.ms
DURATION = 250 *pq.ms


# # The JIT model is compiled.
# The first model evaluation compiles the model to C code implicitly, from that point onwards evaluation speeds are fractions of ms. This is fast for python as you can see below.

# In[2]:


IinRange = [60,70,85,100];
params = {}
params['amplitude'] = 500*pq.pA
params['delay'] = DELAY
params['duration'] = 600*pq.ms
fig_title = 'Layer 5 regular spiking (RS) pyramidal cell (fig 8.12)'
plot_model(IinRange,reduced_cells,params,cell_key='RS',title=fig_title,timed=True)


# In[3]:


IinRange = [290,370,500,550];
params = {}
params['delay'] = DELAY
params['duration'] = 600*pq.ms
fig_title = 'Layer 5 intrinsic bursting (IB) pyramidal cell (fig 8.19)'
plot_model(IinRange,reduced_cells,params,cell_key='IB',title=fig_title)


# In[4]:


IinRange = [200,300,400,600];
params = {}
params['delay'] = DELAY
params['duration'] = 210*pq.ms
figtitle='Cortical chattering (CH) cell  (fig 8.23)'
plot_model(IinRange,reduced_cells,params,cell_key='CH',title=figtitle)


# In[5]:


IinRange = [100,125,200,300];
params = {}
params['delay'] = DELAY
T=320;
figtitle = 'Low-threshold spiking (LTS) interneuron (fig 8.25)';
params['duration'] = T*pq.ms
plot_model(IinRange,reduced_cells,params,cell_key='LTS',title=figtitle)


# In[6]:


T=100;
params['duration'] = T*pq.ms
IinRange = [73.2,100,200,400];
figtitle = 'Fast-spiking (FS) interneuron (fig 8.27) ';
plot_model(IinRange,reduced_cells,params,cell_key='FS',title=figtitle)



# # Bursting

# In[7]:


figtitle = 'Thalamocortical (TC) cell (fig 8.31) ';
Iin0 = -1200; #% required to lower Vrmp to -80mV for 120 ms
IinRange = [0,50,100];
T=650;
params['duration'] = T*pq.ms
IinRange = transform_input(T,IinRange,Iin0,burstMode=True)
plot_model(IinRange,reduced_cells,params,cell_key='TC',title=figtitle,direct=True)


# In[8]:


Iin0 = -350;
IinRange = [30,50,90];
IinRange = transform_input(T,IinRange,Iin0,burstMode=True)
T=650;
figtitle = 'Reticular thalamic nucleus (RTN) cell (fig 8.32)';
plot_model(IinRange,reduced_cells,params,cell_key='RTN',title=figtitle,direct=True)
