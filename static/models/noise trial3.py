from static.models.Rx_Fermentation_Ecoli_Glucose_Aerobic_Batch import Ecoli_Aero
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

#define model
modelInUse= Ecoli_Aero()
modelInUse.solve()
t = modelInUse.solve()[0]
C= modelInUse.solve()[1]

S = C[:, 0]
A = C[:, 1]
B = C[:, 3]
C_noise1 =  np.zeros((C.shape))
C_noise2=  np.zeros((C.shape))
C_noise3=  np.zeros((C.shape))
C_noise=  np.zeros((C.shape))
import numpy as np
for i in range(len(t)):
    for k in range(len(C[0])):
        # C_noise1[:, k] = C[:, k] - (C[:, k] * (((math.sin(t[i]*33))/11)+(math.cos(t[i]*12))/81)) -(C[:, k] * (((0.66*(((math.sin(t[i] * 25))/9) + (math.cos(t[i] * 23)) / 73)))) +(C[:, k] * (((((math.sin(t[i] * 11)) /3) + (math.cos(t[i] * 61)) / 43)))))
        # C_noise2[:, k] =C[:, k] -(C[:, k] * (((0.66*(((math.sin(t[i] * 25))/9) + (math.cos(t[i] * 23)) / 73)))))
        # C_noise3[:, k] = C[:, k] -(C[:, k] * (((((math.sin(t[i] * 11)) /3) + (math.cos(t[i] * 61)) / 43))))
        # C_noise [:,k] = C_noise1[:, k]
        C_noise[:,k] = C[:, k] + C[:, k]*((math.sin(t[i]*22))/1)+ C[:, k]*((math.cos(t[i]*37))/33)
       # C_noise[:, k] = C[:, k] + C[:, k]*(((((math.sin(t[i]* 34))) + (math.cos(t[i]* 12)))+0.66*(((((math.sin(t[i]*23)) + (math.cos(t[i]* 87)))))-0.33*((((math.sin(t[i]* 43)) ) + (math.cos(t[i]* 61)))))))


#        C_noise [:, k] = C[:, k]*(math.exp((10**-17)*t[i])+math.exp(-(10**-17)*t[i]))
# ((math.sin(t[i]*33))/11)+(math.cos(t[i]*12))/81))
# PV2.append(0.6*(((math.sin(t[i] * 25))/9) + (math.cos(t[i] * 23)) / 73))
# PV3.append(0.33*(((math.sin(t[i] * 11)) /3) + (math.cos(t[i] * 61)) / 43)

plt.plot(t,C_noise[:,0])
plt.plot(t,C[:,0])

plt.plot(t,C_noise[:,0])
plt.plot(t,C[:,0])
plt.plot(t,C_noise[:,1])
plt.plot(t,C[:,1])
plt.plot(t,C_noise[:,3])
plt.plot(t,C[:,3])
plt.xlabel('Time (h)')
plt.ylabel('Concentration (g/L)')
#
# # plt.plot(t, C[:,0])
# # # plt.plot(t, C[:,1])
# # # # plt.plot(f.solve()[0], f.solve()[1][:,2])
# # # plt.plot(t, C[:,3])
# # # plt.plot(t,C[:,0])
# # plt.plot(t, PV[:,0])
# # # plt.plot(t,C[:,1])
# # # plt.plot(t, PV[:,1])
# # # plt.plot(t,C[:,3])
# # # plt.plot(t, PV[:,3])
plt.show()

