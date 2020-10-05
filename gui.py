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

# helper text label
def TextLabel(text, justification = 'r', width = 30):
        return sg.Text(text + ':', justification=justification, size=(width, 1))

def create_main_window(parameters, password_attempt, PASSWORD):
    sg.theme('BeerBerry')  # sets colour theme of window
    radio_choices = [
        '1st Harmonic',
        '2nd Harmonic',
        '3rd Harmonic',
        '4th Harmonic',
        '5th Harmonic']

    # creates layout of the window
    layout = [[
        sg.Column([
        
            # Row 1: record/load data, parameters, login
            [
                sg.Column([[
                    sg.Column([[sg.Button('Record Data')]], element_justification='center',),
                    sg.Column([[sg.FileBrowse(button_text='Select Data File', key="Select Data File", enable_events=True)]]),
                    sg.Column([[sg.Button('Parameters', disabled=True, button_color=('white','#adadad'))]]),
                    sg.Column([[sg.Button('Login', key='Authenticate')]]),
                    
                ]], justification='center')
            ],

            # Row 2: selected filename, optional
            [
                sg.Column([
                    [TextLabel('File', 'center', None), sg.Input(key='Filename', disabled=True)]
                ], key='File Container', justification='center')
            ],

            # hidden: baseline coords
            [
                sg.Column([
                    [sg.Input(key="x1")],
                    [sg.Input(key="y1")],
                    [sg.Input(key="x2")],
                    [sg.Input(key="y2")],
                ], visible=False)
            ],

            # Row 3: graph controls, canvas and results
            [
                sg.Column([
                    [
                        sg.Radio('Harmonics', key='Harmonics', group_id='graph_control_radio', disabled=True, enable_events=True, font='Helvetica 12'),
                        sg.Radio('Time Domain', key='Time Domain', group_id='graph_control_radio', disabled=True, enable_events=True, font='Helvetica 12'),
                        sg.Radio('Freq Domain', key='Freq Domain', group_id='graph_control_radio', disabled=True, enable_events=True, font='Helvetica 12'),
                        sg.Radio('Cumulative Sum', key='Cumulative Sum', group_id='graph_control_radio', disabled=True, enable_events=True, font='Helvetica 12'),
                        sg.Radio('Envelope', key='Envelope', group_id='graph_control_radio', disabled=True, enable_events=True, font='Helvetica 12')
                    ],
                    [
                        sg.Canvas(size=(898, 634), key='-CANVAS-'),
                    ]
                ], key='Graph Controls', element_justification='center', justification='center'),

                sg.Column([[
                    #sg.Frame('Results', 
                    #    [
                    #        [sg.Text('Conc: 25ppm')], 
                    #        [sg.Text('Peak Area: 50')], 
                    #        [sg.Text('Peak Height: 10')]
                    #    ])
                    TextLabel('Results', 'center', None), sg.Input(key='PPM', disabled=True)
                ]], key='Results', element_justification='center', justification='center')
            ],

            # Row 4: harmonic checkboxes
            [
                sg.Column([[
                    sg.Checkbox('1st Harmonic', enable_events=True, key='r1', disabled=True), 
                    sg.Checkbox('2nd Harmonic', enable_events=True, key='r2', disabled=True), 
                    sg.Checkbox('3rd Harmonic', enable_events=True, key='r3', disabled=True),
                    sg.Checkbox('4th Harmonic', enable_events=True, key='r4', disabled=True), 
                    sg.Checkbox('5th Harmonic', enable_events=True, key='r5', disabled=True)
                ]], key='Harmonic Container', justification='center')
            ],

            # Ro 5: graph controls
            #[
                
            #],

            # Row 6: define baseline, calculate result, save data, exit
            [
                sg.Button('Define Baseline', key='Define baseline', disabled=True, auto_size_button=True), 
                sg.FileSaveAs(button_text='Save Raw Data', key='Save Raw Data', target='Save Raw Data', disabled=True, enable_events=True, file_types=(('DATA', '.data'), ('BIN', '.bin'), ('CSV', '.csv'), ('All Files', '*.*')), auto_size_button=True),
                sg.FileSaveAs(button_text='Save Processed Data', key='Save Processed Data', disabled=True, target='Save Processed Data', enable_events=True, file_types=(('DATA', '.data'), ('BIN', '.bin'), ('CSV', '.csv'), ('All Files', '*.*')), auto_size_button=True),
                sg.Button('Exit', auto_size_button=True)
            ]
        ], element_justification='center', justification='center', scrollable=True, size=(935, 930))]]

    # return window with layout
    return sg.Window(
        'BeerBerry',
        layout,
        element_justification='center',
        font='Helvetica 18',
        resizable=True)

####### Creating parameters window ##############################

def create_parameters_window(
        parameters,
        PARAMETER_KEYS_TO_ELEMENT_KEYS):


    def TextLabel(text):
        return sg.Text(text + ':', justification='r', size=(30, 1))

    layout = [[sg.Text('Parameters', justification='center', font='Helvetica 18')],
              [TextLabel('Frequency perturbation'), sg.Input(key='-FREQ PERT-')],
              [TextLabel('Band-width window'), sg.Input(key='-BW WINDOW-')],
              [TextLabel('Env lpf bandwidth'), sg.Input(key='-LPF BW-')],
              [TextLabel('Sample Rate'), sg.Input(key='-SAMPLE RATE-')],
              [TextLabel('Callibration A'), sg.Input(key='-A-')],
              [TextLabel('Callibration B'), sg.Input(key='-B-')],
              [TextLabel('Callibration C'), sg.Input(key='-C-')],
              [sg.Button('Save'), sg.Button('Exit')]]

    window = sg.Window(
        'Insert Parameters',
        layout,
        keep_on_top=True,
        finalize=True,
        grab_anywhere=True
        )

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

