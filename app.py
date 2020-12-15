import codecs
import matplotlib

import PySimpleGUI as sg
import pandas as pd
import numpy as np
import peakutils as pk
import matplotlib.pyplot as plt
import time

from os import path
from json import (load as jsonload, dump as jsondump)

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import PolygonSelector
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


plt.style.use(['science','ieee'])
plt.ioff()

"""
This file contains the main processes and functions of the app.
Graphing functionality is also contained here.

Last Updated: 08/10/2020
Author: Joshua Failla
Contributors: Michael Graps, Andrew Durnford, Nathan Gillbanks
"""

# local modules
import file
import maths
from gui import (
    create_main_window,
    create_parameters_window,
    draw_figure,
    destroy_figure,
    load_parameters,
    save_parameters,
    create_excitation_parameters_window)

# use tkinter
matplotlib.use('TkAgg')


####### Parameter Info ################################
sg.LOOK_AND_FEEL_TABLE['BeerBerry'] = {
    'BACKGROUND': '#FFFFFF',
    'TEXT': '#000000',
    'INPUT': '#C4C4C4',
    'TEXT_INPUT': '#000000',
    'SCROLL': '#c7e78b',
    'BUTTON': (
        'white',
        '#40BAD2'),
    'PROGRESS': (
        '#01826B',
        '#D0D0D0'),
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0,
}
PASSWORD = '1245'
PARAMETERS_FILE = path.join(path.dirname(__file__), r'parameters_file.cfg')
DEFAULT_SETTINGS = {
    'freq_pert': 60,
    'bandwith_window': 10,
    'lpf_bw': 10,
    'sample_rate': 8000.0,
    'a': 1e-8,
    'b': 1e-8,
    'c': 1e-8}

# "Map" from the settings dictionary keys to the window's element keys
PARAMETER_KEYS_TO_ELEMENT_KEYS = {
    'freq_pert': '-FREQ PERT-',
    'bandwith_window': '-BW WINDOW-',
    'lpf_bw': '-LPF BW-',
    'sample_rate': '-SAMPLE RATE-',
    'a': '-A-',
    'b': '-B-',
    'c': '-C-'}

EXCITATION_PARAMETER = path.join(path.dirname(__file__), r'exciation_file.cfg')
EXCITATION_SETTINGS = {
    'amplitude': 0.06,
    'stable': 2.0,
    'sample_rate': 8000,
    'duration': 8.0,
    'frequency': 60.0,
    'v1': 0.0,
    'v2': 0.0,
    'v3': 0.7}
# "Map" from the settings dictionary keys to the window's element keys
EXCITATION_KEYS_TO_ELEMENT_KEYS = {
    'amplitude': '-AMPLITUDE-',
    'stable': '-STABLE-',
    'sample_rate': '-EXC SAMPLE RATE-',
    'duration': '-DURATION-',
    'frequency': '-FREQ-',
    'v1': '-V1-',
    'v2': '-V2-',
    'v3': '-V3-'}

# raw or post data type
TYPE = None

# colors
GREEN = '#32cd32'
GREY = '#adadad'
TEAL = '#40bad2'
RED = '#ff3232'
BLUE = '#1f75fe'

# Initialising empty variables so they can remain within the whole program
# scope
t, i, f, Imag, Imagfilt, ifilt, ienv, int_ienv, ienv_filtered = (
    [] for i in range(9))
harm_one, harm_two, harm_three, harm_four, harm_five = ([] for i in range(5))

df = None
df_Post = None
data = None
fname = None
password_attempt = None

window, parameters, exc_parameters=None, load_parameters(
    PARAMETERS_FILE, DEFAULT_SETTINGS, PARAMETER_KEYS_TO_ELEMENT_KEYS), load_parameters(
    EXCITATION_PARAMETER, EXCITATION_SETTINGS, EXCITATION_KEYS_TO_ELEMENT_KEYS)
xdata = []
ydata = []
clickEvent = None

fig_canvas_agg = None
toolbar = None


def disable_button_grey(button):
    window.find_element(button).Update(
        disabled=True, button_color=('white', GREY))


def disable_button_teal(button):
    window.find_element(button).Update(
        disabled=True, button_color=('white', TEAL))


def enable_button_teal(button):
    window.find_element(button).Update(
        disabled=False, button_color=('white', TEAL))


def enable_button_green(button):
    window.find_element(button).Update(
        disabled=False, button_color=('white', GREEN))


def disable_harmonics():
    window.find_element("r1").Update(disabled=True)
    window.find_element("r2").Update(disabled=True)
    window.find_element("r3").Update(disabled=True)
    window.find_element("r4").Update(disabled=True)
    window.find_element("r5").Update(disabled=True)


def enable_harmonics():
    window.find_element("r1").Update(disabled=False)
    window.find_element("r2").Update(disabled=False)
    window.find_element("r3").Update(disabled=False)
    window.find_element("r4").Update(disabled=False)
    window.find_element("r5").Update(disabled=False)


def show_harmonics_graph():
    global fig_canvas_agg
    global toolbar

    enable_harmonics()

    if fig_canvas_agg:
        destroy_figure(fig_canvas_agg, toolbar)

    fig = plt.figure()
    window.find_element('Define baseline').Update(disabled=False)

    if window['r1'].get():
        plt.plot(t, harm_one, color='b')
    if window['r2'].get():
        plt.plot(t, harm_two, color='#40BAD3')
    if window['r3'].get():
        plt.plot(t, harm_three, color='orange')
    if window['r4'].get():
        plt.plot(t, harm_four, color='g')
    if window['r5'].get():
        plt.plot(t, harm_five, color='y')

    fig.suptitle('Harmonics', fontsize=16)
    fig.set_size_inches(6, 4) #original 9,6
    fig.set_dpi(100)
    plt.xlabel('Time (s)')
    plt.ylabel('Current (S.U)')

    fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)


def show_envelope_graph():
    global fig_canvas_agg
    global toolbar
    global harm_one
    global harm_two
    global harm_three
    global harm_four
    global harm_five

    enable_harmonics()

    if fig_canvas_agg:
        destroy_figure(fig_canvas_agg, toolbar)

    fig = plt.figure()

    fig.clf()

    print(plt.xlim())

    if window['r1'].get():
        envelope = pk.envelope(harm_one, deg=5, max_it=None, tol=1e-3)
        plt.plot(t, envelope, color='b')
    if window['r2'].get():
        envelope = pk.envelope(harm_two, deg=5, max_it=None, tol=1e-3)
        plt.plot(t, envelope, color='#40BAD3')
    if window['r3'].get():
        envelope = pk.envelope(harm_three, deg=5, max_it=None, tol=1e-3)
        plt.plot(t, envelope, color='orange')
    if window['r4'].get():
        envelope = pk.envelope(harm_four, deg=5, max_it=100, tol=1e-3)
        plt.plot(t, envelope, color='g')
    if window['r5'].get():
        envelope = pk.envelope(harm_five, deg=5, max_it=100, tol=1e-3)
        plt.plot(t, envelope, color='y')

    fig.suptitle('Envelope', fontsize=16)
    fig.set_size_inches(6, 4) #orig 9,6
    fig.set_dpi(100)
    plt.xlabel('Time (s)')
    plt.ylabel('Current (S.U)')
    fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)


# main function to load/process data
def start():
    global fig_canvas_agg
    global toolbar
    global df
    global df_Post
    global data
    global t
    global i
    global f
    global Imag
    global Imagfilt
    global ifilt
    global ienv
    global int_ienv
    global ienv_filtered
    global harm_one
    global harm_two
    global harm_three
    global harm_four
    global harm_five

    window.find_element('PPM').Update('')

    # this is for the Layout Design of the Window
    layout2 = [[sg.Text('Loading')],
               [sg.ProgressBar(1, orientation='h', size=(
                   20, 20), key='progress', style='winnative')],
               ]

    # This Creates the Physical Window
    window2 = sg.Window('File Load', layout2).Finalize()
    progress_bar = window2.FindElement('progress')

    # This Updates the Window
    # progress_bar.UpdateBar(Current Value to show, Maximum Value to show)
    progress_bar.UpdateBar(0, 5)
    # adding time.sleep(length in Seconds) has been used to Simulate adding your script in between Bar Updates
    time.sleep(.5)

    enable_harmonics()

    # if default radio button is clicked, returns true for precalc
    if TYPE is 'RAW':
        if len(data.columns) == 2:
            # Column 1: Voltage
            v = data.iloc[:, 0].values
            i = data.iloc[:, 1].values

            #v, i = maths.blanking_first_samples(8000, v, i) #changed to 8000
            f, t = maths.get_time_values(
                i, float(parameters['sample_rate']))
            Imag = maths.magnitude_of_current(i, i.size)

            window.find_element('Define baseline').Update(disabled=False)

            harm_one = maths. filter_ienv(maths.get_ienv(
                i, int(
                    parameters['freq_pert']), 1, int(
                    parameters['bandwith_window']), float(
                    parameters['sample_rate']), int(
                    parameters['lpf_bw']), t),200)

            progress_bar.UpdateBar(1, 5)

            harm_two = maths. filter_ienv(maths.get_ienv(
                i, int(
                    parameters['freq_pert']), 2, int(
                    parameters['bandwith_window']), float(
                    parameters['sample_rate']), int(
                    parameters['lpf_bw']), t),200)

            progress_bar.UpdateBar(2, 5)
            time.sleep(.5)

            harm_three = maths. filter_ienv(maths.get_ienv(
                i, int(
                    parameters['freq_pert']), 3, int(
                    parameters['bandwith_window']), float(
                    parameters['sample_rate']), int(
                    parameters['lpf_bw']), t),200)

            progress_bar.UpdateBar(3, 5)

            harm_four = maths. filter_ienv(maths.get_ienv(
                i, int(
                    parameters['freq_pert']), 4, int(
                    parameters['bandwith_window']), float(
                    parameters['sample_rate']), int(
                    parameters['lpf_bw']), t),200)
            progress_bar.UpdateBar(4, 5)

            harm_five = maths. filter_ienv(maths.get_ienv(
                i, int(
                    parameters['freq_pert']), 5, int(
                    parameters['bandwith_window']), float(
                    parameters['sample_rate']), int(
                    parameters['lpf_bw']), t),200)

            time.sleep(0.5)
            # This will Close The Window
            window2.Close()

            int_ienv = maths.cumulative_sum_ienv(harm_two)
            ienv_filtered = maths.filter_ienv(
                harm_two, 200)

            # open harmonic with 2nd selected
            window.find_element("r2").Update(value=True)
            show_harmonics_graph()

            window.find_element('Harmonics').Update(disabled=False, value=True)
            window.find_element('Time Domain').Update(disabled=False)
            window.find_element('Freq Domain').Update(disabled=False)
            window.find_element('Cumulative Sum').Update(disabled=False)
            window.find_element('Envelope').Update(disabled=False)

            d = {
                't': t,
                'i': i,
                'f': f,
                'Imag': Imag,
                'harm_one': harm_one,
                'harm_two': harm_two,
                'harm_three': harm_three,
                'harm_four': harm_four,
                'harm_five': harm_five,
                'int_ienv': int_ienv,
                'ienv_filtered': ienv_filtered
            }
            df_Post = pd.DataFrame(d)

            window.find_element('Harmonic Container').Update(visible=True)
            if df_Post is not None:
                if password_attempt == PASSWORD:
                    window.find_element('Save Raw Data').Update(disabled=False)
                window.find_element(
                    'Save Processed Data').Update(disabled=False)

        elif len(data.columns) == 11:
            sg.popup_error(
                'Error: Select Post Calculation to Load Calculated Data Files')
        else:
            sg.popup_error('Error: Incompatible Data File')

    elif TYPE == 'PROCESSED':
        df_Post = file.readFile(fname, 1)
        print(df_Post)
        print(len(df_Post.columns))
        if len(df_Post.columns) == 11:
            t = df_Post['t']
            i = df_Post['i']
            f = df_Post['f']
            Imag = df_Post['Imag']
            harm_one = df_Post['harm_one']
            harm_two = df_Post['harm_two']
            harm_three = df_Post['harm_three']
            harm_four = df_Post['harm_four']
            harm_five = df_Post['harm_five']
            int_ienv = df_Post['int_ienv']
            ienv_filtered = df_Post['ienv_filtered']

            # open harmonic with 2nd selected
            window.find_element("r2").Update(value=True)
            show_harmonics_graph()

            window.find_element('Harmonics').Update(disabled=False, value=True)
            window.find_element('Time Domain').Update(disabled=False)
            window.find_element('Freq Domain').Update(disabled=False)
            window.find_element('Cumulative Sum').Update(disabled=False)
            window.find_element('Envelope').Update(disabled=False)

            time.sleep(0.1)
            progress_bar.UpdateBar(1, 5)
            progress_bar.UpdateBar(2, 5)
            time.sleep(0.2)
            progress_bar.UpdateBar(3, 5)
            progress_bar.UpdateBar(4, 5)
            progress_bar.UpdateBar(5, 5)
            time.sleep(0.5)
            # This will Close The Window
            window2.Close()

            if df_Post is not None:
                window.find_element(
                    'Save Processed Data').Update(disabled=False)

        elif len(df_Post.columns) == 2:
            sg.popup_error('Error: Select Raw Data to Load Raw Data files')

        else:
            sg.popup_error('Error: Incompatible Data File')

# handle events of the program loop
while True:

    if window is None:
        window = create_main_window(parameters, password_attempt, PASSWORD)

    event, values = window.read()

    print(event)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    elif event == 'Harmonics':
        if (not xdata and not ydata):
            show_harmonics_graph()
        else:
            print('calc')
            calculate_results()

    elif event == 'r1' or event == 'r2' or event == 'r3' or event == 'r4' or event == 'r5':
        if window['Envelope'].get():
            show_envelope_graph()
        if window['Harmonics'].get():
            if (not xdata and not ydata):
                show_harmonics_graph()
            else:
                print('calc')
                calculate_results()

    elif event == 'Time Domain':
        disable_harmonics()

        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg, toolbar)

        window.find_element('Define baseline').Update(disabled=True)

        fig = plt.figure()

        fig.clf()

        plt.plot(t,i)
        fig.suptitle('Raw Signal', fontsize=16)
        fig.set_size_inches(6, 4) #orig 9,6
        fig.set_dpi(100)
        plt.xlabel('Time (s)')
        plt.ylabel('Current (S.U)')
        fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

        # fig = matplotlib.figure.Figure(figsize=(9, 6), dpi=100)
        # fig.suptitle('Time Domain', fontsize=16)
        # fig.add_subplot(
        #     111,
        #     xlabel='Time (s)',
        #     ylabel='Current (S.U)').plot(
        #     t,
        #     i,
        #     c='#40BAD2')

        # fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'Freq Domain':
        disable_harmonics()

        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg, toolbar)

        window.find_element('Define baseline').Update(disabled=True)

        # split data to limit
        limit = int(parameters['freq_pert']) * 100
        newF = np.copy(f[:limit])
        newImag = np.copy(Imag[:limit])
        
        
        fig = plt.figure()

        fig.clf()

        plt.plot(newF, newImag)
        fig.suptitle('Frequency Domain', fontsize=16)
        fig.set_size_inches(6, 4) #orig 9,6
        fig.set_dpi(100)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude of Current')
        fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

        # fig = matplotlib.figure.Figure(figsize=(9, 6), dpi=100)

        # fig.suptitle('Freq Domain', fontsize=16)

        # ax = fig.add_subplot(
        #     111,
        #     xlabel='Frequency (hz)',
        #     ylabel='Magnitude of Current')

        # ax.plot(newF, newImag, c='#40BAD2')

        # fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'Cumulative Sum':
        disable_harmonics()

        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg, toolbar)

        window.find_element('Define baseline').Update(disabled=True)
        
        
        fig = matplotlib.figure.Figure(figsize=(9, 6), dpi=100)
        fig.suptitle('Cumulative Sum', fontsize=16)
        fig.add_subplot(
            111,
            xlabel='Time (s)',
            ylabel='Ienv').plot(
            t,
            int_ienv,
            c='#40BAD2')

        fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'Envelope':
        show_envelope_graph()

###############################################################################

    elif event == 'Record Data':
        proceed = False

        if password_attempt == PASSWORD:
            exc_event, exc_values = create_excitation_parameters_window(
                exc_parameters, EXCITATION_KEYS_TO_ELEMENT_KEYS).read(close=True)
            if exc_event == 'Record':
                proceed = True
        else:
            exc_values = exc_parameters
            proceed = True

        if proceed == True:
            layout2 = [[sg.Text('Recording')],
                       [sg.ProgressBar(1, orientation='h', size=(
                           20, 20), key='progress', style='winnative')],
                       ]

            # This Creates the Physical Window
            window2 = sg.Window('File Load', layout2).Finalize()
            progress_bar = window2.FindElement('progress')
            progress_bar.UpdateBar(0, 5)
            time.sleep(1)
            progress_bar.UpdateBar(1, 5)
            save_parameters(
                EXCITATION_PARAMETER,
                exc_parameters,
                exc_values,
                EXCITATION_KEYS_TO_ELEMENT_KEYS)

            progress_bar.UpdateBar(3, 5)

            data = maths.excitation(exc_parameters)
            #volt = data = maths.time2volt(exc_parameters)
            progress_bar.UpdateBar(4, 5)
            time.sleep(1)
            progress_bar.UpdateBar(5, 5)
            time.sleep(1)
            window2.close()
            sg.PopupOK("Recording Complete")
            TYPE = 'RAW'
            window.TKroot.title('BeerBerry')
            start()

    elif event == 'Select Data File':
        
        if fname != values['Select Data File']:
            fname = values['Select Data File']

            if fname:
                # determine file type
                success = False
                temp = file.readFile(fname, 0)

                if len(temp.columns) == 2:
                    if (password_attempt == PASSWORD):
                        TYPE = 'RAW'
                        success = True
                        data = file.readFile(fname, 0)
                    else:
                        sg.popup_error(
                            'Error: Please login to load Raw data files')
                elif len(temp.columns) == 11:
                    TYPE = 'PROCESSED'
                    success = True
                else:
                    sg.popup_error('Error: Incompatible Data File')

                if success:
                    # window.find_element('Filename').Update(fname)
                    window.TKroot.title('BeerBerry - ' + fname)
                    start()
 
    elif event == 'Save Raw Data':
        outFile = values['Save Raw Data']
        file.writeFile(outFile, data, 0)

    elif event == 'Save Processed Data':
        outFile = values['Save Processed Data']
        file.writeFile(outFile, df_Post, 1)

    elif event == 'Save Figure':
        outFile = values['Save Figure']
        file.writeFile(outFile, data, 0)

    elif event == 'Authenticate':
        # logout
        if password_attempt == PASSWORD:
            password_attempt = None
            window.find_element('Authenticate').Update("Login")
            disable_button_grey('Parameters')
            disable_button_grey('Save Raw Data')

        # login
        else:
            password_attempt = sg.popup_get_text('Password', '')
            while password_attempt != PASSWORD and password_attempt is not None:
                password_attempt = sg.popup_get_text(
                    'Password is incorrect', '')
            if password_attempt == PASSWORD:
                window.find_element('Authenticate').Update("Logout")
                enable_button_teal('Parameters')
                if data is not None:
                    enable_button_teal('Save Raw Data')
                else:
                    disable_button_teal('Save Raw Data')

    elif event == 'Parameters':
        param_event, values = create_parameters_window(
            parameters, PARAMETER_KEYS_TO_ELEMENT_KEYS).read(
            close=True)
        if param_event == 'Save':
            save_parameters(
                PARAMETERS_FILE,
                parameters,
                values,
                PARAMETER_KEYS_TO_ELEMENT_KEYS)
            sg.popup('Parameters saved')

            if TYPE is not None:
                start()

    #################################################################################

    def calculate_results():
        global fig_canvas_agg
        global toolbar

        enable_harmonics()
        area = 0
        height = 0

        fig = plt.figure()
        if window['r1'].get():
            plt.plot(t, harm_one, color='b')
            if maths.is_y_valid(t, harm_one, xdata, ydata):
                copy_x_data = np.copy(xdata)
                copy_y_data = np.copy(ydata)
                curve_1, curve_2, peak_height, index_of_peak, diff_curves, area_between_curves = maths.map_baseline(
                    t, harm_one, copy_x_data, copy_y_data)
                plt.plot(t, curve_2, color='b')
                plt.plot([t[index_of_peak], t[index_of_peak]], [
                    curve_2[index_of_peak], curve_1[index_of_peak]], color='r')

                plt.fill_between(t, curve_1, curve_2, alpha=0.3)
                print("Harm One")

        if window['r2'].get():
            plt.plot(t, harm_two, color='#40BAD3')
            if maths.is_y_valid(t, harm_two, xdata, ydata):
                copy_x_data = np.copy(xdata)
                copy_y_data = np.copy(ydata)
                curve_1, curve_2, peak_height, index_of_peak, diff_curves, area_between_curves = maths.map_baseline(
                    t, harm_two, copy_x_data, copy_y_data)
                plt.plot(t, curve_2, color='#40BAD3')
                plt.plot([t[index_of_peak], t[index_of_peak]], [
                    curve_2[index_of_peak], curve_1[index_of_peak]], color='r', label='Height: ' + str(peak_height))
                plt.fill_between(t, curve_1, curve_2, alpha=0.3,
                                 label='Area: ' + str(area_between_curves))
                plt.legend(loc="upper left")

                area = area_between_curves
                height = peak_height

                print("Harm Two")
        if window['r3'].get():
            plt.plot(t, harm_three, color='orange')
            if maths.is_y_valid(t, harm_three, xdata, ydata):
                copy_x_data = np.copy(xdata)
                copy_y_data = np.copy(ydata)
                curve_1, curve_2, peak_height, index_of_peak, diff_curves, area_between_curves = maths.map_baseline(
                    t, harm_three, copy_x_data, copy_y_data)
                plt.plot(t, curve_2, color='orange')
                plt.plot([t[index_of_peak], t[index_of_peak]], [
                    curve_2[index_of_peak], curve_1[index_of_peak]], color='r')
                plt.fill_between(t, curve_1, curve_2, alpha=0.3)
        if window['r4'].get():
            plt.plot(t, harm_four, color='g')
            if maths.is_y_valid(t, harm_four, xdata, ydata):
                copy_x_data = np.copy(xdata)
                copy_y_data = np.copy(ydata)
                curve_1, curve_2, peak_height, index_of_peak, diff_curves, area_between_curves = maths.map_baseline(
                    t, harm_four, copy_x_data, copy_y_data)
                plt.plot(t, curve_2, color='g')
                plt.plot([t[index_of_peak], t[index_of_peak]], [
                    curve_2[index_of_peak], curve_1[index_of_peak]], color='r')
                plt.fill_between(t, curve_1, curve_2, alpha=0.3)
        if window['r5'].get():
            plt.plot(t, harm_five, color='y')
            if maths.is_y_valid(t, harm_five, xdata, ydata):
                copy_x_data = np.copy(xdata)
                copy_y_data = np.copy(ydata)
                curve_1, curve_2, peak_height, index_of_peak, diff_curves, area_between_curves = maths.map_baseline(
                    t, harm_five, copy_x_data, copy_y_data)
                plt.plot(t, curve_2, color='y')
                plt.plot([t[index_of_peak], t[index_of_peak]], [
                    curve_2[index_of_peak], curve_1[index_of_peak]], color='r')
                plt.fill_between(t, curve_1, curve_2, alpha=0.3)

        fig.suptitle('Harmonics', fontsize=16)
        fig.set_size_inches(6, 4) #orig 9,6
        fig.set_dpi(100)
        destroy_figure(fig_canvas_agg, toolbar)
        fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

        window.find_element('Envelope').Update(disabled=False)
        
        # handle results
        ret = ''
       
        ppm = maths.conc(float(parameters['a']), float(
            parameters['b']), float(parameters['c']), area)

        if ppm == -2:
            window.find_element('PPM').Update(text_color=RED)
            ret = 'Signal beyond calibration range defined by constants'
        elif ppm == -1:
            window.find_element('PPM').Update(text_color=RED)
            ret = 'Concentration too high, out of range of calibration'
        else:
            window.find_element('PPM').Update(text_color=GREEN)
            ret = str(ppm) + 'ppm free SO2'

        window.find_element('PPM').Update(ret)
        window.find_element('Define baseline').Update(disabled=False)

    # handle on graph baseline points click
    def onclick(event):
        global fig_canvas_agg
        global toolbar
        global window

        tmp = 'Please select second point on the graph'
        window.find_element('PPM').Update(tmp, text_color=BLUE)

        if (len(xdata) < 2):
            xdata.append(event.xdata)
            ydata.append(event.ydata)

            if (len(xdata) == 2):
                # enable graphs
                window.find_element('Harmonics').Update(disabled=False)
                window.find_element('Time Domain').Update(disabled=False)
                window.find_element('Freq Domain').Update(disabled=False)
                window.find_element('Cumulative Sum').Update(disabled=False)
                window.find_element('Envelope').Update(disabled=False)
                calculate_results()

    if event == 'Define baseline':
        window.find_element('Define baseline').Update(disabled=True)

        # disable graphs
        window.find_element('Harmonics').Update(disabled=True)
        window.find_element('Time Domain').Update(disabled=True)
        window.find_element('Freq Domain').Update(disabled=True)
        window.find_element('Cumulative Sum').Update(disabled=True)
        window.find_element('Envelope').Update(disabled=True)

        tmp = 'Please select first point on the graph'
        window.find_element('PPM').Update(tmp, text_color=BLUE)
        if (len(xdata) >= 2):
            xdata = []
            ydata = []
        clickEvent = fig_canvas_agg.mpl_connect('button_press_event', onclick)


window.close()
