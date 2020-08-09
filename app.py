import PySimpleGUI as gui
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Helper
import os as os

layout = [[gui.Text('Document to open')],
          [gui.In(), gui.FileBrowse()],
          [gui.Button('plot'), gui.Button('save'), gui.Cancel()]]

window = gui.Window('Window that stays open', layout)

while True:
    event, values = window.read()

    fname = values[0]
    ext = os.path.splitext(fname)[-1].lower()
    if ext == ".data":
        data = Helper.data_read(fname)
    elif ext == ".bin":
        data = Helper.binary_Read(fname)
    elif ext == ".csv":
        data = Helper.csv_read(fname)


    volts = data.iloc[:, 0].to_numpy()
    amps = data.iloc[:, 1].to_numpy()
    time = Helper.get_time_values(volts)

    if event == gui.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'plot':
        Helper.draw_plot(time, amps)
    elif event == 'save':
        Helper.csv_Write(data)

window.close()
