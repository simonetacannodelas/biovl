# -*- coding: utf-8 -*-
"""
Created on Friday Jan 24 13:34:32 2020

@author: simoca
"""

from scipy.integrate import odeint
#Package for plotting
import math
#Package for the use of vectors and matrix
import numpy as np
import pandas as pd
import array as arr
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import glob
from random import sample
import random
import time
import plotly
import plotly.graph_objs as go
import json


class Ecoli_Aero:
    def __init__(self, Control = False):
        self.Kap=0.5088 #g/L
        self.Ksa=0.0128
        self.Kia=1.2602 #g/L
        self.Ks= 0.0381 #g/L
        self.Kis = 1.8383 #g/L affinity constant
        self.Ko = 0.0001
        self.qAcmax= 0.1148 #g/gh
        self.qm=0.0133 #g/gh
        self.qOmax= 13.4*31.9988/1000 #g/gh
        self.qSmax= 0.635 #g/gh
        self.Yas= 0.8938 #g/g
        self.Yoa= 0.5221 #g/g
        self.Yos= 1.5722 #g/g
        self.Yxa= 0.5794 #g/g
        self.Yem = 0.5321 #g/g
        self.Yxsof = 0.229  # g/g
        self.pAmax= 0.2286 #gA/gXh
        self.kla= 220
        self.H= 1400 #Henry constant

        self.G0 = 4.94
        self.A0 = 0.0129
        self.O0 = 98
        self.X0 = 0.17
        self.tau= 35 #response time
        self.t_start = 0
        self.V0 = 2
        self.F0 = 0
        self.SFR = 1.5
        self.t_expfb_start = 0
        self.t_constfb_start = 1.5
        self.t_end = 15
        
        #parameters for control, default every 1/24 hours:
        self.Control = Control
        self.coolingOn = True
        self.Contamination=False
        self.steps = (self.t_end - self.t_start)*24
        self.T0 = 35
        self.K_p = 2.31e+01
        self.K_i = 1
        self.K_d = 0
        self.Tset = 30
        self.u_max = 150
        self.u_min = 0

    def rxn(self, C,t , u, fc):
        #when there is no control, k has no effect
        k=1
        #when cooling is off than u = 0
        if self.coolingOn == False:
            u = 0
        if self.Contamination == True:
            fc=np.random.randint(0,10)
            fc=fc/17

        if self.Control == True :
            #Cardinal temperature model with inflection: Salvado et al 2011 "Temperature Adaptation Markedly Determines Evolution within the Genus Saccharomyces"
            #Strain E.coli  W310
            Topt = 35
            Tmax = 45.48
            Tmin = 10
            T = C[5]
            if T < Tmin or T > Tmax:
                 k = 0
            else:
                 D = (T-Tmax)*(T-Tmin)**2
                 E = (Topt-Tmin)*((Topt-Tmin)*(T-Topt)-(Topt-Tmax)*(Topt+Tmin-2*T))
                 k = D/E
        # Volume balance
        if (t >= self.t_expfb_start):
            if (t < self.t_constfb_start):
                Fin = self.F0 * math.exp(self.SFR * (t - self.t_expfb_start))
                Fout = 0
            else:
                Fin = self.F0 * math.exp(self.SFR * (self.t_constfb_start - self.t_expfb_start))
                Fout = 0
        else:
            Fin = 0
            Fout = 0

        F = Fin - Fout

        qS = (self.qSmax/(1+C[1]/self.Kia))*(C[0]/(C[0]+self.Ks))
        qSof = self.pAmax*(qS/(qS+self.Kap))
        pA = qSof*self.Yas
        qSox = (qS-qSof)*(C[2]/(C[2]+self.Ko))
        qSan = (qSox-self.qm)*self.Yem*(0.488/0.391)
        qsA = (self.qAcmax/(1+(qS/self.Kis)))*(C[1]/(C[1]+self.Ksa))
        qA = pA - qsA
        mu = (qSox - self.qm)*self.Yem+ qsA*self.Yxa + qSof*self.Yxsof
        qO = self.Yos*(qSox-qSan)+qsA*self.Yoa

        #Solving the mass balances
        dGdt = (F/C[4])*(self.G0-C[0])-(qS*C[3])
        dAdt = qA*C[3]-((F/C[4])*C[1])
        dOdt = self.kla*(self.O0-C[2])-qO*C[3]*self.H
        dXdt = (mu - (F/C[4]))*C[3]
        dVdt = F
        if self.Control == True :
            '''
             dHrxn heat produced by cells estimated by yeast heat combustion coeficcient dhc0 = -21.2 kJ/g
             dHrxn = dGdt*V*dhc0(G)-dEdt*V*dhc0(E)-dXdt*V*dhc0(X)
             (when cooling is working)  Q = - dHrxn -W ,
             dT = V[L] * 1000 g/L / 4.1868 [J/gK]*dE [kJ]*1000 J/KJ
             dhc0(EtOH) = -1366.8 kJ/gmol/46 g/gmol [KJ/g]
             dhc0(Glc) = -2805 kJ/gmol/180g/gmol [KJ/g]
             
            ''' 
            #Metabolic heat: [W]=[J/s], dhc0 from book "Bioprocess Engineering Principles" (Pauline M. Doran) : Appendix Table C.8 
            dHrxndt =   dXdt*C[4]*(-21200) #[J/s]  + dGdt*C[4]*(15580)- dEdt*C[4]*(29710) 
            #Shaft work 1 W/L1
            W = 1*C[4] #[J/S] negative because exothermic  
            #Cooling just an initial value (constant cooling to see what happens)
            #dQdt = -0.03*C[4]*(-21200) #[J/S]   
            #velocity of cooling water: u [m3/h] -->controlled by PID       
            
            #Mass flow cooling water
            M=u/3600*1000 #[kg/s]
            #Define Tin = 5 C, Tout=TReactor
            #heat capacity water = 4190 J/kgK
            Tin = 5
            #Estimate water at outlet same as Temp in reactor
            Tout = C[5]
            cpc = 4190
            #Calculate Q from Eq 9.47
            Q=-M*cpc*(Tout-Tin) # J/s    
            #Calculate Temperature change
            dTdt = -1*(dHrxndt - Q + W)/(C[4]*1000*4.1868) #[K/s]
        else: 
            dTdt = 0
        return [dGdt,dAdt,dOdt,dXdt,dVdt, dTdt]
                
    def solve(self):
        #solve normal:
        t = np.linspace(self.t_start, self.t_end, self.steps)
        if self.Control == False :
            u = 0
            fc= 1
            C0 = [self.G0, self.A0, self.O0, self.X0,self.V0,self.T0]
            C = odeint(self.rxn, C0, t, rtol = 1e-7, mxstep= 500000, args=(u,fc,))
    
        #solve for Control
        else:
            fc=0
            """
            PID Temperature Control:
            """
            # storage for recording values
            C = np.ones([len(t), 6]) 
            C0 = [self.G0, self.A0, self.O0, self.X0,self.V0,self.T0]
            C[0] = C0
            self.ctrl_output = np.zeros(len(t)) # controller output
            e = np.zeros(len(t)) # error
            ie = np.zeros(len(t)) # integral of the error
            dpv = np.zeros(len(t)) # derivative of the pv
            P = np.zeros(len(t)) # proportional
            I = np.zeros(len(t)) # integral
            D = np.zeros(len(t)) # derivative
            
            for i in range(len(t)-1):
                #print(t[i])
                #PID control of cooling water
                dt = t[i+1]-t[i]
                #Error
                e[i] = C[i,5] - self.Tset  
                #print(e[i])
                if i >= 1:
                    dpv[i] = (C[i,5]-C[i-1,5])/dt
                    ie[i] = ie[i-1] + e[i]*dt
                P[i]=self.K_p*e[i]
                I[i]=self.K_i*ie[i]
                D[i]=self.K_d*dpv[i]
                
                self.ctrl_output[i]=P[i]+I[i]+D[i]
                u=self.ctrl_output[i]
                if u>self.u_max:
                    u=self.u_max
                    ie[i] = ie[i] - e[i]*dt # anti-reset windup
                if u < self.u_min:
                    u =self.u_min
                    ie[i] = ie[i] - e[i]*dt # anti-reset windup
                #time for solving ODE    
                ts = [t[i],t[i+1]]
                #disturbance
                #if self.t[i] > 5 and self.t[i] < 10:
                #   u = 0                
                #solve ODE from last timepoint to new timepoint with old values              
    
                y =  odeint(self.rxn, C0, ts, rtol = 1e-7, mxstep= 500000, args=(u,fc,))
                #update C0
                C0 = y[-1]
                #merge y to C
                C[i+1]=y[-1]
        return t, C
    def create_plot(self, t, C):
        S = C[:, 0]
        A = C[:, 1]
        B = C[:, 3]
        df = pd.DataFrame({'t': t, 'Substrate': S, 'Biomass': B, 'Acetate': A})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['t'], y=df['Substrate'], name='Glucose'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['Biomass'], name='Biomass'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['Acetate'], name='Acetate'))
        fig.update_layout(title=('Simulation of aerobic batch growth of Escherichia coli by acetate cycling'),
                          xaxis_title='time (h)',
                          yaxis_title='Concentration (g/L)')
        print('print')
        graphJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJson

    def add_noise(self,t,C):
        PV = []
        PV2 = []
        PV3 = []
        PV4 = []
        import numpy as np
        C_noise = np.zeros((C.shape))
        import numpy as np
        for i in range(len(t)):
            PV.append((((math.sin(t[i] * 33)) / 17) + (math.cos(t[i] * 17)) / 83))
            PV2.append(0.67 * (((math.sin(t[i] * 31)) / 11) + (math.cos(t[i] * 23)) / 73))
            PV3.append(0.37 * (((math.sin(t[i] * 23)) / 7) + (math.cos(t[i] * 37)) / 53))
            PV4.append(0.19 * (((math.sin(t[i] * 19)) / 3) + (math.cos(t[i] * 53)) / 37))
        for i in range(len(C[0])):
            C_noise[:, i] = (C[:, i] + PV * C[:, i] + PV2 * C[:, i] - PV3 * C[:, i] - PV4 * C[:, i])
            # C_noise[:, i] = C[:, i]*(math.exp(PV)+math.exp(PV2)+math.exp(PV3)+math.exp(PV4))
        S = C[:, 0]
        S_noise =C_noise[:,0]
        A = C[:, 1]
        A_noise =C_noise[:,1]
        B = C[:, 3]
        B_noise=C_noise[:, 3]
        df = pd.DataFrame({'t': t, 'Substrate': S, 'Biomass': B, 'Acetate': A,'Substrate noise': S_noise, 'Biomass noise': B_noise, 'Acetate noise': A_noise,})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['t'], y=df['Substrate'], name='Glucose'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['Biomass'], name='Biomass'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['Acetate'], name='Acetate'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['Substrate noise'], name='Glucose noise'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['Biomass noise'], name='Biomass noise'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['Acetate noise'], name='Acetate noise'))
        fig.update_layout(title=('Simulation of aerobic batch growth of Escherichia coli by acetate cycling'),
                          xaxis_title='time (h)',
                          yaxis_title='Concentration (g/L)')
        print('print')
        graphJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJson


f= Ecoli_Aero()
f.solve()
C= f.solve()[1]
print(C)

# plt.plot(f.solve()[0], f.solve()[1][:,0])
# plt.plot(f.solve()[0], f.solve()[1][:,1])
# # plt.plot(f.solve()[0], f.solve()[1][:,2])
# plt.plot(f.solve()[0], f.solve()[1][:,3])
# plt.show()