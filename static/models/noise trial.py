from static.models.Rx_Fermentation_Ecoli_Glucose_Aerobic_Batch import Ecoli_Aero
import keras
import matplotlib.pyplot as plt

#define model
model = Ecoli_Aero()
modelNoise = model.add(GaussianNoise(0.01, input_shape=(2,)))

plt.plot(model)
plt.plot(modelNoise)
