import PySimpleGUI as gui
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import NateFunc as nFunc


layout = [[gui.Text('Document to open')],
          [gui.In(), gui.FileBrowse()],
          [ gui.Button('plot'), gui.Button('save'), gui.Cancel()]]

window = gui.Window('Window that stays open', layout)

def draw_plot(volts, amps):
    plt.plot(volts, amps)
    plt.show(block=False)

def get_time_values(volts):
    sample_rate = 8000.0
    dt = 1/sample_rate
    nod = len(amps)+1
    n = np.arange(1, nod)
    t = n*dt
    return t

def save_bin(df):
    df.to_pickle("myfile.bin")

while True:
    event, values = window.read()

    fname = values[0]
    data = pd.read_csv(fname, header=None, delimiter=r"\s+")
    #data = pd.read_pickle(fname)
    volts = data.iloc[:,0].to_numpy()
    amps = data.iloc[:,1].to_numpy()
    time = get_time_values(volts)
    
    

    if event == gui.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'plot':
        draw_plot(time, amps)
    elif event == 'save':
        save_bin(data)

window.close()