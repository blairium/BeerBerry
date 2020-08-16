
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os as os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

def binary_Write(fileName, df):
    df.to_pickle(fileName)

def csv_Write(fileName, df):
    df.to_csv(fileName)

def binary_Read(fileName):
    data = pd.read_pickle(fileName)
    return data

def data_read(fileName):
    data = pd.read_csv(fileName, header=None, delimiter=r"\s+")
    return data

def csv_read(fileName):
    data = pd.read_csv(fileName, header=None)
    data = data.iloc[:,1:]
    return data

def draw_plot(time, amps):
    plt.plot(time, amps)
    plt.show(block=False)

def get_time_values(volts):
    sample_rate = 8000.0
    dt = 1 / sample_rate
    nod = len(volts) + 1
    n = np.arange(1, nod)
    t = n * dt
    return t

def draw_plot(time, amps):
    plt.plot(time, amps)
    plt.show(block=False)

def readFile(fileName):

    ext = os.path.splitext(fileName)[-1].lower()
    if ext == ".data":
        data = data_read(fileName)
    elif ext == ".bin":
            data = binary_Read(fileName)
    elif ext == ".csv":
            data = csv_read(fileName)

    return data

def writeFile(fileName, data):
    ext = os.path.splitext(fileName)[-1].lower()
    if ext == ".data":
        csv_Write(fileName, data)
    elif ext == ".bin":
        binary_Write(fileName, data)
    elif ext == ".csv":
        csv_Write(fileName, data)











