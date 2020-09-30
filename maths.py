import time

import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import sounddevice as sd
import scipy.io.wavfile as wf
import os

from scipy import signal
from datetime import datetime
from scipy import signal
from peakutils import baseline
import ntpath


def blanking_first_samples(blank_samples, v, i):
    for x in range(0, blank_samples):
        v[x] = 0
        i[x] = 0
    return v, i


def magnitude_of_current(i, nod):
    # Magnitude of Current (Absolute value of fourier transform)
    Imag = (np.absolute(np.fft.fft(i) / nod * 2))
    return Imag


def get_ienv(i, freq_pert, harm_num, harm_bandwith, sample_rate, lpf_bw, t):
    # Filter size
    n = 2046
    nod = i.size
    # Low pass cut off
    fc = freq_pert * harm_num
    bw = harm_bandwith

    fs2 = sample_rate / 2
    # Full ADC rate
    if fc == bw:
        ff = [0.0, ((fc + bw) / fs2), ((fc + bw) / fs2 * 1.01), 1.0]
        m = [0, 1, 0, 0]
        n_freq_in = int(2**(np.ceil(np.log(n) / np.log(2))))
        b = sp.signal.firwin2(
            n + 1,
            ff,
            m,
            nfreqs=None,
            window="hamming",
            antisymmetric=False)
    else:
        ff = [
            0.0,
            ((fc - bw) / fs2 * 0.99),
            ((fc - bw) / fs2),
            ((fc + bw) / fs2),
            ((fc + bw) / fs2 * 1.01),
            1.0]
        m = [0, 0, 1, 1, 0, 0]
        n_freq_in = int(2**(np.ceil(np.log(n) / np.log(2))))
        b = sp.signal.firwin2(
            n + 1,
            ff,
            m,
            nfreqs=None,
            window="hamming",
            antisymmetric=False)

    c = b / np.max(b)

    w, h = sp.signal.freqz(c, 1, worN=500)
    gain = (np.max(np.absolute(h)))
    c = c / gain
    ifilt = sp.signal.lfilter(c, 1, i)
    Imagfilt = (np.abs(np.fft.fft(ifilt) / nod * 2))

    # -------------------------------

    i2sin = np.sin(2 * np.pi * fc * t)
    i2cosin = np.cos(2 * np.pi * fc * t)

    ixsin = ifilt * i2sin
    ixcosin = ifilt * i2cosin

    fc2 = lpf_bw
    ff = [0, fc2 / fs2, fc2 / fs2 * 1.01, 1]
    m = [0, 0, 1, 1]
    b = sp.signal.firwin2(
        n + 1,
        ff,
        m,
        nfreqs=None,
        window="hamming",
        antisymmetric=False)
    c = b / np.max(b)
    w, h = sp.signal.freqz(c, 1, worN=500)
    gain = (np.max(np.absolute(h)))
    c = c / gain

    ixsin_filt = sp.signal.lfilter(c, 1, ixsin)
    ixcosin_filt = sp.signal.lfilter(c, 1, ixcosin)

    ienv = 2 * np.sqrt(ixsin_filt * ixsin_filt + ixcosin_filt * ixcosin_filt)
    print("pass")
    return ienv


def cumulative_sum_ienv(ienv):
    int_ienv = np.cumsum(ienv)
    return int_ienv


def filter_ienv(ienv, filter_length):
    #filter_length = 200
    ienv_filtered = np.copy(ienv)
    ienv_filtered = sp.signal.filtfilt(
        np.ones(filter_length) / filter_length, 1, ienv_filtered)
    return ienv_filtered


def get_time_values(amps, sample_rate):
    dt = 1 / float(sample_rate)
    nod = amps.size
    df = sample_rate / nod
    n = np.arange(1, nod + 1)
    t = n * dt
    f = n * df
    return f, t


def map_baseline(t, ienv, xdata, ydata):
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

    xdata = [int(i) for i in xdata]

    area_under_curve = np.trapz(
        t[xdata[0]:xdata[1]], ienv[xdata[0]:xdata[1]])
    area_under_baseline = np.trapz(xdata, ydata)
    area_between_curves = area_under_curve - area_under_curve
    curve_1 = np.copy(ienv)
    curve_2 = np.copy(ienv)
    curve_2[xdata[0]:xdata[1]] = np.linspace(
        ydata[0], ydata[1], xdata[1] - xdata[0])
    diff_curves = curve_1 - curve_2

    peak_height = np.max(diff_curves)
    print(peak_height)
    index_of_peak = np.where(peak_height == diff_curves)[0][0]

    return curve_1, curve_2, peak_height, index_of_peak, diff_curves


def is_y_valid(t, ienv, xdata, ydata):
    print("Checking if y is valid")
    copy_t = np.full(np.size(t), xdata[0])
    copy_t = copy_t - t
    copy_t = np.abs(copy_t)
    x_start = np.where(copy_t == (np.min(np.abs(copy_t))))

    copy_t = np.full(np.size(t), xdata[1])
    copy_t = copy_t - t
    copy_t = np.abs(copy_t)
    x_end = np.where(copy_t == (np.min(np.abs(copy_t))))

    subset = ienv[x_start[0][0]:x_end[0][0]]
    to_compare = np.linspace(
        ydata[0], ydata[1], x_end[0][0] - x_start[0][0])
    valid = -1
    for i in range(x_end[0][0] - x_start[0][0]):
        if subset[i] - to_compare[i] > valid:
            valid = subset[i] - to_compare[i]
    if valid > 0:
        return True
    return False


def excitation(exc_parameters):
    # settings
    # This is as a fraction of the maximum amplitude 1 = 2.96 V
    amplitude = float(exc_parameters['amplitude'])
    stable = float(exc_parameters['stable'])  # stable duration in seconds
    # Doesn't necessarily work for other sample rates
    sample_rate = float(exc_parameters['sample_rate'])
    # recording duration in seconds
    duration = float(exc_parameters['duration'])
    frequency = float(exc_parameters['frequency'])  # Frequency
    # Stable "Voltage" actually a fraction of max output positive values only
    v1 = float(exc_parameters['v1'])
    # Recording Start "Voltage" actually a fraction of max output 0.1 = ~0.045V
    v2 = float(exc_parameters['v2'])
    # Recording stop "Voltage" actually a fraction of max output 1.0 = ~1.265
    v3 = float(exc_parameters['v3'])

    sramp = np.linspace(v1, v1, int(stable * sample_rate)
                        )  # ramp for stable period
    ramp = np.linspace(v2, v3, int(duration * sample_rate)
                       )  # ramp for excitation

    # stable duration
    # Left channel wave form
    xls = np.linspace(0, stable * 2 * np.pi, int(stable * sample_rate))
    # Right Channel waveform
    xrs = np.linspace(0, stable * 2 * np.pi, int(stable * sample_rate))

    s_left_channel = np.sin(frequency * xls) * amplitude
    s_right_channel = np.sin(frequency * xrs + np.pi) * amplitude

    s_left_channel -= sramp
    s_right_channel += sramp

    stable_waveform_stereo = np.vstack(
        (s_left_channel, s_right_channel)).T  # combine left and right channels

    # record duration
    xl = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))
    xr = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))

    left_channel = amplitude * np.sin(frequency * xl)
    right_channel = amplitude * np.sin(frequency * xr + np.pi)

    left_channel -= ramp

    right_channel += ramp

    # combine left and right channels
    waveform_stereo = np.vstack((left_channel, right_channel)).T

    # create total waveform
    total_waveform = (
        np.append(
            stable_waveform_stereo,
            waveform_stereo,
            axis=0))

    # record data
    rec_data = sd.playrec(total_waveform, sample_rate, channels=1)
    time.sleep(stable + duration)
    sd.stop()

    rec = len(rec_data)
    zeroCol = np.zeros(rec, dtype=int)
    df = pd.DataFrame(zeroCol)
    df.insert(loc=1, column=1, value=rec_data)
    blank_samples = 4000
    df.iloc[0:blank_samples, 1] = 0
    return df


def conc(a, b, c, area):
    # conc = (-b + sqrt(b^2-4*a*(c-value)))/(2*a)
    # value = area

    # if conc > (-b/2a) * 0.85
    # High concentration, out of calibration range
    return 0
