#!/usr/local/bin python
# python plot.py data.csv graph.png transform.csv graph2.png
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
import random

def read_csv(data_file):
    axes_labels = []
    xs = []
    ys = []
    with open(data_file, 'r') as f:
        axes_labels = f.readline().split()
        for line in f:
            point = map(float,line.split())
            xs.append(point[0])
            ys.append(point[1])

    return axes_labels, xs, ys

def write_csv(data_file, labels, xs, ys):
    with open(data_file, 'w') as f:
        f.write(labels[0]+'\t'+labels[1]+'\n')
        for i,x in enumerate(xs):
            f.write('%f\t%f\n' % (x,ys[i]))

def generate_random_data(filename):
    xs = np.linspace(0.0, 5.0, num=10000)
    ys = np.sin(7 * 2 * np.pi * xs) + np.sin(23 * 2 * np.pi * xs) + 3*np.sin(15 * 2 * np.pi * xs)
    for i,y in enumerate(ys):
        #pass
        ys[i] = y+random.random()*4-2

    write_csv(filename, ['Time', 'Signal Amplitude'], xs, ys)

def generate_plot(data_file, output_file, title='Signal Data'):
    fig, ax = plt.subplots()
    with open(data_file, 'r') as f:
        axes_labels, xs, ys = read_csv(data_file)

        ax.plot(xs, ys, 'o-', markersize=2)
        ax.set(xlabel=axes_labels[0], ylabel=axes_labels[1], title=title)
        ax.grid()

        fig.savefig(output_file, dpi=200)
        plt.show()

'''def fourier_transform(data_file, transform_data_file, bins=None):
    labels, xs, ys = read_csv(data_file)

    if bins is None:
        bins = len(xs)

    #ks = np.linspace(0,len(xs)/(2*(xs[-1]-xs[0])), num=bins)
    ks = np.linspace(0,len(xs)/((xs[-1]-xs[0])), num=bins)
    transformed_ys = []

    for k in ks:
        sum = 0
        for n,y in enumerate(ys):
            sum += y*complex(np.cos(2*np.pi*k*xs[n]),-np.sin(2*np.pi*k*xs[n]))
        transformed_ys.append(abs(sum)*(xs[1]-xs[0]))

    write_csv(transform_data_file, ['Frequency', 'Power'], ks, transformed_ys)'''

def fourier_transform(data_file, transform_data_file, bins=None):
    labels, xs, ys = read_csv(data_file)

    if bins is None:
        bins = len(xs)

    ks = range(bins)
    transformed_ys = []

    for k in ks:
        sum = 0
        for n,y in enumerate(ys):
            sum += y*complex(np.cos(2*np.pi*k*n/bins),-np.sin(2*np.pi*k*n/bins))
        transformed_ys.append(abs(sum))

    print(transform_data_file)
    write_csv(transform_data_file, ['Frequency', 'Power'], np.linspace(0,len(xs)/((xs[-1]-xs[0])), num=bins), transformed_ys)

def fft(ys, bins):
    if len(ys) == 1:
        return fft_slow(ys, bins)
    else:
        output = []
        if len(bins) % 2 == 0:
            evens = fft(ys[::2], bins/2)
            odds = fft(ys[1::2], bins/2)
            for k in range(bins):
                if k < bins/2:
                    output.append(evens[k]%(bins/2)+)

def fft_slow(ys, bins):
    output = []
    for k in range(bins):
        sum = 0
        for n,y in enumerate(ys):
            sum += y*complex(np.cos(2*np.pi*k*n/bins),-np.sin(2*np.pi*k*n/bins))
        output.append(sum)

    return output

def nptransform(data_file, transform_data_file):
    labels, xs, ys = read_csv(data_file)
    transformed_ys = abs(np.fft.fft(ys))
    write_csv(transform_data_file, ['Frequency', 'Power'], np.linspace(0,len(xs)/((xs[-1]-xs[0])), num=len(transformed_ys)), transformed_ys)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('python plot.py <data_file> <image_file> <transform_date_file> <transform_image_file>')
    else:
        data_file = sys.argv[1]
        image_file = sys.argv[2]
        transform_data_file = sys.argv[3]
        transform_image_file = sys.argv[4]

        #generate_random_data(data_file)
        #generate_plot(data_file, image_file)
        #nptransform(data_file, transform_data_file)
        #generate_plot(transform_data_file, transform_image_file, title='Fourier Transformed Data (NP)')
        #fourier_transform(data_file, transform_data_file, 100)
        #generate_plot(transform_data_file, transform_image_file, title='Fourier Transformed Data (Program)')
        print(fft_slow([1, 2-1j, -1j, -1+2j], 4))
