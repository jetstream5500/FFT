import numpy as np
import ctypes

cfft = ctypes.CDLL('fft.so')

class c_Complex(ctypes.Structure):
    _fields_ = [("real", ctypes.c_double),("imaginary", ctypes.c_double)]

def fft2(a):
    for i, row in enumerate(a):
        new_row = fft(row)
        for j,e in enumerate(new_row):
            a[i][j] = e

    a = a.transpose()

    for i, row in enumerate(a):
        new_row = fft(row)
        for j,e in enumerate(new_row):
            a[i][j] = e

    a = a.transpose()

def dft(ys):
    input = (c_Complex * len(ys))()
    for i,y in enumerate(ys):
        input[i].real = y.real
        input[i].imaginary = y.imag

    cfft.dft(input, len(ys))

    python_output = []
    for i,row in enumerate(input):
        python_output.append(complex(row.real, row.imaginary))

    return np.array(python_output)

# Pads the input so it is a power of 2
def fft(ys, min_size=None):
    size = len(ys)
    if min_size is not None:
        size = min_size

    #pads with 0s
    upper = 1
    count = 0
    while upper < size:
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

    # Execute c function
    cfft.fft(input, new_length)

    #for row in output:
    python_output = []
    for i,row in enumerate(input):
        python_output.append(complex(row.real, row.imaginary))

    return np.array(python_output)
