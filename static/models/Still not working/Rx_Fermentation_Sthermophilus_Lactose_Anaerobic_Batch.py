# -*- coding: utf-8 -*-

from scipy.integrate import odeint
# Package for plotting
import math
# Package for the use of vectors and matrix
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


class Sthermophilus_anae:
    def __init__(self, Control=False):
        #Biological model
        self.mu_max = 2.06 #h^-1
        self.tlag= 0.81 #h
        self.Ks= 0.79 #g/L
        self.Ki= 164 #g/L
        self.Kp_la= 0.24 #g/L
        self.K_la= 19.8 #g/L
        self.Kp_pH1= 20 #g/L
        self.Kp_pH2= 7 #g/L
        self.pHopt= 6.39
        self.spreadparameter= 1.42
        self.alphagrowth= 5.19 #g/g
        self.Y_gal = 0.69 #g/g

        #Mixed weak acid/based model
        self.KrC1=10**7
        self.KrLA=10**7
        self.KrNH=10**12
        self.KrP1=10**8
        self.KrP2=10**12
        self.KrW=10**10
        self.KrZ=10**7
        self.pKw=14
        self.pKz=9.4
        self.T=40
        self.pKc1=3404.7/(self.T-14.8435+0.03279*self.T)
        self.pKla=3.86
        self.pKNH=2835.8/(self.T-0.6322+0.00123*self.T)
        self.pKp1=799.3/(self.T-4.5535+0.01349*self.T)
        self.pKp2=1979.5/(self.T-5.3541+0.01984*self.T)

        # Initial concentrations
        self.S0= 65 #g/L
        self.Gal0 = 0.0  # g/L
        self.X0 = 0.025 #g/L
        self.LA0 = 0.0 #g/L
        self.La0 = 0.0 #g/L
        self.NH30 = 0.0025 #g/L
        self.NH40 = 0 #g/L
        self.PH20 = 2
        self.PH0 = 0
        self.P0 = 0.00
        self.C10=0.01
        self.C20=0.01
        self.H0= 0
        self.OH0=0.01
        self.Z0 = 2 #mol/L
        self.IZ0 = 0


        self.t_end = 10
        self.t_start = 0

        # parameters for control, default every 1/24 hours:
        self.Control = Control
        self.coolingOn = True
        self.Contamination = False
        self.steps = (self.t_end - self.t_start) * 24
        self.T0 = 40
        self.K_p = 2.31e+01
        self.K_i = 3.03e-01
        self.K_d = -3.58e-03
        self.Tset = 30
        self.u_max = 150
        self.u_min = 0

    def rxn(self, C, t):

        #Apparent equilibrium constant
        self.KNHeq=10**(-self.pKNH)
        self.KP1eq=10**(-self.pKp1)
        self.KP2eq=10**(-self.pKp2)
        self.KC1eq=10**(-self.pKc1)
        self.KLaeq=10**(-self.pKla)
        self.KWeq=10**(-self.pKw)
        self.KZeq=10**(-self.pKz)

        # number of components
        n =16
        #0 Lactose
        #1 Galactose
        #2 Biomass
        #3 Lactic acid
        #4 Lactate
        #5 Ammonia
        #6 Ammonium
        #7 Phosphoric acid
        #8 Dihydrogen phosphate
        #9 Hydrogen phosphate
        #10 Carbon dioxide dissolved
        #11 Bicarbonate
        #12 Hydrogen ion
        #13 Hydroxyl ion
        #14 Unknow undissociated acid form
        #15 Unknow dissociated acid form
        # number of processes
        m = 9
        # initialize the stoichiometric matrix, s
        s = np.zeros((m, n))

        #Biological process
        #Biomass growth

        #Biomass growth
        rho[0, 0] = ((-1-self.Y_gal) + self.Y_gal + 1 -0.22 -0.002)*self.mu_max*(C[0]/(C[0]+self.Ks))*(self.Ki/(C[3]+self.Ki))*math.exp(-(self.pHopt-C[12])**2/(self.spreadparameter**2))*C[2]
        #Lactic acid production
        rho[1, 0] = ((-1-self.Y_gal) + self.Y_gal + 1/3 + 1/3)*self.alphagrowth*(self.mu_max*(C[0]/(C[0]+self.Ks))*(self.Ki/(C[3]+self.Ki))*math.exp(-(self.pHopt-C[12])**2/(self.spreadparameter**2))*C[2])
        #Ammonia dissociation
        rho[2, 0] =(self.KNHeq*self.KrNH)*C[6]-self.KrNH*C[5]*C[12]
        #Phosphate dissociate 1
        rho[3, 0] = (self.KP1eq*self.KrP1)*C[7]-self.KrP1*C[9]*C[12]
        #Phosphate dissociate 2
        rho[4,0] = (self.KP2eq*self.KrP2)*C[8]-self.KrP2*C[9]*C[12]
        # Carbonate dissociation 1
        rho[5,0] = (self.KC1eq*self.KrC1)*C[10]-self.KrC1*C[11]*C[12]
        # Lactate dissociation
        rho[6,0] = (self.KLaeq*self.KrLA)*C[3]-self.KrLA*C[4]
        #Water dissociation
        rho[7,0] = 1-self.KrW*C[12]*C[13]
        #Dissociation of unknown compound
        rho[8,0] = (self.KZeq*self.KrZ)*C[14]-self.KrZ*C[15]*C[12]
        # Developing the matrix, the overall conversion rate is stoichiometric *rate
        res=np.zeros((9,1))
        for i in range(len(s)):
            for j in range(len(rho[0])):
                for k in range (len(rho)):
                    res[i][j] += s[i][k]*rho[k][j]
        print(res)
        # Solving the mass balances
        dXdt = res[0, 0]
        dLAdt= res[1, 0]
        dNHdt = res[2, 0]
        dP1dt = res[3, 0]
        dP2dt = res[4, 0]
        dCOdt = res[5, 0]
        dLadt = res[6, 0]
        dWdt = res[7, 0]
        dZdt = res[8, 0]


        return [dXdt, dLAdt, dNHdt, dP1dt, dP2dt, dCOdt, dLadt, dWdt, dZdt]

    def solve(self):
         t = np.linspace(self.t_start, self.t_end, self.steps)
         C0 = ([self.S0, self.Gal0, self.X0, self.LA0, self.La0, self.NH30, self.NH40, self.PH20, self.PH0, self.P0, self.C10, self.C20, self.H0, self.OH0, self.Z0, self.IZ0])
         C = odeint(self.rxn, C0, t, rtol=1e-7, mxstep=500000)
         return t, C

#
f = Sthermophilus_anae()
C = f.solve()[1]
t = f.solve()[0]
# # plt.plot(f.solve()[0], C[0],'g-')
# # plt.plot(f.solve()[0], C[5],'k-')
# plt.plot(t, C)
# plt.show()
