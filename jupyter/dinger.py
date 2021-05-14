import tty
import sys
import termios
import time
import pandas as pd
import numpy as np

ESC = chr(27)


class NodeData:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.data = []

    def add_sample(self, delta):
        self.data.append(delta)

class Distribution:
    def __init__(self):
        self.data = {}


    def add_sample(self, source, destination, delta):
        if source not in self.data.keys():
            self.data[source] = {}
        if destination not in self.data[source].keys():
            self.data[source][destination] = NodeData(source, destination)
        self.data[source][destination].add_sample(delta)

    def store_sample(self, file_name):
        for source in self.data.keys():
            for destination in self.data.keys():
                print(source+';'+destination+';'.join([str(delta) for delta in self.data[source][destination]])+'\n')
        # create strings
        strings = []
        labels = np.sort(self.data.keys())
        for source in labels:
            for destination in labels:
                strings.append(source+';'+destination+';'.join([str(delta) for delta in self.data[source][destination]])+'\n')
        with open(file_name, "w") as file:
            file.writelines(strings)
    def print_sample(self):
        labels = np.sort(self.data.keys())
        for source in labels:
            for destination in labels:
                print(source+';'+destination+';'.join([str(delta) for delta in self.data[source][destination]])+'\n')



def fit(file_name):
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    key_old = None
    key_new = None
    distribution = Distribution()

    # Start sampling
    print('Press esc to end sampling!')
    try:
        while key_old != ESC:
            start = time.time()
            key_new=sys.stdin.read(1)[0]
            end = time.time()
            distribution.add_sample(key_old, key_new, end-start)
            key_old = key_new
        print('ESC pressed')
        distribution.print_sample
    except KeyboardInterrupt:
        print('Ctrl + C pressed')
    finally:
        distribution.store_sample(file_name)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)