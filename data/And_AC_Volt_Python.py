import numpy as np
import pandas as pd
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt

def major_function(freq_pert,sec_har_bw,lpf_bw,
    har_num,max_time,max_width,sample_rate,data):

    blank_samples = 4000          #set first samples to zero

    max_index_l = round((max_time - max_width) * sample_rate)
    max_index_u = round((max_time + max_width) * sample_rate)

    nod = len(data.index)                    # Number of data points

    dt = 1/sample_rate           # Distance between the data points
    df = sample_rate/nod         # Sample rate

    n = np.arange(1, nod+1)
    t = n*dt
    f = n*df

    v = data.iloc[:,0].values                   # Column 1: Voltage
    i = data.iloc[:,1].values                   # Column 2: Current

    for x in range(0,blank_samples):
        v[x]=0
        i[x]=0

    Imag = (np.absolute(np.fft.fft(i)/nod*2))  #Magnitude of Current (Abselute value of fourier transform
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

    # Filter size
    n = 2046

    # Low pass cut off
    fc = freq_pert*har_num
    bw = sec_har_bw

    # Full ADC rate
    fs2 = sample_rate/2
    ff = [0.0,((fc-bw)/fs2*0.99), ((fc-bw)/fs2), ((fc+bw)/fs2), ((fc+bw)/fs2*1.01), 1.0]
    m = [0, 0, 1, 1, 0, 0]
    n_freq_in = int(2**(np.ceil(np.log(n)/np.log(2))))
    print(n_freq_in)
    b=sp.signal.firwin2(n+1,ff,m, nfreqs=None, window="hamming", antisymmetric=False)

    c= b/np.max(b)

    w,h = sp.signal.freqz(c,1,worN=10001)
    gain = (np.max(np.absolute(h)))
    c = c/gain
    ifilt = sp.signal.lfilter(c,1,i)
    Imagfilt = (np.abs(np.fft.fft(ifilt)/nod*2))

    #-------------------------------

    i2sin = np.sin(2*np.pi*fc*t)
    i2cosin = np.cos(2*np.pi*fc*t)

    ixsin = ifilt*i2sin
    print(ixsin)
    ixcosin = ifilt*i2cosin

    fc2 = lpf_bw
    ff = [0, fc2/fs2, fc2/fs2*1.01, 1]
    m = [0, 0, 1, 1]
    b = sp.signal.firwin2(n+1,ff,m, nfreqs=None, window="hamming", antisymmetric=False)
    c = b/np.max(b)
    w,h = sp.signal.freqz(c,1,worN=10001)
    gain = (np.max(np.absolute(h)))
    c = c/gain

    ixsin_filt = sp.signal.lfilter(c,1,ixsin)
    ixcosin_filt = sp.signal.lfilter(c,1,ixcosin)

    ienv = 2*np.sqrt(ixsin_filt * ixsin_filt + ixcosin_filt * ixcosin_filt);
    int_ienv = np.cumsum(ienv)

    testmax = 0.0

    for x in range(max_index_l-1,max_index_u):
        if ienv[x]>testmax:
            testmax= ienv[x]

    second_test = 0.0
    for x in range(int(round(nod*0.1))-1,int(round(nod*0.9))):
        if ienv[x]>second_test:
            second_test = ienv[x]
    second_test = testmax / second_test * 100

    print(testmax)
    print(second_test)

    doff = 0

    # Filter ienv
    filter_length = 200
    ienv_filtered = ienv[doff:nod-1]
    ienv_filtered = sp.signal.filtfilt(np.ones(filter_length)/filter_length,1,ienv_filtered);

    return t,i,f,Imag,Imagfilt,ifilt,ienv,int_ienv,ienv


def get_time_values(amps):
    sample_rate = 8000.0
    dt = 1/sample_rate
    nod = len(amps.index)
    n = np.arange(1, nod)
    t = n*dt
    return t
