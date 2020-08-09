
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def binary_Write(df):
    df.to_pickle("myfile.bin")

def csv_Write(df):
    df.to_csv("myfile.csv")

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


