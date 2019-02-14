import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

duration = 1  # seconds
fs = 44100

myrecording = sd.rec(duration * fs, samplerate=fs, channels=1)

print(len(myrecording))
for i,x in enumerate(myrecording):
    print(myrecording[-1])
sd.wait()


print(myrecording)
plt.plot(myrecording)
plt.show()
