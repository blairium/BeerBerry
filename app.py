import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Helper
import matplotlib
from json import (load as jsonload, dump as jsondump)
from os import path
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from data.And_AC_Volt_Python import major_function
from matplotlib.widgets import PolygonSelector
from matplotlib.axes import Axes
from asyncio import events
import asyncio

matplotlib.use('TkAgg')

sg.LOOK_AND_FEEL_TABLE['BeerBerry'] = {'BACKGROUND': '#FFFFFF',
                                       'TEXT': '#000000',
                                       'INPUT': '#C4C4C4',
                                       'TEXT_INPUT': '#000000',
                                       'SCROLL': '#c7e78b',
                                       'BUTTON': ('white', '#40BAD2'),
                                       'PROGRESS': ('#01826B', '#D0D0D0'),
                                       'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
                                       }
PASSWORD = '1245'
PARAMETERS_FILE = path.join(path.dirname(__file__), r'parameters_file.cfg')
DEFAULT_SETTINGS = {'freq_pert': 60, 'bandwith_window': 10, 'lpf_bw': 10, 'harmonic': 2, 'max_time': 1.5,
                    'max_width': 0.2, 'sample_rate': 8000.0, 'theme': sg.theme('BeerBerry')}
# "Map" from the settings dictionary keys to the window's element keys
PARAMETER_KEYS_TO_ELEMENT_KEYS = {'freq_pert': '-FREQ PERT-', 'bandwith_window': '-BW WINDOW-', 'lpf_bw': '-LPF BW-',
                                  'harmonic': '-HARMONIC-',
                                  'max_time': '-MAX TIME-', 'max_width': '-MAX WIDTH-', 'sample_rate': '-SAMPLE RATE-',
                                  'theme': '-THEME-'}

xdata = []
ydata = []


###### Load/Save Parameters File ##########################################
def load_parameters(parameters_file, default_parameters):
    try:
        with open(parameters_file, 'r') as f:
            parameters = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No parameters file found... will create one for you',
                               keep_on_top=True, background_color='red', text_color='white')
        parameters = default_parameters
        save_parameters(parameters_file, parameters, None)
    return parameters


def save_parameters(parameters_file, parameters, values):
    if values:  # if there are stuff specified by another window, fill in those values
        for key in PARAMETER_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
            try:
                parameters[key] = values[PARAMETER_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating parameters from window values. Key = {key}')

    with open(parameters_file, 'w') as f:
        jsondump(parameters, f)

    sg.popup('Parameters saved')


def onclick(event):
    # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
    #     ('double' if event.dblclick else 'single', event.button,
    #     event.x, event.y, event.xdata, event.ydata))
        while True:
            if (len(xdata) < 2):
                xdata.append(event.xdata)
                ydata.append(event.ydata)
            else:
                break
        print(xdata)
        print(ydata)

   



def draw_figure(canvas, figure, toolbar=None):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    toolbar = NavigationToolbar2Tk(figure_canvas_agg, canvas)

    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

    return figure_canvas_agg, toolbar


def destroy_figure(fig_canvas_agg, toolbar):
    fig_canvas_agg.get_tk_widget().forget()
    toolbar.forget()
    plt.close('all')


# ab1 = [[sg.Canvas(size = (700,500), key='-CANVAS-')],
#       [sg.Button('baseline')]]
# tab2 = [[sg.Canvas(size = (700,500), key='-CANVAS2-')]]
# tab3 = [[sg.Canvas(size = (700,500), key='-CANVAS3-')]]

####### Creating the Main Window ################################
def create_main_window(parameters, password_attempt):
    sg.theme(parameters['theme'])
    layout = [[sg.Radio('Pre-Calc', 'RAD1', default=True, font=['Helvetica', 10], key='OP1'),
               sg.Radio('Post-Calc', 'RAD1', font=['Helvetica', 10]),
                sg.In(), sg.FileBrowse(), sg.Button('Log in', visible=False if password_attempt == PASSWORD else True),
               sg.Button('Logout', visible=True if password_attempt == PASSWORD else False)],
              [sg.Button('Load'),
               sg.Button('Insert Parameters', visible=True if password_attempt == PASSWORD else False)],
              
              [sg.Canvas(size=(898, 634), key='-CANVAS-')],
              [sg.Button('plot', disabled=True, ), sg.Button('plot2', disabled=True, ),
               sg.Button('plot3', disabled=True, ), sg.Button('baseline', disabled=True, ),
               sg.FileSaveAs(button_text='save', disabled=True, target='save', enable_events=True, key='save',
                             file_types=(('DATA', '.data'), ('BIN', '.bin'), ('CSV', '.csv'), ('All Files', '*.*'))),
                sg.Radio('Pre-Calc', 'RAD2', default=True, font=['Helvetica', 10], key='OP2'),
                sg.Radio('Post-Calc', 'RAD2', font=['Helvetica', 10]),
               sg.Button('Exit')]]

    return sg.Window('BeerBerry', layout, element_justification='center', font='Helvetica 18')


####### Creating parameters window ##############################
def create_insert_parameters_window(parameters):
    sg.theme(parameters['theme'])

    def TextLabel(text):
        return sg.Text(text + ':', justification='r', size=(30, 1))

    layout = [[sg.Text('Parameters', justification='center', font='Helvetica 18')],
              [TextLabel('Frequency perturbation'), sg.Input(key='-FREQ PERT-')],
              [TextLabel('Band-width window'), sg.Input(key='-BW WINDOW-')],
              [TextLabel('Env lpf bandwidth'), sg.Input(key='-LPF BW-')],
              [TextLabel('Harmonic to Use'), sg.Input(key='-HARMONIC-')],
              [TextLabel('Maximum Time'), sg.Input(key='-MAX TIME-')],
              [TextLabel('Maximum Width'), sg.Input(key='-MAX WIDTH-')],
              [TextLabel('Sample Rate'), sg.Input(key='-SAMPLE RATE-')],
              [TextLabel('Theme'), sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
              [sg.Button('Save'), sg.Button('Exit')]]

    window = sg.Window('Insert Parameters', layout, keep_on_top=True, finalize=True)

    for key in PARAMETER_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
        try:
            window[PARAMETER_KEYS_TO_ELEMENT_KEYS[key]].update(value=parameters[key])
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from parameters. Key = {key}')

    return window


# Initialising empty variables so they can remain within the whole program scope
t, i, f, Imag, Imagfilt, ifilt, ienv, int_ienv, ienv_filtered = ([] for i in range(9))
fig_canvas_agg = None
df = None
df_Post = None
password_attempt = None
window, parameters = None, load_parameters(PARAMETERS_FILE, DEFAULT_SETTINGS)
print(parameters)
while True:

    if window is None:
        window = create_main_window(parameters, password_attempt)

    event, values = window.read()
    fname = values[1]

    print(event)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'plot':
        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg, toolbar)

        window.find_element('baseline').Update(disabled=False)

        fig = matplotlib.figure.Figure(figsize=(9, 6), dpi=100)
        fig.add_subplot(111, xlabel='Time (s)', ylabel='Current (S.U)').plot(t, ienv)
        fig.suptitle('Results', fontsize=16)
        fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'plot2':
        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg, toolbar)

        window.find_element('baseline').Update(disabled=True)
        fig = matplotlib.figure.Figure(figsize=(9, 6), dpi=100)
        fig.add_subplot(111, xlabel='Time (s)', ylabel='Current').plot(t, i)

        fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'plot3':
        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg, toolbar)

        window.find_element('baseline').Update(disabled=True)

        fig = matplotlib.figure.Figure(figsize=(9, 6), dpi=100)
        fig.add_subplot(221).plot(f, Imag)
        fig.add_subplot(223).plot(t, ifilt)
        fig.add_subplot(222).plot(f, Imagfilt)
        fig.add_subplot(224).plot(t, int_ienv)

        fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'Load':

        tmp = window['OP1'].get()

        # if default radio button is clicked, returns true for precalc
        if tmp:
            print(type(fname))
            data = Helper.readFile(fname, 0)
            num = sg.popup_get_text('Harmonic Number', 'Enter nth harmonic')
            t, i, f, Imag, Imagfilt, ifilt, ienv, int_ienv, ienv_filtered = major_function(int(parameters['freq_pert']),
                                                                                           int(parameters[
                                                                                                   'bandwith_window']),
                                                                                           int(parameters['lpf_bw']),
                                                                                           int(num),
                                                                                           float(
                                                                                               parameters['max_time']),
                                                                                           float(
                                                                                               parameters['max_width']),
                                                                                           float(parameters[
                                                                                                     'sample_rate']),
                                                                                           data)

            window.find_element('plot').Update(disabled=False)
            window.find_element('plot2').Update(disabled=False)
            window.find_element('plot3').Update(disabled=False)

            d = {
                't': t,
                'i': i,
                'f': f,
                'Imag': Imag,
                'Imagfilt': Imagfilt,
                'ifilt': ifilt,
                'ienv': ienv,
                'int_ienv': int_ienv,
                'ienv_filtered': ienv_filtered
            }
            df_Post = pd.DataFrame(d)
            print(type(df))
            if df_Post is not None:
                window.find_element('save').Update(disabled=False)
        else:
            df_Post = Helper.readFile(fname, 1)
            t = df_Post[['t']]
            i = df_Post[['i']]
            f = df_Post[['f']]
            Imag = df_Post[['Imag']]
            Imagfilt = df_Post[['Imagfilt']]
            ifilt = df_Post[['ifilt']]
            ienv = df_Post[['ienv']]
            int_ienv = df_Post[['int_ienv']]
            ienv_filtered = df_Post[['ienv_filtered']]

            window.find_element('plot').Update(disabled=False)
            window.find_element('plot2').Update(disabled=False)
            window.find_element('plot3').Update(disabled=False)

            if df_Post is not None:
                window.find_element('save').Update(disabled=False)

    elif event == 'save':

        tmp = window['OP2'].get()
        outFile = values['save']
        if tmp:

            Helper.writeFile(outFile, data, 0)

        else:

            Helper.writeFile(outFile, df_Post, 1)

    elif event == 'baseline':
        if (len(xdata) >= 2):
            xdata = []
            ydata = []
        clickEvent = fig_canvas_agg.mpl_connect('button_press_event', onclick)

    elif event == 'Log in':
        password_attempt = sg.popup_get_text('Password', '')
        while password_attempt != PASSWORD and password_attempt != None:
            password_attempt = sg.popup_get_text('Password is incorrect', '')
        if password_attempt == PASSWORD:
            window.find_element('Logout').Update(visible=True)
            window.find_element('Log in').Update(visible=False)
            window.find_element('Insert Parameters').Update(visible=True)

    elif event == 'Logout':
        password_attempt = None
        window.find_element('Logout').Update(visible=False)
        window.find_element('Log in').Update(visible=True)
        window.find_element('Insert Parameters').Update(visible=False)

    elif event == 'Insert Parameters':
        event, values = create_insert_parameters_window(parameters).read(close=True)
        if event == 'Save':
            window.close()
            window = None
            save_parameters(PARAMETERS_FILE, parameters, values)
            fig_canvas_agg = None

window.close()
