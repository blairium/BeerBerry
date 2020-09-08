import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from json import (load as jsonload, dump as jsondump)
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.widgets import PolygonSelector
from matplotlib.axes import Axes
matplotlib.use('TkAgg')


####### Creating the Main Window ################################
def create_main_window(parameters, password_attempt, PASSWORD):
    sg.theme(parameters['theme']) #sets colour theme of window

    ###creates layout of the window
    layout = [
                # elements in the top row (radio buttons for loading raw data or calculated data, file browser, login button)
                [sg.Radio('Raw Data', 'RAD1', default=True, font=['Helvetica', 10], key='OP1'),
                sg.Radio('Post Calculation', 'RAD1', font=['Helvetica', 10]),
                sg.In(key = '-FILENAME-',enable_events=True), sg.FileBrowse(), sg.Button('Log in', visible=False if password_attempt == PASSWORD else True),
                sg.Button('Logout', visible=True if password_attempt == PASSWORD else False)],

                #elements in the second row (Load button, Insert parameters button which is hidden until logged in)
                [sg.Button('Load',  disabled=True), sg.Button('Insert Parameters', visible=True if password_attempt == PASSWORD else False)],

                #third row contains the canvas for the graphs
                [sg.Canvas(size=(898, 634), key='-CANVAS-')],

                # elements in the fourth row are (buttons to switch different graphs, the define baseline button,
                # map baseline button, save button, radio buttons saving raw or calculated data, and an exit button)
                [sg.Button('plot', disabled=True, ), sg.Button('plot2', disabled=True, ),
                sg.Button('plot3', disabled=True, ), sg.Button('plot4', disabled=True, ),
                sg.Button('plot5', disabled=True, ),sg.Button('plot6', disabled=True, ),
                sg.Button('Define baseline', disabled=True,), sg.Button('Map baseline', disabled=True,),
                sg.FileSaveAs(button_text='save', disabled=True, target='save', enable_events=True, key='save',
                             file_types=(('DATA', '.data'), ('BIN', '.bin'), ('CSV', '.csv'), ('All Files', '*.*'))),
                sg.Radio('Raw Data', 'RAD2', default=True, font=['Helvetica', 10], key='OP2'),
                sg.Radio('Post Calculation', 'RAD2', font=['Helvetica', 10]),
                sg.Button('Exit')]]

    ###return window with layout
    return sg.Window('BeerBerry', layout, element_justification='center', font='Helvetica 18')

####### Creating parameters window ##############################
def create_insert_parameters_window(parameters,PARAMETER_KEYS_TO_ELEMENT_KEYS):
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

####### Create Figure In Canvas ##############################
def draw_figure(canvas, figure, toolbar=None):

    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas) # create canvas containing passed in figure
    toolbar = NavigationToolbar2Tk(figure_canvas_agg, canvas) # create toolbar
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1) #pack figure and toolbar into canvas

    #return canvas and toolbar
    return figure_canvas_agg, toolbar

####### Destroy Figure In Canvas ##############################
def destroy_figure(fig_canvas_agg, toolbar):

    fig_canvas_agg.get_tk_widget().forget() # destroys canvas
    toolbar.forget() # destroys toolbar
    plt.close('all') # destroys figure


###### Load/Save Parameters File ##########################################
def load_parameters(parameters_file, default_parameters, PARAMETER_KEYS_TO_ELEMENT_KEYS):
    try:
        with open(parameters_file, 'r') as f:
            parameters = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No parameters file found... will create one for you',
                               keep_on_top=True, background_color='red', text_color='white')
        parameters = default_parameters
        save_parameters(parameters_file, parameters, None, PARAMETER_KEYS_TO_ELEMENT_KEYS)
    return parameters


def save_parameters(parameters_file, parameters, values, PARAMETER_KEYS_TO_ELEMENT_KEYS):
    if values:  # if there are stuff specified by another window, fill in those values
        for key in PARAMETER_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
            try:
                parameters[key] = values[PARAMETER_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating parameters from window values. Key = {key}')

    with open(parameters_file, 'w') as f:
        jsondump(parameters, f)

    sg.popup('Parameters saved')
