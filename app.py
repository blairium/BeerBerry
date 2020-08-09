import PySimpleGUI as gui
import pandas as pd
import matplotlib.pyplot as plt


layout = [[gui.Text('Document to open')],
          [gui.In(), gui.FileBrowse()],
          [ gui.Button('plot'), gui.Cancel()]]

window = gui.Window('Window that stays open', layout)

def draw_plot(volts, amps):
    plt.plot(volts, amps)
    plt.show(block=False)

while True:
    event, values = window.read()

    fname = values[0]
    data = pd.read_csv(fname, header=None, delimiter=r"\s+")
    volts = data.iloc[:,0].to_numpy()
    amps = data.iloc[:,1].to_numpy()



    if event == gui.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'plot':
        draw_plot(volts, amps)

window.close()
