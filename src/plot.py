#!/usr/local/bin python
# python plot.py data.csv graph.png transform.csv graph2.png
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
import random
import r2fft

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
    xs = np.linspace(0.0, 5.0, num=4096)
    ys = np.sin(7 * 2 * np.pi * xs) + np.sin(30 * 2 * np.pi * xs) + 3*np.sin(15 * 2 * np.pi * xs)
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

def custom_transform(data_file, transform_data_file):
    labels, xs, ys = read_csv(data_file)
    transformed_ys = abs(r2fft.fft(ys))
    write_csv(transform_data_file, ['Frequency', 'Power'], np.linspace(0,len(xs)/((xs[-1]-xs[0])), num=len(transformed_ys)), transformed_ys)

def np_transform(data_file, transform_data_file):
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


        ##print(output)
        generate_random_data(data_file)
        generate_plot(data_file, image_file)
        np_transform(data_file, transform_data_file)
        generate_plot(transform_data_file, transform_image_file, title='Fourier Transformed Data (NP)')
        custom_transform(data_file, transform_data_file)
        generate_plot(transform_data_file, transform_image_file, title='Fourier Transformed Data (Custom)')

        #print(np.fft.fft([1, 2, 3+1j, 1+1j, 2+2j, 5+2j, 6+1j, -1j]))
