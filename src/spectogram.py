import sys
import argparse
import sounddevice as sd
import queue

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import r2fft
from random import *

# Global queue
q = queue.Queue()
data = np.zeros((512,512)).tolist()
im = None

def audio_callback(indata, frames, time, status):
    #print(len(indata))
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)

    #fancy slicing??
    #print(indata[::1, 0])
    q.put(indata[::1, 0])
    #print(q)

def update_spectogram(frame):
    while True:
        if q.qsize() > 16:
            #print(q.qsize())
            a = im.get_array()
            data_seg = []
            for i in range(16):
                data_seg.extend(q.get_nowait())
            fft_data = abs(r2fft.fft(data_seg))[::16]
            #print(len(fft_data))
            #for i in range(512):
            #    a[i] = fft_data
            a = np.append(a[1:],fft_data)
            im.set_array(a)
            im.set_clim(vmax=np.amax(a))
        else:
            break
    return [im]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Description")
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    parser.add_argument(
        '-d', '--device', type=int,
        help='input device (numeric ID or substring)')
    #parser.add_argument(
    #    '-w', '--window', type=float, default=200, metavar='DURATION',
    #    help='visible time slot (default: %(default)s ms)')
    parser.add_argument(
        '-i', '--interval', type=float, default=100,
        help='minimum time between plot updates (default: %(default)s ms)')
    #parser.add_argument(
    #    '-b', '--blocksize', type=int, help='block size (in samples)')
    parser.add_argument(
        '-r', '--samplerate', type=float, help='sampling rate of audio device')
    #parser.add_argument(
    #    '-n', '--downsample', type=int, default=10, metavar='N',
    #    help='display every Nth sample (default: %(default)s)')
    #parser.add_argument(
    #    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    #    help='input channels to plot (default: the first)')
    args = parser.parse_args()

    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']

    print(args)

    stream = sd.InputStream(
        device=args.device, channels=1,
        samplerate=args.samplerate, callback=audio_callback)

    fig = plt.figure()
    im = plt.imshow(data, animated=True, vmin=0, vmax=1)
    ani = animation.FuncAnimation(fig, update_spectogram, interval=args.interval, blit=True)

    with stream:
        print('Recording started...')
        plt.show()
