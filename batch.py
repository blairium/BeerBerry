import maths
#import app
import file
from gui import (
    create_main_window,
    create_parameters_window,
    draw_figure,
    destroy_figure,
    load_parameters,
    save_parameters,
    create_excitation_parameters_window)
import os
from os import path
rootdir = r'C:\Users\bhaydon\OneDrive - LA TROBE UNIVERSITY\Documents\Beer_Berry_testing\08022021\1.8mM_wash_once_only'#Add the full location of folder where your data is e.g C:\Users\blair\OneDrive - LA TROBE UN
savedir = r'C:\Users\bhaydon\OneDrive - LA TROBE UNIVERSITY\Documents\Beer_Berry_testing\08022021\1.2mM_wash_once'
import time
import pandas as pd

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
    'v3': 0.7,
    'cfact' : -1,
    'name' : 'test'}
# "Map" from the settings dictionary keys to the window's element keys
EXCITATION_KEYS_TO_ELEMENT_KEYS = {
    'amplitude': '-AMPLITUDE-',
    'stable': '-STABLE-',
    'sample_rate': '-EXC SAMPLE RATE-',
    'duration': '-DURATION-',
    'frequency': '-FREQ-',
    'v1': '-V1-',
    'v2': '-V2-',
    'v3': '-V3-',
    'cfact' : '-cfact-'
   # 'name' : '-name-',
    #'autosave' : '-autosave-'
    }

window, parameters, exc_parameters=None, load_parameters(
    PARAMETERS_FILE, DEFAULT_SETTINGS, PARAMETER_KEYS_TO_ELEMENT_KEYS), load_parameters(
    EXCITATION_PARAMETER, EXCITATION_SETTINGS, EXCITATION_KEYS_TO_ELEMENT_KEYS)










for n in range(10):
    print(str(n+1))
    data, volt_range = maths.excitation(exc_parameters)
    n = n + 1
    
    fileName =  '1.2_S7_repeated_without_extra_buffer_wash'+'_run_'+str(n)+'.csv'
    
    #data = pd.Dataframe
    data.to_csv(fileName, index=False, header=True, sep=',')
    print('sleep')
    time.sleep(2)

print('Experiment Complete')