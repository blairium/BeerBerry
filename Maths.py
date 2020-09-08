import numpy as np
import pandas as pd
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt

def blanking_first_samples(blank_samples, v, i):
    for x in range(0,blank_samples):
        v[x]=0
        i[x]=0
    return v, i

def magnitude_of_current(i,nod):
    Imag = (np.absolute(np.fft.fft(i)/nod*2))  #Magnitude of Current (Absolute value of fourier transform)
    return Imag

def get_ienv(i, freq_pert, harm_num, harm_bandwith, sample_rate, lpf_bw):
    # Filter size
    n = 2046

    # Low pass cut off
    fc = freq_pert*har_num
    bw = harm_bandwith

    # Full ADC rate
    fs2 = sample_rate/2
    ff = [0.0,((fc-bw)/fs2*0.99), ((fc-bw)/fs2), ((fc+bw)/fs2), ((fc+bw)/fs2*1.01), 1.0]
    m = [0, 0, 1, 1, 0, 0]
    n_freq_in = int(2**(np.ceil(np.log(n)/np.log(2))))
    b=sp.signal.firwin2(n+1,ff,m, nfreqs=None, window="hamming", antisymmetric=False)

    c= b/np.max(b)

    w,h = sp.signal.freqz(c,1,worN=500)
    gain = (np.max(np.absolute(h)))
    c = c/gain
    ifilt = sp.signal.lfilter(c,1,i)
    Imagfilt = (np.abs(np.fft.fft(ifilt)/nod*2))

    #-------------------------------

    i2sin = np.sin(2*np.pi*fc*t)
    i2cosin = np.cos(2*np.pi*fc*t)

    ixsin = ifilt*i2sin
    ixcosin = ifilt*i2cosin

    fc2 = lpf_bw
    ff = [0, fc2/fs2, fc2/fs2*1.01, 1]
    m = [0, 0, 1, 1]
    b = sp.signal.firwin2(n+1,ff,m, nfreqs=None, window="hamming", antisymmetric=False)
    c = b/np.max(b)
    w,h = sp.signal.freqz(c,1,worN=500)
    gain = (np.max(np.absolute(h)))
    c = c/gain

    ixsin_filt = sp.signal.lfilter(c,1,ixsin)
    ixcosin_filt = sp.signal.lfilter(c,1,ixcosin)

    ienv = 2*np.sqrt(ixsin_filt * ixsin_filt + ixcosin_filt * ixcosin_filt)

    return ienv

def cumulative_sum_ienv(ienv):
    int_ienv = np.cumsum(ienv)
    return int_ienv


def filter_ienv(ienv, filter_length):
    #filter_length = 200
    ienv_filtered = np.copy(ienv)
    ienv_filtered = sp.signal.filtfilt(np.ones(filter_length)/filter_length,1,ienv_filtered)
    return ienv_filtered

def get_time_values(amps, sample_rate):
    dt = 1/float(sample_rate)
    nod = len(amps.index)
    df = sample_rate/nod
    n = np.arange(1, nod+1)
    t = n*dt
    f = n*df
    return f,t

#FFT filtering
#frequency domain
# p = np.fft.fft(i)
# #sample position of freq_pert x 2
# sample_freq_pert = freq_pert*2/sample_rate*nod
# #sample number of lpf_bw
# sample_lpf_bw = sec_har_bw/sample_rate*nod
# #blanking of fft date
# p_filtered = p
#
# for x in range(0,int(sample_freq_pert-sample_lpf_bw/2)):
#     p_filtered[x]=0.0
#
# for x in range(int((sample_freq_pert+sample_lpf_bw/2)-1),int(nod-sample_freq_pert-sample_lpf_bw/2)):
#     p_filtered[x]=0.0
#
# for x in range(int((nod-sample_freq_pert+sample_lpf_bw/2)-1),nod):
#     p_filtered[x]=0.0
#
# #time domain waveform
# p_wave = np.fft.ifft(p_filtered)
# p_wave = p_wave.real
