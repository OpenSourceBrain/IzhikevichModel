'''

NOT YET COMPLETE...

'''
from neuroml.loaders import read_neuroml2_file

nml_doc = read_neuroml2_file('FiveCells.net.nml')

for iz in nml_doc.izhikevich_cells:
    print('Found: %s'%(iz.id))
    
    '''
    
    <izhikevichCell id="izTonicSpiking" v0 = "-70mV" thresh = "30mV" a ="0.02" b = "0.2" c = "-65" d = "6"/>
    
    0.04 * v^2    +    5 * v     + 140.0
    
    = 0.04 * (v^2  +  125 * v   +  3500)
    
    = 0.04 * (v - (-42.3443)) * (v - (-82.6556))
    
    
<izhikevich2007Cell id="RS" v0 = "-60mV" C="100 pF" k = "0.7 nS_per_mV"
                        vr = "-60 mV" vt = "-40 mV" vpeak = "35 mV" 
                        a = "0.03 per_ms" b = "-2 nS" c = "-50 mV" d = "100 >
                        
    k * (v-vr) * (v-vt)
                        
                        
    '''
    
    v0 = '%s'%iz.v0
    vr = '-42.3443 mV'
    vt = '-82.6556 mV'
    vpeak = '%s'%iz.thresh
    
    
    a = '%s per_ms'%iz.a
    b = '%s nS'%iz.b
    c = '%s mV'%iz.c
    d = '%s pA'%iz.d
    
    k = '0.04 nS_per_mV'
    C = '100 pF'
    
    iz2007 = '<izhikevich2007Cell id="%s" v0="%s" vt="%s" vr="%s" vpeak="%s" \n'%(iz.id,v0,vt,vr,vpeak) \
            +'                    a="%s" b="%s" c="%s" d="%s" k="%s" C="%s"/>\nNOT YET COMPLETE...'%(a,b,c,d,k,C)
    
    print(iz2007)
