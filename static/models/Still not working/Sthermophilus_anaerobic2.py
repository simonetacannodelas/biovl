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
    def __init__(self):
        #Biological model
        self.mu_max = 2.06 #h^-1
        self.tlag= 0.8#h
        self.Ks= 0.79 #g/L
        self.Ki= 164 #g/L
        self.Kp_la= 0.24 #g/L
        self.K_la= 19.8 #g/L
        self.Kp_pH1= 20 #g/L
        self.Kp_pH2= 7 #g/L
        self.pHopt= 6.39
        self.pHmax=7
        self.pHmin=5.9
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
        self.pKz = 9.4
        self.T = 313.16
        self.pKc1=3404.7/(self.T-14.8435+0.03279*self.T)
        self.pKla=3.86
        self.pKNH=2835.8/(self.T-0.6322+0.00123*self.T)
        self.pKp1=799.3/(self.T-4.5535+0.01349*self.T)
        self.pKp2=1979.5/(self.T-5.3541+0.01984*self.T)

        # Initial concentrations
        self.S0= 65 #g/L
        self.Gal0 = 0.0001  # g/L
        self.X0 = 0.25 #g/L
        self.LA0 = 0.1 #g/L
        self.La0 = 0.0 #g/L
        self.NH30 = 0.005 #g/L
        self.NH40 = 0.005 #g/L
        self.PH20 = 2
        self.PH0 = 0
        self.P0 = 0
        self.C10=2e-05
        self.C20=0
        self.H0= 1e-07
        self.OH0=1e-07
        self.Z0 =  2#mol/L
        self.IZ0 = 0
        self.PHo = 7


        self.t_end = 10
        self.t_start = 0.000000001
        self.steps = (self.t_end - self.t_start) * 24
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
       #
        if C[16] < self.pHmin or C[16] > self.pHmax:
            k = 0
        else:
            D = (C[16] - self.pHmax) * (C[16] - self.pHmin) ** 2
            E = (self.pHopt - self.pHmin) * ((self.pHopt - self.pHmin) * (C[16] - self.pHopt) - (self.pHopt - self.pHmax) * (
                        self.pHopt + self.pHmin - 2 * C[16]))
            k = D / E

        # initialize the rate vector
        #biomass growth
        growth = k * self.mu_max*(C[0]/(C[0]+self.Ks))*(self.Ki/(C[3]+self.Ki))*C[2]
        #lactic synthesis
        lactic_synt = k * self.alphagrowth * self.mu_max*(C[0]/(C[0]+self.Ks))*(self.Ki/(C[3]+self.Ki))*math.exp((-1)*(6.42-10**C[12])**2/1)*C[2]
        # Ammonia dissociation
        ammoniadiss = (self.KNHeq * self.KrNH) * C[6] - self.KrNH * C[5] * C[12]
        # Phosphate dissociate 1
        phosphdiss1 = (self.KP1eq * self.KrP1) * C[7] - self.KrP1 * C[9] * C[12]
        # Phosphate dissociate 2
        phosphdiss2 = (self.KP2eq * self.KrP2) * C[8] - self.KrP2 * C[9] * C[12]
        # Carbonate dissociation 1
        carbdiss1 = (self.KC1eq * self.KrC1) * C[10] - self.KrC1 * C[11] * C[12]
        # Lactate dissociation
        lactdiss = (self.KLaeq * self.KrLA) * C[3] - self.KrLA * C[4]
        # Water dissociation
        wdiss = 1 - self.KrW * C[12] * C[13]
        # Dissociation of unknown compound
        zdiss = (self.KZeq * self.KrZ) * C[14] - self.KrZ * C[15] * C[12]
        r = np.zeros((17,1))

        r[0,0] = -(1 + self.Y_gal)*growth -(1 + self.Y_gal)*lactic_synt
        r[1,0] = (self.Y_gal)*growth + (self.Y_gal)*lactic_synt
        r[2,0] = growth
        r[3,0] = -1 * lactdiss
        r[4,0] = 1 / 3 * lactic_synt + lactdiss
        r[5,0] = -0.22 * growth + ammoniadiss
        r[6,0] = -1 * ammoniadiss
        r[7,0] = 0.02 * growth - phosphdiss1
        r[8,0] = phosphdiss1 - phosphdiss2
        r[9,0] = phosphdiss2
        r[10,0] = -carbdiss1
        r[11,0] = carbdiss1
        r[12,0] = 1/3 * lactic_synt + ammoniadiss + phosphdiss1 + phosphdiss2 + carbdiss1 + lactdiss + wdiss + zdiss
        r[13,0] = wdiss
        r[14,0] = -1 * zdiss
        r[15,0] = zdiss
        r[16,0] = -1*math.log(C[12])

        dSdt = r[0,0]
        dGaldt = r[1,0]
        dXdt = r[2,0]
        dLAdt = r[3,0]
        dLadt = r[4,0]
        dAdt = r[5,0]
        dA1dt = r[6,0]
        dPdt = r[7,0]
        dP1dt = r[8,0]
        dP2dt = r[9,0]
        dC1dt = r[10,0]
        dC2dt = r[11,0]
        dHdt = r[12,0]
        dOHdt = r[13,0]
        duZdt = r[14,0]
        dZdt = r[15,0]
        dPHdt = r[16,0]


        return [dSdt, dGaldt, dXdt, dLAdt, dLadt, dAdt, dA1dt, dPdt, dP1dt, dP2dt, dC1dt, dC2dt, dHdt, dOHdt, duZdt, dZdt, dPHdt]

    def solve(self):
        t = np.linspace(self.t_start, self.t_end, self.steps)
        C = np.ones([len(t), 16])
        C0 = ([self.S0, self.Gal0, self.X0, self.LA0, self.La0, self.NH30, self.NH40, self.PH20, self.PH0, self.P0, self.C10, self.C20, self.H0, self.OH0, self.Z0, self.IZ0, self.PHo])
        self.ctrl_output = np.zeros(len(t))  # controller output
        e = np.zeros(len(t))  # error
        ie = np.zeros(len(t))  # integral of the error
        dpv = np.zeros(len(t))  # derivative of the pv
        P = np.zeros(len(t))  # proportional
        I = np.zeros(len(t))  # integral
        D = np.zeros(len(t))  # derivative

        for i in range(len(t) - 1):
             # print(t[i])
             # PID control of cooling water
             dt = t[i + 1] - t[i]
             # Error
             e[i] = C[i, 12] - self.pHopt
             # print(e[i])
             if i >= 1:
                 dpv[i] = (C[i, 12] - C[i - 1, 12]) / dt
                 ie[i] = ie[i - 1] + e[i] * dt
             P[i] = self.K_p * e[i]
             I[i] = self.K_i * ie[i]
             D[i] = self.K_d * dpv[i]

             self.ctrl_output[i] = P[i] + I[i] + D[i]
             u = self.ctrl_output[i]
             if u > self.u_max:
                 u = self.u_max
                 ie[i] = ie[i] - e[i] * dt  # anti-reset windup
             if u < self.u_min:
                 u = self.u_min
                 ie[i] = ie[i] - e[i] * dt  # anti-reset windup
             # time for solving ODE
             ts = [t[i], t[i + 1]]
        C = odeint(self.rxn, C0, t, rtol=1e-7, mxstep=500000)
        return (t, C)

#
f = Sthermophilus_anae()
C = f.solve()[1]
t = f.solve()[0]

#
plt.plot(t, C[:,0], label = 'Lactose')
plt.plot(t, C[:,1], label = 'Galactose')
plt.plot(t, C[:,2], label = 'Biomass')
plt.plot(t, C[:,3], label = 'Lactic Acid')
plt.plot(t, C[:,16], label = 'pH')
plt.legend()
plt.xlabel('Time(h)')
plt.ylabel('Concentration (g/L)')
plt.axis([0, 10, 0, 67])
plt.savefig("model_sthermophilus.png")
plt.show()
