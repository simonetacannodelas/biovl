# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 13:34:32 2018

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

class SCerevisiae_Aero:
    def __init__(self, Control = False):
        self.Yox_XG = 0.8
        self.Yred_XG = 0.05
        self.Yox_XE =  0.72
        self.Y_OG = 1.067
        self.Y_EG = 0.5
        self.Y_OE = 1.5
        self.q_g = 3.5
        self.q_o = 0.37
        self.q_e = 0.32
        self.t_lag = 4.66
        self.Kg = 0.17
        self.Ke = 0.56
        self.Ko = 0.0001
        self.Ki = 0.31
        self.O_sat = 0.00755
        self.kla = 1004
        
        self.G0 = 18
        self.E0 = 0.0
        self.O0 = 0.00755
        self.X0 = 0.1
        
        self.t_end = 30
        self.t_start = 0
        self.V0 = 2
        
        #parameters for control, default every 1/24 hours:
        self.Control = Control
        self.coolingOn = True
        self.Contamination=False
        self.steps = (self.t_end - self.t_start)*24
        self.T0 = 30
        self.K_p = 2.31e+01
        self.K_i = 3.03e-01
        self.K_d = -3.58e-03
        self.Tset = 30
        self.u_max = 150
        self.u_min = 0
    def dict(self):
        dictParameters = {'Yox_XG': 'Yield for the oxidative pathway of glucose to biomass',
                          'Yred_XG':'Yield of the reductive pathway of glucose to biomass',
                          'Yox_XE': 'Yield of the pathway of ethanol to biomass',
                          'Y_OG': 'Yield of the need of oxygen to glucose',
                          'Y_EG': 'Yield of the need of ethanol to glucose',
                          'q_o': 'Maximal specific oxygen uptake rate',
                          'q_g': 'Maximal specific glucose  uptake rate',
                          'q_e': 'Maximal specific ethanol uptake rate',
                          't_lag': 'Lag time',
                          'Kg': 'Saturation parameter for glucose uptake',
                          'Ke':'Saturation parameter for ethanol uptake',
                          'Ko':'Saturation parameter for oxygen uptake',
                          'Ki': 'Inhibition parameter: free glucose inhibits ethanol uptake',
                          'O_sat': 'Concentration of saturated oxygen',
                          'kla': 'Mass transfer coefficient for oxygen'
                          }
        return dictParameters

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
            #Strain S. cerevisiae PE35 M
            Topt = 30
            Tmax = 45.48
            Tmin = 5.04 
            T = C[5]
            if T < Tmin or T > Tmax:
                 k = 0
            else:
                 D = (T-Tmax)*(T-Tmin)**2
                 E = (Topt-Tmin)*((Topt-Tmin)*(T-Topt)-(Topt-Tmax)*(Topt+Tmin-2*T))
                 k = D/E 
                      
        #number of components
        n = 4
        m = 4
        #initialize the stoichiometric matrix, s
        s = np.zeros((m,n))        
        s[0,0] = -1
        s[0,1] = 0
        s[0,2] = -self.Y_OG
        s[0,3] = self.Yox_XG
        
        s[1,0] = -1
        s[1,1] = self.Y_EG
        s[1,2] = 0
        s[1,3] = self.Yred_XG
        
        s[2,0] = 0
        s[2,1] = -1
        s[2,2] = -self.Y_OE
        s[2,3] = self.Yox_XE
        
        s[3,0] = 0
        s[3,1] = 0
        s[3,2] = 1
        s[3,3] = 0
        #initialize the rate vector
        rho = np.zeros((4,1))
        ##initialize the overall conversion vector
        r=np.zeros((4,1))
        rho[0,0] = k*((1/self.Y_OG)*min(self.q_o*(C[2]/(C[2]+self.Ko)),self.Y_OG*(self.q_g*(C[0]/(C[0]+self.Kg)))))*C[3]
        rho[1,0] = k*((1-math.exp(-t/self.t_lag))*((self.q_g*(C[0]/(C[0]+self.Kg)))-(1/self.Y_OG)*min(self.q_o*(C[2]/(C[2]+self.Ko)),self.Y_OG*(self.q_g*(C[0]/(C[0]+self.Kg))))))*C[3]
        rho[2,0] = k*((1/self.Y_OE)*min(self.q_o*(C[2]/(C[2]+self.Ko))-(1/self.Y_OG)*min(self.q_o*(C[2]/(C[2]+self.Ko)),self.Y_OG*(self.q_g*(C[0]/(C[0]+self.Kg)))),self.Y_OE*(self.q_e*(C[1]/(C[1]+self.Ke))*(self.Ki/(C[0]+self.Ki)))))*C[3]
        rho[3,0] = self.kla*(self.O_sat - C[2])
    
        #Developing the matrix, the overall conversion rate is stoichiometric *rates
        r[0,0] = (s[0,0]*rho[0,0])+(s[1,0]*rho[1,0])+(s[2,0]*rho[2,0])+(s[3,0]*rho[3,0])
        r[1,0] = (s[0,1]*rho[0,0])+(s[1,1]*rho[1,0])+(s[2,1]*rho[2,0])+(s[3,1]*rho[3,0])
        r[2,0] = (s[0,2]*rho[0,0])+(s[1,2]*rho[1,0])+(s[2,2]*rho[2,0])+(s[3,2]*rho[3,0])
        r[3,0] = (s[0,3]*rho[0,0])+(s[1,3]*rho[1,0])+(s[2,3]*rho[2,0])+(s[3,3]*rho[3,0])
    
        #Solving the mass balances
        dGdt = r[0,0]
        dEdt = r[1,0]*fc
        dOdt = r[2,0]
        dXdt = r[3,0]
        dVdt = 0
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
        return [dGdt,dEdt,dOdt,dXdt,dVdt, dTdt]
                
    def solve(self):
        #solve normal:
        t = np.linspace(self.t_start, self.t_end, self.steps)
        if self.Control == False :
            u = 0
            fc= 1
            C0 = [self.G0, self.E0, self.O0, self.X0,self.V0,self.T0]
            C = odeint(self.rxn, C0, t, rtol = 1e-7, mxstep= 500000, args=(u,fc,))
    
        #solve for Control
        else:
            fc=0
            """
            PID Temperature Control:
            """
            # storage for recording values
            C = np.ones([len(t), 6]) 
            C0 = [self.G0, self.E0, self.O0, self.X0,self.V0,self.T0]
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
        G = C[:, 0]
        E = C[:, 1]
        B = C[:, 3]
        df = pd.DataFrame({'t': t, 'G': G, 'B': B, 'E': E})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['t'], y=df['G'], name='Glucose'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['B'], name='Biomass'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['E'], name='Ethanol'))
        fig.update_layout(title=('Simulation of the model for the Scerevisiae'),
                          xaxis_title='time (h)',
                          yaxis_title='Concentration (g/L)')
        print('print')
        graphJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJson
SCerevisiae_Aero()
SCerevisiae_Aero().solve()
print(SCerevisiae_Aero().solve())
# t = f.solve()[0]
# C = f.solve()[1]
# f.create_plot(t,C)



# class PlotCanvas(FigureCanvas):
#     def __init__(self, parent=None, width= 9 , height=4, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=dpi)
#         self.axes = fig.add_subplot(111)
#         fig.subplots_adjust(right = 0.6,top = 0.8)
#         FigureCanvas.__init__(self, fig)
#         self.setParent(parent)
#
#         FigureCanvas.setSizePolicy(self,
#                 QSizePolicy.Expanding,
#                 QSizePolicy.Expanding)
#         FigureCanvas.updateGeometry(self)
#         self.plot(C ,t)
#
#     def plot(self,C,t):
#         data = C
#         time = t
#         #plot C dependent of t:
#
#         ax = self.figure.add_subplot(111)
#         ax2 = ax.twinx()
#         ax3 = ax.twinx()
#         ax4 = ax.twinx()
#
#         ax3.spines['right'].set_position(('axes',1.15))
#         ax4.spines['right'].set_position(('axes',1.37))
#
#         l1, = ax.plot(time, data[:len(time),3], color = 'g',label = 'Biomass')
#         l2, = ax2.plot(time, data[:len(time),1], color = 'r',label = 'Ethanol')
#         l3, = ax3.plot(time, data[:len(time),0], color = 'b',label = 'Glucose')
#         l4, = ax4.plot(time, data[:len(time),2]*1000, color = 'y',label = 'Oxygen')
#
#         labels = [l1, l2, l3, l4]
#         ax.legend(labels, [l.get_label() for l in labels], loc = 'lower left', bbox_to_anchor = (0,1.05,1,0.5),mode = 'expand', ncol=3)
#
#         ax.set_title('')
#         ax.set_xlabel('time [h]')
#         ax3.set_ylabel('Glucose [g/L]', color = 'b')
#         ax2.set_ylabel('Ethanol [g/L]', color = 'r')
#         ax.set_ylabel('Biomass [g/L]', color = 'g')
#         ax4.set_ylabel('Oxygen [mg/L]', color = 'y')
#         if hasattr(modelInUse, 't_expfb_start'):
#             ax5 = ax.twinx()
#             ax5.spines['right'].set_position(('axes',1.57))
#             l5, = ax5.plot(time, data[:len(time),4], color = 'grey',label = 'Volume')
#             labels = [l1, l2, l3, l4, l5]
#             ax.legend(labels, [l.get_label() for l in labels], loc = 'lower left', bbox_to_anchor = (0,1.05,1,0.5),mode = 'expand', ncol=3, fontsize = 'small')
#             ax5.set_ylabel('Volume [L]', color = 'grey')
#
#             ymin, ymax = ax.get_ylim()
#             #seperate phases on the diagramm and plot text which phase is plotted
#             ax.text(x = (modelInUse.t_expfb_start/2) , y = ymax + 0.5 ,
#                     s= 'Batch phase', fontsize = 7, horizontalalignment='center' )
#             ax.axvline(x= modelInUse.t_expfb_start, color = 'black', linestyle = '--')
#             ax.text(x = (modelInUse.t_expfb_start+modelInUse.t_constfb_start)/2  , y = ymax + 0.5,
#                         s= 'exp FB', fontsize = 7, horizontalalignment='center')
#
#             ax.axvline(x=modelInUse.t_constfb_start, color = 'black', linestyle = '--')
#             ax.text(x = (modelInUse.t_constfb_start+modelInUse.t_end)/2 , y = ymax + 0.5,
#                     s= 'const FB', fontsize = 7, horizontalalignment='center')
#         if hasattr(modelInUse, 't_feed_start'):
#             ax5 = ax.twinx()
#             ax5.spines['right'].set_position(('axes',1.55))
#             l5, = ax5.plot(time, data[:len(time),4], color = 'grey',label = 'Volume')
#             labels = [l1, l2, l3, l4, l5]
#             ax.legend(labels, [l.get_label() for l in labels], loc = 'lower left', bbox_to_anchor = (0,1.05,1,0.5),mode = 'expand', ncol=3, fontsize = 'small')
#             ax5.set_ylabel('Volume [L]', color = 'grey')
#
#
#             ymin, ymax = ax.get_ylim()
#             ax.text(x = (modelInUse.t_feed_start/2) , y = ymax + 0.5 ,
#                     s= 'Batch phase', fontsize = 7, horizontalalignment='center' )
#             ax.axvline(x= modelInUse.t_feed_start, color = 'black', linestyle = '--')
#             ax.text(x = (modelInUse.t_feed_start+modelInUse.t_end)/2  , y = ymax + 0.5,
#                         s= 'CSTR phase', fontsize = 7, horizontalalignment='center')
#
#         self.draw()

# def create_plot(modelInUse, title):
#     f = modelInUse().solve()
#     if modelInUse == 'Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Batch':
#         t = f[0]
#         G = f[1][:,0]
#         E = f[1][:,1]
#         B = f[1][:,3]
#         df = pd.DataFrame({'t': t, 'G': G, 'B':B, 'E':E})
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(x = df['t'],y=df['G'], name='Glucose'))
#         fig.add_trace(go.Scatter(x=df['t'], y=df['B'], name='Biomass'))
#         fig.add_trace(go.Scatter(x=df['t'], y=df['E'], name='Ethanol'))
#         fig.update_layout(title=('Simulation of the model for the %s' % title),
#                           xaxis_title='time (h)',
#                           yaxis_title='Concentration (g/L)')
#         graphJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     return graphJson

