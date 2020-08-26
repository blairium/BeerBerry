import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os as os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')


def binary_Write(fileName, df):
    df.to_pickle(fileName)


def binary_Write_Post(fileName, df):
    df.to_pickle(fileName)


def csv_Write(fileName, df):
    df.to_csv(fileName, index=False, sep=' ')


def csv_WritePost(fileName, df):
    df.to_csv(fileName, index_label='row')
    # columns=['t', 'i', 'Imag', 'Imagfilt', 'ifilt', 'ienv', 'int_ienv', 'ienv_filtered']


def binary_Read(fileName):
    data = pd.read_pickle(fileName)
    return data


def binary_Read_Post(fileName):
    data = pd.read_pickle(fileName)
    return data


def data_read_Post(fileName):
    data = pd.read_csv(fileName)
    return data


def data_read(fileName):
    data = pd.read_csv(fileName, header=None, delimiter=r"\s+")
    return data


def csv_read(fileName):
    data = pd.read_csv(fileName, header=None)
    data = data.iloc[:, 1:]
    return data


def csv_read_Post(fileName):
    data = pd.read_csv(fileName, header=0)
    data = data.iloc[:, 1:]
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


def readFile(fileName, post):
    ext = os.path.splitext(fileName)[-1].lower()

    if post == 1:

        if ext == ".data":
            data = data_read_Post(fileName)
        elif ext == ".bin":
            data = binary_Read_Post(fileName)
        elif ext == ".csv":
            data = csv_read_Post(fileName)

    else:
        if ext == ".data":
            data = data_read(fileName)
        elif ext == ".bin":
            data = binary_Read(fileName)
        elif ext == ".csv":
            data = csv_read(fileName)

    return data


def writeFile(fileName, data, post):
    ext = os.path.splitext(fileName)[-1].lower()
    ##
    if post == 1:

        if ext == ".data":
            csv_WritePost(fileName, data)
        elif ext == ".bin":
            binary_Write_Post(fileName, data)
        elif ext == ".csv":
            csv_WritePost(fileName, data)

    elif post == 0:
        if ext == ".data":
            csv_Write(fileName, data)
        elif ext == ".bin":
            binary_Write(fileName, data)
        elif ext == ".csv":
            csv_Write(fileName, data)
