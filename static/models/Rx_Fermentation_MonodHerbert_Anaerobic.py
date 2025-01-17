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


class #Nombre de tu modelo#:
    def __init__(self):
        #Fill up with your parameters
        # Ejemplo:
        #self.Y_XS = 0.8 #g/g


        #Initial state variable
        #Ejemplo:
        #self.S0 = 18

    def rxn(self, C,t, u):
        #when there is no control, k has no effect
        k=1
        #when cooling is off than u = 0
        if self.coolingOn == False:
            u = 0
    
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
        self.s = np.zeros((2,3))
        self.rho=np.zeros((2,1))        
        self.s[0,2]=1
        self.s[0,0]=(-1/self.Y_XS)
        self.s[0,1] = (1/self.Y_PX)
        self.s[1,2]=-1
        
        self.rho[0,0]=((self.mu_max*C[0])/(C[0]+self.Ks))*C[2]
        self.rho[1,0]=self.kd*C[2]

#        print(self.rho)
#        print(self.s)
        self.r= np.zeros((3,1))
        self.r[0,0]= self.s[0,0]*self.rho[0,0]+self.s[1,0]*self.rho[1,0]
        self.r[1,0]= self.s[0,1]*self.rho[0,0]+self.s[1,1]*self.rho[1,0]
        self.r[2,0]= self.s[0,2]*self.rho[0,0]+self.s[1,2]*self.rho[1,0]
        dSdt = self.r[0,0]
        dPdt = self.r[1,0]
        dXdt = self.r[2,0]
        dVdt = 0
#    
#        n = 3
#        m = 3
#        #initialize the stoichiometric matrix, s
#        s = np.zeros((m,n))        
#        s[0,0] = -1/self.Y_XS
#        s[0,1] = -1/self.Y_OX
#        s[0,2] = 1
#        
#        
#        s[1,0] = 0
#        s[1,1] = 1/self.y_x
#        s[1,2] = -1
#        
#        s[2,0] = 0
#        s[2,1] = self.kla
#        s[2,2] = 0       
#        #initialize the rate vector
#        rho = np.zeros((m,1))
#        ##initialize the overall conversion vector
#        r=np.zeros((n,1))
#        rho[0,0] = self.mu_max*(C[0]/(C[0]+self.Ks))*C[2]
#        rho[1,0] = self.kd*C[2]
#        rho[2,0] = self.kla*(self.O_sat - C[1])
#    
#        #Developing the matrix, the overall conversion rate is stoichiometric *rates
#        r[0,0] = (s[0,0]*rho[0,0])+(s[1,0]*rho[1,0])+(s[2,0]*rho[2,0])
#        r[1,0] = (s[0,1]*rho[0,0])+(s[1,1]*rho[1,0])+(s[2,1]*rho[2,0])
#        r[2,0] = (s[0,2]*rho[0,0])+(s[1,2]*rho[1,0])+(s[2,2]*rho[2,0])
#        
#
#        #Solving the mass balances
#        dSdt = r[0,0]
#        dOdt = r[1,0]
#        dXdt = r[2,0]
#        dVdt = 0
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
            W = -1*C[4] #[J/S] negative because exothermic  
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
        return [dSdt, dPdt, dXdt, dVdt, dTdt]  
              
    def solve(self):
        #solve normal:
        t = np.linspace(self.t_start, self.t_end, self.steps)
        if self.Control == False :
            u = 0
            C0 = [self.S0, self.P0, self.X0,self.V0, self.T0]
            C = odeint(self.rxn, C0, t, rtol = 1e-7, mxstep= 500000, args=(u,))
    
        #solve for Control
        else:
            """
            PID Temperature Control:
            """
            # storage for recording values
            C = np.ones([len(t), 6]) 
            C0 = [self.S0, self.P0, self.X0,self.V0,self.T0]
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
    
                y =  odeint(self.rxn, C0, ts, rtol = 1e-7, mxstep= 500000, args=(u,))
                #update C0
                C0 = y[-1]
                #merge y to C
                C[i+1]=y[-1]
            
        return t, C
    
    
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width= 9 , height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.subplots_adjust(right = 0.6,top = 0.8)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(C ,t)

    def plot(self,C,t):
        data = C
        time = t
        #plot C dependent of t:
        
        ax = self.figure.add_subplot(111)
        ax3 = ax.twinx()
        ax4 = ax.twinx()
        
        ax3.spines['right'].set_position(('axes',1.15))
        ax4.spines['right'].set_position(('axes',1.37))
        
        l1, = ax.plot(time, data[:len(time),2], color = 'g',label = 'Biomass')
        l3, = ax3.plot(time, data[:len(time),0], color = 'b',label = 'Substrate')
        l4, = ax4.plot(time, data[:len(time),1]*1000, color = 'r',label = 'Product')
        
        labels = [l1, l3, l4]
        ax.legend(labels, [l.get_label() for l in labels], loc = 'lower left', bbox_to_anchor = (0,1.05,1,0.5),mode = 'expand', ncol=3)
          
        ax.set_title('')
        ax.set_xlabel('time [h]')
        ax3.set_ylabel('Substrate [g/L]', color = 'b')
        ax.set_ylabel('Biomass [g/L]', color = 'g')
        ax4.set_ylabel('Product [g/L]', color = 'r')
        if hasattr(modelInUse, 't_expfb_start'):
            ax5 = ax.twinx()
            ax5.spines['right'].set_position(('axes',1.57))
            l5, = ax5.plot(time, data[:len(time),4], color = 'grey',label = 'Volume')
            labels = [l1, l2, l3, l4, l5]
            ax.legend(labels, [l.get_label() for l in labels], loc = 'lower left', bbox_to_anchor = (0,1.05,1,0.5),mode = 'expand', ncol=3, fontsize = 'small')
            ax5.set_ylabel('Volume [L]', color = 'grey')
            
            ymin, ymax = ax.get_ylim()
            #seperate phases on the diagramm and plot text which phase is plotted
            ax.text(x = (modelInUse.t_expfb_start/2) , y = ymax + 0.5 ,
                    s= 'Batch phase', fontsize = 7, horizontalalignment='center' )
            ax.axvline(x= modelInUse.t_expfb_start, color = 'black', linestyle = '--')
            ax.text(x = (modelInUse.t_expfb_start+modelInUse.t_constfb_start)/2  , y = ymax + 0.5, 
                        s= 'exp FB', fontsize = 7, horizontalalignment='center')
            
            ax.axvline(x=modelInUse.t_constfb_start, color = 'black', linestyle = '--')
            ax.text(x = (modelInUse.t_constfb_start+modelInUse.t_end)/2 , y = ymax + 0.5,
                    s= 'const FB', fontsize = 7, horizontalalignment='center')
        if hasattr(modelInUse, 't_feed_start'):
            ax5 = ax.twinx()
            ax5.spines['right'].set_position(('axes',1.55))
            l5, = ax5.plot(time, data[:len(time),4], color = 'grey',label = 'Volume')
            labels = [l1, l2, l3, l4, l5]
            ax.legend(labels, [l.get_label() for l in labels], loc = 'lower left', bbox_to_anchor = (0,1.05,1,0.5),mode = 'expand', ncol=3, fontsize = 'small')
            ax5.set_ylabel('Volume [L]', color = 'grey')
            
            
            ymin, ymax = ax.get_ylim()
            ax.text(x = (modelInUse.t_feed_start/2) , y = ymax + 0.5 ,
                    s= 'Batch phase', fontsize = 7, horizontalalignment='center' )
            ax.axvline(x= modelInUse.t_feed_start, color = 'black', linestyle = '--')
            ax.text(x = (modelInUse.t_feed_start+modelInUse.t_end)/2  , y = ymax + 0.5, 
                        s= 'CSTR phase', fontsize = 7, horizontalalignment='center')
                        
        self.draw()

    
f = Monod_Herbert_Anaero()
f.solve()
plt.plot(f.solve()[0], f.solve()[1])
plt.show()
