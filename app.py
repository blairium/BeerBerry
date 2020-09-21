import codecs
import matplotlib

import PySimpleGUI as sg
import pandas as pd
import numpy as np
import peakutils as pk
import matplotlib.pyplot as plt

from os import path
from json import (load as jsonload, dump as jsondump)

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import PolygonSelector
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

# local modules
import file
import maths
from gui import (
    create_main_window,
    create_insert_parameters_window,
    draw_figure,
    destroy_figure,
    load_parameters,
    save_parameters)

# use tkinter
matplotlib.use('TkAgg')


def onclick(event):
    if (len(xdata) < 2):
        xdata.append(event.xdata)
        ydata.append(event.ydata)


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
    'harmonic': 2,
    'max_time': 1.5,
    'max_width': 0.2,
    'sample_rate': 8000.0,
    'theme': sg.theme('BeerBerry')}
# "Map" from the settings dictionary keys to the window's element keys
PARAMETER_KEYS_TO_ELEMENT_KEYS = {
    'freq_pert': '-FREQ PERT-',
    'bandwith_window': '-BW WINDOW-',
    'lpf_bw': '-LPF BW-',
    'harmonic': '-HARMONIC-',
    'max_time': '-MAX TIME-',
    'max_width': '-MAX WIDTH-',
    'sample_rate': '-SAMPLE RATE-',
    'theme': '-THEME-'}


# Initialising empty variables so they can remain within the whole program
# scope
t, i, f, Imag, Imagfilt, ifilt, ienv, int_ienv, ienv_filtered = (
    [] for i in range(9))
harm_one, harm_two, harm_three, harm_four, harm_five = ([] for i in range(5))
fig_canvas_agg = None
df = None
df_Post = None
data = None
password_attempt = None
window, parameters = None, load_parameters(
    PARAMETERS_FILE, DEFAULT_SETTINGS, PARAMETER_KEYS_TO_ELEMENT_KEYS)
xdata = []
ydata = []
clickEvent = None
toolbar = None
print(parameters)
while True:

    if window is None:
        window = create_main_window(parameters, password_attempt, PASSWORD)

    event, values = window.read()
    fname = values['-FILENAME-']

    print(event)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == '-FILENAME-':
        data = file.readFile(fname, 0)
        window.find_element('Load').Update(disabled=False)

    elif event == 'plot' or event == 'r1' or event == 'r2' or event == 'r3' or event == 'r4' or event == 'r5':
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

        fig.suptitle('Selected Harmonics', fontsize=16)
        fig.set_size_inches(9, 6)
        fig.set_dpi(100)
        fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'plot2':
        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg, toolbar)

        window.find_element('Define baseline').Update(disabled=True)
        fig = matplotlib.figure.Figure(figsize=(9, 6), dpi=100)
        fig.add_subplot(
            111,
            xlabel='Time (s)',
            ylabel='Current').plot(
            t,
            i,
            c='#40BAD2')

        fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'Freq vs Mag of Current':
        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg, toolbar)

        window.find_element('Define baseline').Update(disabled=True)

        fig = matplotlib.figure.Figure(figsize=(9, 6), dpi=100)
        fig.add_subplot(111,
                        xlim=(0,
                              int(parameters['freq_pert']) * 10),
                        xlabel='frequency',
                        ylabel='Magnitude of Current').plot(f,
                                                            Imag,
                                                            c='#40BAD2')

        fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'Cumulative Sum':
        if fig_canvas_agg:
            destroy_figure(fig_canvas_agg, toolbar)

        window.find_element('Define baseline').Update(disabled=True)

        fig = matplotlib.figure.Figure(figsize=(9, 6), dpi=100)
        fig.add_subplot(
            111,
            xlabel='Time (s)',
            ylabel='int_ienv').plot(
            t,
            int_ienv,
            c='#40BAD2')

        fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'Load':

        tmp = window['OP1'].get()

        # if default radio button is clicked, returns true for precalc
        if tmp:

            if len(data.columns) == 2:
                # Column 1: Voltage
                v = data.iloc[:, 0].values
                i = data.iloc[:, 1].values

                v, i = maths.blanking_first_samples(4000, v, i)
                f, t = maths.get_time_values(
                    i, float(parameters['sample_rate']))
                Imag = maths.magnitude_of_current(i, i.size)

                window.find_element(
                    'Define baseline').Update(disabled=False)

                harm_one = maths.get_ienv(
                    i, int(
                        parameters['freq_pert']), 1, int(
                        parameters['bandwith_window']), float(
                        parameters['sample_rate']), int(
                        parameters['lpf_bw']), t)
                harm_two = maths.get_ienv(
                    i, int(
                        parameters['freq_pert']), 2, int(
                        parameters['bandwith_window']), float(
                        parameters['sample_rate']), int(
                        parameters['lpf_bw']), t)
                harm_three = maths.get_ienv(
                    i, int(
                        parameters['freq_pert']), 3, int(
                        parameters['bandwith_window']), float(
                        parameters['sample_rate']), int(
                        parameters['lpf_bw']), t)
                harm_four = maths.get_ienv(
                    i, int(
                        parameters['freq_pert']), 4, int(
                        parameters['bandwith_window']), float(
                        parameters['sample_rate']), int(
                        parameters['lpf_bw']), t)
                harm_five = maths.get_ienv(
                    i, int(
                        parameters['freq_pert']), 5, int(
                        parameters['bandwith_window']), float(
                        parameters['sample_rate']), int(
                        parameters['lpf_bw']), t)

                int_ienv = maths.cumulative_sum_ienv(harm_two)
                ienv_filtered = maths.filter_ienv(
                    harm_two, 200)

                if fig_canvas_agg:
                    destroy_figure(fig_canvas_agg, toolbar)

                fig = matplotlib.figure.Figure(
                    figsize=(9, 6), dpi=100)
                fig.add_subplot(
                    111, xlabel='Time (s)', ylabel='Current (S.U)').plot(
                    t, harm_two, c='#40BAD2')
                fig.suptitle('Selected Harmonics', fontsize=16)
                fig_canvas_agg, toolbar = draw_figure(
                    window['-CANVAS-'].TKCanvas, fig)

                window.find_element('plot').Update(disabled=False)
                window.find_element('plot2').Update(disabled=False)
                window.find_element(
                    'Freq vs Mag of Current').Update(disabled=False)
                window.find_element(
                    'Cumulative Sum').Update(disabled=False)

                d = {
                    't': t,
                    'i': i,
                    'f': f,
                    'Imag': Imag,
                    'ienv': harm_two,
                    'int_ienv': int_ienv,
                    'ienv_filtered': ienv_filtered
                }
                df_Post = pd.DataFrame(d)
                if df_Post is not None:
                    window.find_element(
                        'save').Update(disabled=False)

            elif len(data.columns) == 9:
                sg.popup_error(
                    'Error: Select Post Calculation to Load Calculated Data Files')
            else:
                sg.popup_error('Error: Incompatible Data File')
        else:
            df_Post = file.readFile(fname, 1)
            print(df_Post)
            print(len(df_Post.columns))
            if len(df_Post.columns) == 9:
                t = df_Post['t']
                i = df_Post['i']
                f = df_Post['f']
                Imag = df_Post['Imag']
                Imagfilt = df_Post['Imagfilt']
                ifilt = df_Post['ifilt']
                ienv = df_Post['ienv']
                int_ienv = df_Post['int_ienv']
                ienv_filtered = df_Post['ienv_filtered']

                window.find_element('plot').Update(disabled=False)
                window.find_element('plot2').Update(disabled=False)
                window.find_element(
                    'Freq vs Mag of Current').Update(disabled=False)
                window.find_element('Cumulative Sum').Update(disabled=False)

                if df_Post is not None:
                    window.find_element('save').Update(disabled=False)
            elif len(df_Post.columns) == 2:
                sg.popup_error('Error: Select Raw Data to Load Raw Data files')
            else:
                sg.popup_error('Error: Incompatible Data File')

    elif event == 'Record Data':
        data = maths.excitation()
        sg.PopupOK("Recording Complete")
        window.find_element('Load').Update(disabled=False)

    elif event == 'save':

        tmp = window['OP2'].get()
        outFile = values['save']
        if tmp:

            file.writeFile(outFile, data, 0)

        else:

            file.writeFile(outFile, df_Post, 1)

    elif event == 'Define baseline':
        if (len(xdata) >= 2):
            xdata = []
            ydata = []
        clickEvent = fig_canvas_agg.mpl_connect('button_press_event', onclick)
        window.find_element('Map baseline').Update(disabled=False)

    elif event == 'Map baseline':
        copy_t = np.full(np.size(t), xdata[0])
        copy_t = copy_t - t
        copy_t = np.abs(copy_t)
        x_start = np.where(copy_t == (np.min(np.abs(copy_t))))
        xdata[0] = x_start[0][0]
        copy_t = np.full(np.size(t), xdata[1])
        copy_t = copy_t - t
        copy_t = np.abs(copy_t)
        x_end = np.where(copy_t == (np.min(np.abs(copy_t))))
        xdata[1] = x_end[0][0]

        area_under_curve = np.trapz(
            t[xdata[0]:xdata[1]], ienv_filtered[xdata[0]:xdata[1]])
        area_under_baseline = np.trapz(xdata, ydata)
        area_between_curves = area_under_curve - area_under_curve
        curve_1 = np.copy(ienv_filtered)
        curve_2 = np.copy(ienv_filtered)
        curve_2[xdata[0]:xdata[1]] = np.linspace(
            ydata[0], ydata[1], xdata[1] - xdata[0])
        diff_curves = curve_1 - curve_2

        peak_height = np.max(diff_curves)
        index_of_peak = np.where(peak_height == diff_curves)[0][0]
        fig = plt.figure()
        if window['r1'].get():
            plt.plot(t, harm_one, color='b')
            if maths.is_y_valid(t, harm_one, xdata, ydata):
                copy_x_data = np.copy(xdata)
                copy_y_data = np.copy(ydata)
                curve_1, curve_2, peak_height, index_of_peak, diff_curves = maths.map_baseline(
                    t, harm_one, copy_x_data, copy_y_data)
                plt.plot(t, curve_2, color='b')
                plt.plot([t[index_of_peak], t[index_of_peak]], [
                         curve_2[index_of_peak], curve_1[index_of_peak]], color='r')
                plt.fill_between(t, curve_1, curve_2, color='b', alpha=0.3)
        if window['r2'].get():
            plt.plot(t, harm_two, color='#40BAD3')
            if maths.is_y_valid(t, harm_two, xdata, ydata):
                copy_x_data = np.copy(xdata)
                copy_y_data = np.copy(ydata)
                curve_1, curve_2, peak_height, index_of_peak, diff_curves = maths.map_baseline(
                    t, harm_two, copy_x_data, copy_y_data)
                plt.plot(t, curve_2, color='#40BAD3')
                plt.plot([t[index_of_peak], t[index_of_peak]], [
                         curve_2[index_of_peak], curve_1[index_of_peak]], color='r')
                plt.fill_between(
                    t, curve_1, curve_2, color='#40BAD3', alpha=0.3)
        if window['r3'].get():
            plt.plot(t, harm_three, color='orange')
            if maths.is_y_valid(t, harm_three, xdata, ydata):
                copy_x_data = np.copy(xdata)
                copy_y_data = np.copy(ydata)
                curve_1, curve_2, peak_height, index_of_peak, diff_curves = maths.map_baseline(
                    t, harm_three, copy_x_data, copy_y_data)
                plt.plot(t, curve_2, color='orange')
                plt.plot([t[index_of_peak], t[index_of_peak]], [
                         curve_2[index_of_peak], curve_1[index_of_peak]], color='r')
                plt.fill_between(
                    t, curve_1, curve_2, color='orange', alpha=0.3)
        if window['r4'].get():
            plt.plot(t, harm_four, color='g')
            if maths.is_y_valid(t, harm_four, xdata, ydata):
                copy_x_data = np.copy(xdata)
                copy_y_data = np.copy(ydata)
                curve_1, curve_2, peak_height, index_of_peak, diff_curves = maths.map_baseline(
                    t, harm_four, copy_x_data, copy_y_data)
                plt.plot(t, curve_2, color='g')
                plt.plot([t[index_of_peak], t[index_of_peak]], [
                         curve_2[index_of_peak], curve_1[index_of_peak]], color='r')
                plt.fill_between(t, curve_1, curve_2, color='g', alpha=0.3)
        if window['r5'].get():
            plt.plot(t, harm_five, color='y')
            if maths.is_y_valid(t, harm_five, xdata, ydata):
                copy_x_data = np.copy(xdata)
                copy_y_data = np.copy(ydata)
                curve_1, curve_2, peak_height, index_of_peak, diff_curves = maths.map_baseline(
                    t, harm_five, copy_x_data, copy_y_data)
                plt.plot(t, curve_2, color='y')
                plt.plot([t[index_of_peak], t[index_of_peak]], [
                         curve_2[index_of_peak], curve_1[index_of_peak]], color='r')
                plt.fill_between(t, curve_1, curve_2, color='y', alpha=0.3)

        plt.plot(t, curve_1, c='#40BAD3')
        plt.plot(t, curve_2, c='#40BAD3')
        plt.plot([t[index_of_peak], t[index_of_peak]], [
                 curve_2[index_of_peak], curve_1[index_of_peak]], c='r')
        plt.fill_between(t, curve_1, curve_2, alpha=0.3)
        fig.suptitle('Results', fontsize=16)
        fig.set_size_inches(9, 6)
        fig.set_dpi(100)
        destroy_figure(fig_canvas_agg, toolbar)
        fig_canvas_agg, toolbar = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    elif event == 'Log in':
        password_attempt = sg.popup_get_text('Password', '')
        while password_attempt != PASSWORD and password_attempt is not None:
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
        event, values = create_insert_parameters_window(
            parameters, PARAMETER_KEYS_TO_ELEMENT_KEYS).read(
            close=True)
        if event == 'Save':
            window.close()
            window = None
            save_parameters(
                PARAMETERS_FILE,
                parameters,
                values,
                PARAMETER_KEYS_TO_ELEMENT_KEYS)
            fig_canvas_agg = None

window.close()
