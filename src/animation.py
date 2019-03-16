import sys
import argparse
import sounddevice as sd
import queue

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import r2fft
from random import *

im = None

def update_spectogram(frame):
    a = im.get_array()
    for i in range(40):
        for j in range(40):
            a[i][j] = randint(1,100)
    im.set_array(a)
    return [im]


if __name__ == '__main__':
    fig = plt.figure()
    base_data = np.zeros((40,40))
    im = plt.imshow(base_data, animated=True, vmin=0, vmax=100)
    ani = animation.FuncAnimation(fig, update_spectogram, interval=30, blit=True)

    plt.show()
