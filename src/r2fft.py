import numpy as np
import ctypes

cfft = ctypes.CDLL('fft.so')

class c_Complex(ctypes.Structure):
    _fields_ = [("real", ctypes.c_double),("imaginary", ctypes.c_double)]

def dft(ys, bins=None):
    if bins is None:
        bins = len(ys)

    output = []
    for k in range(bins):
        sum = 0
        for n,y in enumerate(ys):
            sum += y*complex(np.cos(2*np.pi*k*n/bins),-np.sin(2*np.pi*k*n/bins))
        output.append(sum)

    return output

# Pads the input so it is a power of 2
def fft(ys):
    #pads with 0s
    upper = 1
    count = 0
    while upper < len(ys):
        count+=1
        upper*=2
    new_length = pow(2, count)

    # construct arrays for c function
    input = (c_Complex * new_length)()
    for i,y in enumerate(ys):
        input[i].real = y.real
        input[i].imaginary = y.imag
    for i in range(len(ys),new_length):
        input[i].real = 0
        input[i].imaginary = 0
    output = (c_Complex * new_length)()

    # Execute c function
    cfft.fft(input, new_length, output)

    #for row in output:
    python_output = []
    for i,row in enumerate(output):
        python_output.append(complex(row.real, row.imaginary))

    return np.array(python_output)
