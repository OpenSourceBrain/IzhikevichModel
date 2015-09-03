%   This MATLAB file generates figures from the book 
%               Izhikevich E.M. (2007) 
%   "Dynamical systems in neuroscience"

%%%%%%%%%%%%%%% (A) tonic spiking %%%%%%%%%%%%%%%%%%%%%%
clear all;
close all;
%% Set params to reproduce figs from Izhikevich, 2007 (book)
testModel = 'RS'; % cell type to reproduce (RS, IB, CH, LTS, FS, TC, RTN)
burstMode = 0; % tests bursting mode for TC and RTN cells

% RS - Layer 5 regular spiking (RS) pyramidal cell (fig 8.12 from 2007 book)
if strcmp(testModel, 'RS')
	T=520;
	IinRange = [60,70,85,100];
	figtitle = 'Layer 5 regular spiking (RS) pyramidal cell (fig 8.12)';
    C=100; k=0.7; vr=-60; vt=-40; vpeak=35; a=0.03; b=-2; c=-50; d=100; celltype=1;

% IB -  Layer 5 intrinsically bursting (IB) cell (fig 8.19 from 2007 book)
elseif strcmp(testModel, 'IB')
	T=600;
	IinRange = [290,370,500,550];
	figtitle = 'Layer 5 intrinsic bursting (IB) pyramidal cell (fig 8.19)';
    C=150; k=1.2; vr=-75; vt=-45; vpeak=50; a=0.01; b=5; c=-56; d=130; celltype=2;

% CH - Cat primary visual cortex chattering (CH) cell (fig 8.23 from 2007 book)
elseif strcmp(testModel, 'CH') 
	T=210;
	IinRange = [200,300,400,600];
	figtitle = 'Cortical chattering (CH) cell  (fig 8.23)';
	C=50; k=1.5; vr=-60; vt=-40; vpeak=25; a=0.03; b=1; c=-40; d=150; celltype=3;

% LTS - Rat barrel cortex Low-threshold  spiking (LTS) interneuron (fig 8.25 from 2007 book)
elseif strcmp(testModel, 'LTS')
	T=320;
	IinRange = [100,125,200,300];
	figtitle = 'Low-threshold spiking (LTS) interneuron (fig 8.25)';
	C=100; k=1; vr=-56; vt=-42; vpeak=40; a=0.03; b=8; c=-53; d=20; celltype=4;

% FS - Layer 5 rat visual cortex fast-spiking (FS) interneuron (fig8.27 from 2007 book)
elseif strcmp(testModel, 'FS')
	T=100;
	IinRange = [73.2,100,200,400];
	figtitle = 'Fast-spiking (FS) interneuron (fig 8.27) ';
	C=20; k=1; vr=-55; vt=-40; vpeak=25; a=0.2; b=-2; c=-45; d=-55; celltype=5;

% TC - Cat dorsal LGN thalamocortical (TC) cell (fig 8.31 from 2007 book)
elseif strcmp(testModel, 'TC')
	T=650;
    if burstMode
		Iin0 = -1200; % required to lower Vrmp to -80mV for 120 ms
		IinRange = [0,50,100];
    else
		IinRange = [50,100,150];
    end
	figtitle = 'Thalamocortical (TC) cell (fig 8.31) ';
    C=200; k=1.6; vr=-60; vt=-50; vpeak=35; a=0.01; b=15; c=-60; d=10; celltype=6;

% RTN - Rat reticular thalamic nucleus (RTN) cell  (fig8.32 from 2007 book)
elseif strcmp(testModel, 'RTN')
    if burstMode
		Iin0 = -350;
		IinRange = [30,50,90];
		T=720;
    else
		IinRange = [50,70,110];
		T=650;
    end
	figtitle = 'Reticular thalamic nucleus (RTN) cell (fig 8.32)';
	C=40; k=0.25; vr=-65; vt=-45; vpeak=0; a=0.015; b=10; c=-55; d=50; celltype=7;
end

%% Code to implement artificial neuron model        

tau=0.25; %dt
index = 0;
figure('Position', [50, 50, 550, 750]);
for Iinput=IinRange
    index = index + 1; % subplot index
    n=round(T/tau); % number of samples
    
    if burstMode
        n0 = 120/tau; % initial period of 120 ms to lower Vrmp to -80mV
        I=[Iin0*ones(1,n0),Iinput*ones(1,n)];% 2 different pulses of input DC current
        n = n+n0;
    else
        I=[Iinput*ones(1,n)];% pulse of input DC current
    end
    
    v=vr*ones(1,n);  % initialize variables
    u=0*v;
    for i=1:n-1                         % forward Euler method
        v(i+1) = v(i) + tau * (k * (v(i) - vr) * (v(i) - vt) - u(i) + I(i)) / C;
 
    %  Cell-type specific dynamics
    if (celltype < 5) % default 
        u(i+1)=u(i)+tau*a*(b*(v(i)-vr)-u(i)); % Calculate recovery variable
    else 
        if (celltype == 5)  % For FS neurons, include nonlinear U(v): U(v) = 0 when v<vb ; U(v) = 0.025(v-vb) when v>=vb (d=vb=-55)
            if (v(i+1) < d) 
                u(i+1) = u(i) + tau*a*(0-u(i));
            else
                u(i+1) = u(i) + tau*a*((0.025*(v(i)-d).^3)-u(i));
            end
        elseif (celltype == 6) % For TC neurons, reset b
           if (v(i+1) > -65) 
               b=0;
           else
               b=15;
           end
           u(i+1)=u(i)+tau*a*(b*(v(i)-vr)-u(i)); 
        elseif (celltype==7) %For TRN neurons, reset b
            if (v(i+1) > -65)
                b=2;
            else
                b=10;
            end
            u(i+1)=u(i)+tau*a*(b*(v(i)-vr)-u(i));
        end
    end
        
    %  Check if spike occurred and need to reset
    if (celltype < 4 || celltype == 5 || celltype == 7) % default
        if v(i+1)>=vpeak
            v(i)=vpeak;
            v(i+1)=c;
            if celltype ~= 5, u(i+1)=u(i+1)+d; end % reset u, except for FS cells
        end
    elseif (celltype == 4) % LTS cell
        if v(i+1) > (vpeak - 0.1*u(i+1))
            v(i)=vpeak - 0.1*u(i+1);
            v(i+1) = c+0.04*u(i+1); % Reset voltage
            if ((u+d)<670)
                u(i+1)=u(i+1)+d; % Reset recovery variable
            else
                u(i+1) = 670;
            end
        end
    elseif (celltype == 6) % TC cell
        if v(i+1) > (vpeak + 0.1*u(i+1))
            v(i)=vpeak + 0.1*u(i+1);
            v(i+1) = c-0.1*u(i+1); % Reset voltage
            u(i+1)=u(i+1)+d;
        end
    end
    end
    
    % plot V
    subplot(length(IinRange),1,length(IinRange)-index+1); % plot
    plot(tau*(1:n), v);		
    xlabel(['t (ms)     (Iin=', num2str(round(I(i))),' pA)']);
    xlim([0,n*tau])
	ylabel('V (mV)')
    if index == length(IinRange), title(figtitle); end
end
