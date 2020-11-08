import os
import matplotlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg

"""
This file contains all of the file i/o related functions for the app.

Last Updated: 04/10/2020
Author: Nathan Gillbanks
Contributors: Michael Graps
"""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# use tkinter
matplotlib.use('TkAgg')

# Binary file IO pre/post calculation values


def binary_Write(fileName, df):
    df.to_pickle(fileName)


def binary_Write_Post(fileName, df):
    df.to_pickle(fileName)


def binary_Read(fileName):
    data = pd.read_pickle(fileName)
    return data


def binary_Read_Post(fileName):
    data = pd.read_pickle(fileName)
    return data

# CSV file IO pre/post calculation values+


def csv_Write(fileName, df):
    df.to_csv(fileName, index=False, header=True, sep=',')


def csv_WritePost(fileName, df):
    df.to_csv(fileName, index=False, header=True, sep=',')


def csv_read(fileName):
    data = pd.read_csv(fileName, header=0, delimiter=',')
    return data


def csv_read_Post(fileName):
    data = pd.read_csv(fileName, header=0, delimiter=',')
    return data

# data file IO pre/post calculation values


def data_Write(fileName, df):
    df.to_csv(fileName, index=False, header=True, sep='\t')


def data_WritePost(fileName, df):
    df.to_csv(fileName, index=False, header=True, sep='\t')
    # columns=['t', 'i', 'Imag', 'Imagfilt', 'ifilt', 'ienv', 'int_ienv', 'ienv_filtered']


def data_read_Post(fileName):
    data = pd.read_csv(fileName, header=0, delimiter=r"\s+")
    return data


def data_read(fileName):
    data = pd.read_csv(fileName, header=0, delimiter=r"\s+")
    return data

# High-level function to determine which input to call


def readFile(fileName, post):
    ext = os.path.splitext(fileName)[-1].lower()

    if post == 1:
        if ext == ".data":
            data = data_read_Post(fileName)
        elif ext == ".bin":
            data = binary_Read_Post(fileName)
        elif ext == ".csv":
            data = csv_read_Post(fileName)

    elif post == 0:
        if ext == ".data":
            data = data_read(fileName)
        elif ext == ".bin":
            data = binary_Read(fileName)
        elif ext == ".csv":
            data = csv_read(fileName)

    return data

# High level function to determmine which output to call


def writeFile(fileName, data, post):
    ext = os.path.splitext(fileName)[-1].lower()

    if post == 1:
        if ext == ".data":
            data_WritePost(fileName, data)
        elif ext == ".bin":
            binary_Write_Post(fileName, data)
        elif ext == ".csv":
            csv_WritePost(fileName, data)
        #else:
            #sg.popup_error(
               # 'Error: Invalid File Extension (Valid extensions are: .data, .csv, .bin)')

    elif post == 0:
        if ext == ".data":
            data_Write(fileName, data)
        elif ext == ".bin":
            binary_Write(fileName, data)
        elif ext == ".csv":
            csv_Write(fileName, data)
        #else:
            #sg.popup_error(
               # 'Error: Invalid File Extension (Valid extensions are: .data, .csv, .bin)')
