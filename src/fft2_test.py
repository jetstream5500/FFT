import numpy as np
import matplotlib.pyplot as plt
import r2fft

if __name__ == '__main__':
    a = np.zeros((256, 256), dtype=np.complex)
    for i in range(128-2, 128+2):
        for j in range(128-2, 128+2):
            a[i][j] = 20

    r2fft.fft2(a)
    #plt.imshow(abs(a))
    plt.imshow(abs(a))
    plt.show()
