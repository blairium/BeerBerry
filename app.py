import PySimpleGUI as gui
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Helper
import os as os
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

def destroy_figure(fig_canvas_agg):
        fig_canvas_agg.get_tk_widget().forget()
        plt.close('all')

#ab1 = [[gui.Canvas(size = (700,500), key='-CANVAS-')],
#       [gui.Button('baseline')]]
#tab2 = [[gui.Canvas(size = (700,500), key='-CANVAS2-')]]
#tab3 = [[gui.Canvas(size = (700,500), key='-CANVAS3-')]]



layout = [[gui.In(), gui.FileBrowse()],
          #[gui.TabGroup([[gui.Tab('tab 1', tab1), gui.Tab('tab 2', tab2), gui.Tab('tab 3', tab3)]])],
          [gui.Canvas(size = (700,500), key='-CANVAS-')],
          [gui.Button('plot'), gui.Button('plot2'), gui.Button('plot3'), gui.Button('baseline'), gui.Button('save'), gui.Button('calculate')]]        

window = gui.Window('BeerBerry', layout, element_justification='center', font='Helvetica 18')

t,i,f,Imag,Imagfilt,ifilt,ienv,int_ienv,ienv = ([] for i in range(9))
fig_canvas_agg = None

while True:
    event, values = window.read()
    fig_exists = False
    fname = values[0]
    ext = os.path.splitext(fname)[-1].lower()
    if ext == ".data":
        data = Helper.data_read(fname)
    elif ext == ".bin":
        data = Helper.binary_Read(fname)
    elif ext == ".csv":
        data = Helper.csv_read(fname)

    if event == gui.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'plot':
        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg)
        fig = matplotlib.figure.Figure(figsize=(10, 5), dpi=100)
        fig.add_subplot(111).plot(t, ienv)

        fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
        fig_exists = True

    elif event == 'plot2':
        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg)

        fig = matplotlib.figure.Figure(figsize=(10, 5), dpi=100)
        fig.add_subplot(111).plot(t, i)

        fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
        fig_exists = True

    elif event == 'plot3':
        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg)

        fig = matplotlib.figure.Figure(figsize=(10, 5), dpi=100)
        fig.add_subplot(221).plot(f, Imag)
        fig.add_subplot(223).plot(t, ifilt)
        fig.add_subplot(222).plot(f, Imagfilt)
        fig.add_subplot(224).plot(t, int_ienv)

        fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
        fig_exists = True

    elif event == 'save':
        Helper.csv_Write(data)
    elif event == 'calculate':
        t,i,f,Imag,Imagfilt,ifilt,ienv,int_ienv,ienv = major_function(60,10,10,2,1.5,0.2,8000.0,data)
    elif event == 'baseline':
        clickEvent = fig_canvas_agg.mpl_connect('button_press_event', onclick)


window.close()
