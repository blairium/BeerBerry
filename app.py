import PySimpleGUI as gui
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Helper
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from data.And_AC_Volt_Python import major_function
from matplotlib.widgets import PolygonSelector
from matplotlib.axes import Axes
matplotlib.use('TkAgg')



xdata = []
ydata = []
def onclick(event):
    #print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
     #     ('double' if event.dblclick else 'single', event.button,
      #     event.x, event.y, event.xdata, event.ydata))
    if (len(xdata) < 2):
        xdata.append(event.xdata)
        ydata.append(event.ydata)
        print(xdata)
        print(ydata)

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    #toolbar = NavigationToolbar2Tk(figure_canvas_agg, canvas)
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

tab1 = [[gui.Canvas(size = (700,500), key='-CANVAS-')],
        [gui.Button('baseline')]]
tab2 = [[gui.Canvas(size = (700,500), key='-CANVAS2-')]]
tab3 = [[gui.Canvas(size = (700,500), key='-CANVAS3-')]]



layout = [[gui.In(), gui.FileBrowse()],
          [gui.TabGroup([[gui.Tab('tab 1', tab1), gui.Tab('tab 2', tab2), gui.Tab('tab 3', tab3)]])],
          [gui.Button('plot'),
           gui.FileSaveAs(button_text='save', disabled=True, target='save', enable_events=True, key='save', file_types=(('All Files', '*.*'), ('DATA', '.data'), ('CSV', '.csv'), ('BIN', '.bin') )), gui.Button('calculate')]]

window = gui.Window('BeerBerry', layout, element_justification='center', font='Helvetica 18')

t,i,f,Imag,Imagfilt,ifilt,ienv,int_ienv,ienv = ([] for i in range(9))

while True:
    event, values = window.read()
    fig_exists = False
    fname = values[0]

    data = Helper.readFile(fname)




    print(event)
    if event == gui.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'plot':
        if data is not None:
            window.find_element('save').Update(disabled=False)

        fig = matplotlib.figure.Figure(figsize=(10, 5), dpi=100)
        fig.add_subplot(111).plot(t, ienv)

        fig2 = matplotlib.figure.Figure(figsize=(10, 5), dpi=100)
        fig2.add_subplot(111).plot(t, i)

        fig3 = matplotlib.figure.Figure(figsize=(10, 5), dpi=100)
        fig3.add_subplot(221).plot(f, Imag)
        fig3.add_subplot(223).plot(t, ifilt)
        fig3.add_subplot(222).plot(f, Imagfilt)
        fig3.add_subplot(224).plot(t, int_ienv)

        fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

        fig_canvas_agg = draw_figure(window['-CANVAS2-'].TKCanvas, fig2)

        fig_canvas_agg = draw_figure(window['-CANVAS3-'].TKCanvas, fig3)
        fig_exists = True
    elif event == 'save':

        outFile = values['save']
        Helper.writeFile(outFile, data)


    elif event == 'calculate':
        t,i,f,Imag,Imagfilt,ifilt,ienv,int_ienv,ienv = major_function(60,10,10,2,1.5,0.2,8000.0,data)
    elif event == 'baseline':
        clickEvent = fig_canvas_agg.mpl_connect('button_press_event', onclick)

window.close()
