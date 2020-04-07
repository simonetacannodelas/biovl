# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 18:33:18 2018

@author: bjogut and simoca
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

class SCerevisiae_Fedbatch:
    def __init__(self):
        self.Yox_XG = 0.8
        self.Yred_XG = 0.05
        self.Yox_XE =  0.72
        self.Y_OG = 1.067
        self.Y_EG = 0.5
        self.Y_OE = 1.5
        self.q_g = 4.68
        self.q_o = 0.37
        self.q_e = 0.86
        self.t_lag = 4.66
        self.Kg = 0.17
        self.Ke = 0.0001
        self.Ko = 0.56
        self.Ki = 0.31
        self.O_sat = 0.00755
        self.kla = 1004
        self.G0 = 18
        self.E0 = 0.34
        self.O0 = 0.00755
        self.X0 = 0.1
        self.t_end = 30
        self.V0 = 2
        self.Cin = 100
        self.F0 = 0.05
        self.SFR = 0.15
        self.t_expfb_start = 15
        self.t_constfb_start = 18
        self.t_end = 25    

            
    def rxn(self, C,t):
        #matrix
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
        #Volume balance
        if (t>=self.t_expfb_start):
            if (t < self.t_constfb_start):
                Fin = self.F0*math.exp(self.SFR*(t-self.t_expfb_start))
                Fout = 0
            else:
                Fin = self.F0*math.exp(self.SFR*(self.t_constfb_start-self.t_expfb_start))
                Fout = 0
        else:
            Fin = 0
            Fout = 0
         
        F = Fin - Fout       
         
        rho[0,0] = ((1/self.Y_OG)*min(self.q_o*(C[2]/(C[2]+self.Ko)),self.Y_OG*(self.q_g*(C[0]/(C[0]+self.Kg)))))*C[3]
        rho[1,0] = ((1-math.exp(-t/self.t_lag))*((self.q_g*(C[0]/(C[0]+self.Kg)))-(1/self.Y_OG)*min(self.q_o*(C[2]/(C[2]+self.Ko)),self.Y_OG*(self.q_g*(C[0]/(C[0]+self.Kg))))))*C[3]
        rho[2,0] = ((1/self.Y_OE)*min(self.q_o*(C[2]/(C[2]+self.Ko))-(1/self.Y_OG)*min(self.q_o*(C[2]/(C[2]+self.Ko)),self.Y_OG*(self.q_g*(C[0]/(C[0]+self.Kg)))),self.Y_OE*(self.q_e*(C[1]/(C[1]+self.Ke))*(self.Ki/(C[0]+self.Ki)))))*C[3]
        rho[3,0] = self.kla*(self.O_sat - C[2])
    
        #Developing the matrix, the overall conversion rate is stoichiometric *rates
        r[0,0] = (s[0,0]*rho[0,0])+(s[1,0]*rho[1,0])+(s[2,0]*rho[2,0])+(s[3,0]*rho[3,0])
        r[1,0] = (s[0,1]*rho[0,0])+(s[1,1]*rho[1,0])+(s[2,1]*rho[2,0])+(s[3,1]*rho[3,0])
        r[2,0] = (s[0,2]*rho[0,0])+(s[1,2]*rho[1,0])+(s[2,2]*rho[2,0])+(s[3,2]*rho[3,0])
        r[3,0] = (s[0,3]*rho[0,0])+(s[1,3]*rho[1,0])+(s[2,3]*rho[2,0])+(s[3,3]*rho[3,0])
    
        
        #Solving the mass balances terms for dilution, addtion and washing out added  
        dGdt = r[0,0] -F/C[4]*C[0] + Fin/C[4]*self.Cin - Fout/C[4]*C[0]   
        dEdt = r[1,0] -F/C[4]*C[1] - Fout/C[4]*C[1]      
        dOdt = r[2,0]      
        dXdt = r[3,0] -F/C[4]*C[3] - Fout/C[4]*C[3]
        dVdt = F
        return [dGdt,dEdt,dOdt,dXdt, dVdt]
                
        
    def solve(self):
        #time
        t = np.linspace(0, self.t_end)
        C0 = [self.G0, self.E0, self.O0, self.X0, self.V0]
        C = odeint(self.rxn, C0, t, rtol = 1e-7, mxstep= 500000)
        return t, C

    def create_plot(self, t, C):
        G = C[:, 0]
        E = C[:, 1]
        O = C[:, 2]
        B = C[:, 3]
        V = C[:, 4]
        df = pd.DataFrame({'t': t, 'G': G, 'B': B, 'E': E, 'O':O, 'V':V})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['t'], y=df['G'], name='Glucose'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['B'], name='Biomass'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['E'], name='Ethanol'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['O'], name='Oxygen'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['V'], name='Volumen'))
        fig.update_layout(title=('Simulation of the model for the Scerevisiae in fed-batch'),
                          xaxis_title='time (h)',
                          yaxis_title='Concentration (g/L)')
        print('print')
        graphJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJson

    def add_noise(self, t, C):
        PV = []
        PV2 = []
        PV3 = []
        PV4 = []
        import numpy as np
        C_noise = np.zeros((C.shape))
        import numpy as np
        for i in range(len(t)):
            O = 57
            W = 23
            PV.append((((math.sin(t[i] * O)) / W) + (math.cos(t[i] * O*1.5)) / (W*3)))
            PV2.append(0.67 * (((math.sin(t[i] * 0.8*O)) / (W*0.8)) + (math.cos(t[i] *  O*2.5)) / (W*2.75)))
            PV3.append(0.37 * (((math.sin(t[i] * 0.77*O)) / (W*0.6)) + (math.cos(t[i] *  O*3)) /(W*2)))
            PV4.append(0.19 * (((math.sin(t[i] * 0.66*O)) / (W*0.4)) + (math.cos(t[i] *  O*3.5)) / (W*1.5)))
        for i in range(len(C[0])):
            C_noise[:, i] = (C[:, i] + PV*C[:, i] + PV2*C[:, i] - PV3*C[:, i] - PV4*C[:, i])
        G = C[:, 0]
        E = C[:, 1]
        O = C[:, 2]
        B = C[:, 3]
        V = C[:, 4]
        G_noise = C_noise[:, 0]
        E_noise = C_noise[:, 1]
        O_noise = C_noise[:, 2]
        B_noise = C_noise[:, 3]
        V_noise = C_noise[:, 4]
        df = pd.DataFrame({'t': t, 'G': G, 'B': B, 'E': E, 'O':O, 'V':V, 'G_noise': G_noise, 'B_noise': B_noise, 'E_noise': E_noise, 'O_noise':O_noise, 'V_noise':V_noise})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['t'], y=df['G'], name='Glucose'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['B'], name='Biomass'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['E'], name='Ethanol'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['O'], name='Oxygen'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['V'], name='Volumen'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['G_noise'], name='Glucose noise'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['B_noise'], name='Biomass noise'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['E_noise'], name='Ethanol noise'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['O_noise'], name='Oxygen noise'))
        fig.add_trace(go.Scatter(x=df['t'], y=df['V_noise'], name='Volumen noise'))
        fig.update_layout(title=('Simulation of the model for the Scerevisiae in fed-batch'),
                          xaxis_title='time (h)',
                          yaxis_title='Concentration (g/L)')
        graphJson = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJson
    
#class PlotCanvas(FigureCanvas):
#    def __init__(self, parent=None, width= 9 , height=4, dpi=100):
#        fig = Figure(figsize=(width, height), dpi=dpi)
#        self.axes = fig.add_subplot(111)
#        fig.subplots_adjust(right = 0.6,top = 0.8)
#        FigureCanvas.__init__(self, fig)
#        self.setParent(parent)
#        
#        FigureCanvas.setSizePolicy(self,
#                QSizePolicy.Expanding,
#                QSizePolicy.Expanding)
#        FigureCanvas.updateGeometry(self)
#        self.plot(C ,t)
#
#    def plot(self,C,t):
#        data = C
#        time = t
#        #plot C dependent of t:
#        
#        ax = self.figure.add_subplot(111)
#        ax2 = ax.twinx()
#        ax3 = ax.twinx()
#        ax4 = ax.twinx()
#        
#        ax3.spines['right'].set_position(('axes',1.15))
#        ax4.spines['right'].set_position(('axes',1.37))
#        
#        l1, = ax.plot(time, data[:len(time),3], color = 'g',label = 'Biomass')
#        l2, = ax2.plot(time, data[:len(time),1], color = 'r',label = 'Ethanol')
#        l3, = ax3.plot(time, data[:len(time),0], color = 'b',label = 'Glucose')
#        l4, = ax4.plot(time, data[:len(time),2]*1000, color = 'y',label = 'Oxygen')
#        
#        labels = [l1, l2, l3, l4]
#        ax.legend(labels, [l.get_label() for l in labels], loc = 'lower left', bbox_to_anchor = (0,1.05,1,0.5),mode = 'expand', ncol=3)
#          
#        ax.set_title('')
#        ax.set_xlabel('time [h]')
#        ax3.set_ylabel('Glucose [g/L]', color = 'b')
#        ax2.set_ylabel('Ethanol [g/L]', color = 'r')
#        ax.set_ylabel('Biomass [g/L]', color = 'g')
#        ax4.set_ylabel('Oxygen [mg/L]', color = 'y')
#        if hasattr(modelInUse, 't_expfb_start'):
#            ax5 = ax.twinx()
#            ax5.spines['right'].set_position(('axes',1.57))
#            l5, = ax5.plot(time, data[:len(time),4], color = 'grey',label = 'Volume')
#            labels = [l1, l2, l3, l4, l5]
#            ax.legend(labels, [l.get_label() for l in labels], loc = 'lower left', bbox_to_anchor = (0,1.05,1,0.5),mode = 'expand', ncol=3, fontsize = 'small')
#            ax5.set_ylabel('Volume [L]', color = 'grey')
#            
#            ymin, ymax = ax.get_ylim()
#            #seperate phases on the diagramm and plot text which phase is plotted
#            ax.text(x = (modelInUse.t_expfb_start/2) , y = ymax + 0.5 ,
#                    s= 'Batch phase', fontsize = 7, horizontalalignment='center' )
#            ax.axvline(x= modelInUse.t_expfb_start, color = 'black', linestyle = '--')
#            ax.text(x = (modelInUse.t_expfb_start+modelInUse.t_constfb_start)/2  , y = ymax + 0.5, 
#                        s= 'exp FB', fontsize = 7, horizontalalignment='center')
#            
#            ax.axvline(x=modelInUse.t_constfb_start, color = 'black', linestyle = '--')
#            ax.text(x = (modelInUse.t_constfb_start+modelInUse.t_end)/2 , y = ymax + 0.5,
#                    s= 'const FB', fontsize = 7, horizontalalignment='center')
#        if hasattr(modelInUse, 't_feed_start'):
#            ax5 = ax.twinx()
#            ax5.spines['right'].set_position(('axes',1.55))
#            l5, = ax5.plot(time, data[:len(time),4], color = 'grey',label = 'Volume')
#            labels = [l1, l2, l3, l4, l5]
#            ax.legend(labels, [l.get_label() for l in labels], loc = 'lower left', bbox_to_anchor = (0,1.05,1,0.5),mode = 'expand', ncol=3, fontsize = 'small')
#            ax5.set_ylabel('Volume [L]', color = 'grey')
#            
#            
#            ymin, ymax = ax.get_ylim()
#            ax.text(x = (modelInUse.t_feed_start/2) , y = ymax + 0.5 ,
#                    s= 'Batch phase', fontsize = 7, horizontalalignment='center' )
#            ax.axvline(x= modelInUse.t_feed_start, color = 'black', linestyle = '--')
#            ax.text(x = (modelInUse.t_feed_start+modelInUse.t_end)/2  , y = ymax + 0.5, 
#                        s= 'CSTR phase', fontsize = 7, horizontalalignment='center')
#                        
#        self.draw()
