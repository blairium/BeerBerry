import matplotlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg

from json import (load as jsonload, dump as jsondump)
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import PolygonSelector
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

# use tkinter
matplotlib.use('TkAgg')

####### Creating the Main Window ################################


def create_main_window(parameters, password_attempt, PASSWORD):
    sg.theme(parameters['theme'])  # sets colour theme of window
    radio_choices = [
        '1st Harmonic',
        '2nd Harmonic',
        '3rd Harmonic',
        '4th Harmonic',
        '5th Harmonic']

    # creates layout of the window
    layout = [
        # elements in the top row (radio buttons for loading raw data or
        # calculated data, file browser, login button)
        [sg.Radio('Raw Data', 'RAD1', default=True, font=['Helvetica', 10], key='OP1'),
         sg.Radio('Post Calculation', 'RAD1', font=['Helvetica', 10]),
         sg.In(key='-FILENAME-', enable_events=True), sg.FileBrowse(),
         sg.Button('Record Data', auto_size_button=True),
         sg.Button('Load', disabled=True),
         sg.Button(
            'Log in',
            visible=False if password_attempt == PASSWORD else True),
            sg.Button(
            'Logout',
            visible=True if password_attempt == PASSWORD else False),
            sg.Button('Insert Parameters', auto_size_button=True, visible=True if password_attempt == PASSWORD else False)],




        # third row contains the canvas for the graphs
        [sg.Canvas(size=(598, 634), key='-CANVAS-')],

        # elements in the fourth row are (buttons to switch different graphs, the define baseline button,
        # map baseline button, save button, radio buttons saving raw or calculated data, and an exit button)
        [sg.Checkbox('1st Harmonic', enable_events=True, key='r1'), sg.Checkbox('2nd Harmonic', default=True, enable_events=True, key='r2'), sg.Checkbox('3rd Harmonic', enable_events=True, key='r3'),
         sg.Checkbox('4th Harmonic', enable_events=True, key='r4'), sg.Checkbox('5th Harmonic', enable_events=True, key='r5')],
        [sg.Button('plot', disabled=True, auto_size_button=True), sg.Button('plot2', disabled=True, auto_size_button=True),
         sg.Button('Freq vs Mag of Current', disabled=True, ), sg.Button('Cumulative Sum', disabled=True, ),
         sg.Button('Define baseline', disabled=True, auto_size_button=True), sg.Button('Map baseline', disabled=True, auto_size_button=True),

         sg.FileSaveAs(button_text='save', disabled=True, target='save', enable_events=True, key='save',
                       file_types=(('DATA', '.data'), ('BIN', '.bin'), ('CSV', '.csv'), ('All Files', '*.*')), auto_size_button=True),
         sg.Radio('Raw Data', 'RAD2', default=True, font=['Helvetica', 10], key='OP2'),
         sg.Radio('Post Calculation', 'RAD2', font=['Helvetica', 10]),
         sg.Button('Exit', auto_size_button=True)]
    ]

    # return window with layout
    return sg.Window(
        'BeerBerry',
        layout,
        element_justification='center',
        font='Helvetica 18',
        resizable=True)

####### Creating parameters window ##############################


def create_insert_parameters_window(
        parameters,
        PARAMETER_KEYS_TO_ELEMENT_KEYS):
    sg.theme(parameters['theme'])

    def TextLabel(text):
        return sg.Text(text + ':', justification='r', size=(30, 1))

    layout = [[sg.Text('Parameters', justification='center', font='Helvetica 18')],
              [TextLabel('Frequency perturbation'), sg.Input(key='-FREQ PERT-')],
              [TextLabel('Band-width window'), sg.Input(key='-BW WINDOW-')],
              [TextLabel('Env lpf bandwidth'), sg.Input(key='-LPF BW-')],
              [TextLabel('Sample Rate'), sg.Input(key='-SAMPLE RATE-')],
              [TextLabel('Theme'), sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
              [sg.Button('Save'), sg.Button('Exit')]]

    window = sg.Window(
        'Insert Parameters',
        layout,
        keep_on_top=True,
        finalize=True)

    for key in PARAMETER_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
        try:
            window[PARAMETER_KEYS_TO_ELEMENT_KEYS[key]].update(
                value=parameters[key])
        except Exception as e:
            print(
                f'Problem updating PySimpleGUI window from parameters. Key = {key}')

    return window


def create_excitation_parameters_window(
        exc_parameters,
        EXCITATION_KEYS_TO_ELEMENT_KEYS):

    def TextLabel(text):
        return sg.Text(text + ':', justification='r', size=(30, 1))

    layout = [[sg.Text('Parameters', justification='center', font='Helvetica 18')],
              [TextLabel('amplitude'), sg.Input(key='-AMPLITUDE-')],
              [TextLabel('stable'), sg.Input(key='-STABLE-')],
              [TextLabel('sample_rate'), sg.Input(key='-EXC SAMPLE RATE-')],
              [TextLabel('duration'), sg.Input(key='-DURATION-')],
              [TextLabel('frequency'), sg.Input(key='-FREQ-')],
              [TextLabel('v1'), sg.Input(key='-V1-')],
              [TextLabel('v2'), sg.Input(key='-V2-')],
              [TextLabel('v3'), sg.Input(key='-V3-')],
              [sg.Button('Record'), sg.Button('Cancel')]]

    window = sg.Window(
        'Excitation Parameters',
        layout,
        keep_on_top=True,
        finalize=True)

    for key in EXCITATION_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
        try:
            window[EXCITATION_KEYS_TO_ELEMENT_KEYS[key]].update(
                value=exc_parameters[key])
        except Exception as e:
            print(
                f'Problem updating PySimpleGUI window from parameters. Key = {key}')

    return window

####### Create Figure In Canvas ##############################


def draw_figure(canvas, figure, toolbar=None):
    # create canvas containing passed in figure
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    toolbar = NavigationToolbar2Tk(figure_canvas_agg, canvas)  # create toolbar
    figure_canvas_agg.get_tk_widget().pack(
        side='top', fill='both', expand=1)  # pack figure and toolbar into canvas

    # return canvas and toolbar
    return figure_canvas_agg, toolbar

####### Destroy Figure In Canvas ##############################


def destroy_figure(fig_canvas_agg, toolbar):
    fig_canvas_agg.get_tk_widget().forget()  # destroys canvas
    toolbar.forget()  # destroys toolbar
    plt.close('all')  # destroys figure


###### Load/Save Parameters File ##########################################
def load_parameters(
        parameters_file,
        default_parameters,
        PARAMETER_KEYS_TO_ELEMENT_KEYS):
    try:
        with open(parameters_file, 'r') as f:
            parameters = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(
            f'exception {e}',
            'No parameters file found... will create one for you',
            keep_on_top=True,
            background_color='red',
            text_color='white')
        parameters = default_parameters
        save_parameters(
            parameters_file,
            parameters,
            None,
            PARAMETER_KEYS_TO_ELEMENT_KEYS)
    return parameters


def save_parameters(
        parameters_file,
        parameters,
        values,
        PARAMETER_KEYS_TO_ELEMENT_KEYS):
    if values:  # if there are stuff specified by another window, fill in those values
        for key in PARAMETER_KEYS_TO_ELEMENT_KEYS:  # update window with the values read from settings file
            try:
                parameters[key] = values[PARAMETER_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(
                    f'Problem updating parameters from window values. Key = {key}')

    with open(parameters_file, 'w') as f:
        jsondump(parameters, f)

    