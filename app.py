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

def destroy_figure(fig_canvas_agg):
        fig_canvas_agg.get_tk_widget().forget()
        plt.close('all')

#ab1 = [[gui.Canvas(size = (700,500), key='-CANVAS-')],
#       [gui.Button('baseline')]]
#tab2 = [[gui.Canvas(size = (700,500), key='-CANVAS2-')]]
#tab3 = [[gui.Canvas(size = (700,500), key='-CANVAS3-')]]



layout = [[gui.In(), gui.FileBrowse(), gui.Button('Log in')],
          [gui.Canvas(size = (700,500), key='-CANVAS-')],
          [gui.Button('plot', disabled=True,), gui.Button('plot2', disabled=True,), gui.Button('plot3', disabled=True,), gui.Button('baseline', disabled=True,),
           gui.FileSaveAs(button_text='save', disabled=True, target='save', enable_events=True, key='save', file_types=(('DATA', '.data'), ('BIN', '.bin'), ('CSV', '.csv'), ('All Files', '*.*'))),
           gui.Button('calculate'), gui.Button('Exit')]]

window = gui.Window('BeerBerry', layout, element_justification='center', font='ComicSans 18')

t,i,f,Imag,Imagfilt,ifilt,ienv,int_ienv,ienv_filtered = ([] for i in range(9))
fig_canvas_agg = None
df = None
while True:
    event, values = window.read()
    fname = values[0]

    data = Helper.readFile(fname)

    print(event)
    if event == gui.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'plot':
        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg)

        window.find_element('baseline').Update(disabled=False)

        fig = matplotlib.figure.Figure(figsize=(10, 5), dpi=100)
        fig.add_subplot(111).plot(t, ienv)

        fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'plot2':
        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg)

        window.find_element('baseline').Update(disabled=True)

        fig = matplotlib.figure.Figure(figsize=(10, 5), dpi=100)
        fig.add_subplot(111).plot(t, i)

        fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'plot3':
        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg)

        window.find_element('baseline').Update(disabled=True)

        fig = matplotlib.figure.Figure(figsize=(10, 5), dpi=100)
        fig.add_subplot(221).plot(f, Imag)
        fig.add_subplot(223).plot(t, ifilt)
        fig.add_subplot(222).plot(f, Imagfilt)
        fig.add_subplot(224).plot(t, int_ienv)

        fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    elif event == 'calculate':
        t,i,f,Imag,Imagfilt,ifilt,ienv,int_ienv,ienv_filtered = major_function(60,10,10,2,1.5,0.2,8000.0,data)

        window.find_element('plot').Update(disabled=False)
        window.find_element('plot2').Update(disabled=False)
        window.find_element('plot3').Update(disabled=False)




        d = {
            't':t,
            'i':i,
            'f':f,
            'Imag':Imag,
            'Imagfilt':Imagfilt,
            'ifilt':ifilt,
            'ienv':ienv,
            'int_ienv':int_ienv,
            'ienv_filtered':ienv_filtered
            }
        df = pd.DataFrame(d)
        print(type(df))
        if df is not None:
            window.find_element('save').Update(disabled=False)

    elif event == 'save':

        outFile = values['save']
        Helper.writeFile(outFile, df)



    elif event == 'baseline':
        if (len(xdata) >= 2):
            xdata = []
            ydata = []
        clickEvent = fig_canvas_agg.mpl_connect('button_press_event', onclick)

    elif event == 'Log In':


window.close()
