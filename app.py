import PySimpleGUI as gui
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Helper
import os as os
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from data.And_AC_Volt_Python import major_function
matplotlib.use('TkAgg')

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


layout = [[gui.Text('Document to open')],
          [gui.In(), gui.FileBrowse()],
          [gui.Canvas(key='-CANVAS-')],
          [gui.Button('plot'), gui.Button('save'), gui.Button('calculate'), gui.Cancel()]]

window = gui.Window('BeerBerry', layout, element_justification='center', font='Helvetica 18')

t,i,f,Imag,Imagfilt,ifilt,ienv,int_ienv,ienv = ([] for i in range(9))

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

    if event == gui.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'plot':
        fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(111).plot(t, ienv)
        fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    elif event == 'save':
        Helper.csv_Write(data)
    elif event == 'calculate':
        t,i,f,Imag,Imagfilt,ifilt,ienv,int_ienv,ienv = major_function(60,10,10,2,1.5,0.2,8000.0,data)

window.close()
