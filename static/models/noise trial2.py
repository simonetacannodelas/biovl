from static.models.Rx_Fermentation_Scerevisiae_Glucose_Aerobic_Cstr import SCerevisiae_Cstr
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

#define model
modelInUse= SCerevisiae_Cstr()
modelInUse.solve()
t = modelInUse.solve()[0]
C= modelInUse.solve()[1]

S = C[:, 0]
A = C[:, 1]
B = C[:, 3]
PV =[]
PV2 = []
PV3 = []
C_noise =  np.zeros((C.shape))
import numpy as np
for i in range(len(t)):
    PV.append((((math.sin(t[i]*83))/47)+(math.cos(t[i]*11))/23))
    PV2.append(0.6*(((math.sin(t[i] * 61)/31) + (math.cos(t[i] * 43)) / 61)))
    PV3.append(0.33*(((math.sin(t[i] * 41))/19) + (math.cos(t[i] * 61)) / 89))
for i in range(len(C[0])):
    C_noise [:, i] = C[:, i] + C[:, i]* PV + C[:, i]*PV2 + C[:, i]*PV3

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
