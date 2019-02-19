import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import r2fft

duration = 10  # seconds
fs = 44100

myrecording = sd.rec(duration * fs, samplerate=fs, channels=1)

sd.wait()
print(len(myrecording))
print(myrecording)

new_copy = np.array([myrecording[i][0] for i in range(len(myrecording))])
print(new_copy)

testSpec = []
for i in range(2*42*duration-1):
    testSpec.append( np.log(abs(r2fft.fft(new_copy[i*525:525*i+1050]))) )

#plt.plot(abs(r2fft.fft(myrecording)))
plt.imshow(np.array(testSpec), extent=[0,2*fs,0,2*42*duration-1], aspect=44100/2048.0)
plt.show()
