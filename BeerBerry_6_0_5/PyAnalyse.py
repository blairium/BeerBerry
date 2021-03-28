'''
This is a python implementation of the matlab script ACVolt written as a class.

To use place a copy of this script in the working directory and import .

i,e. "import PyAnalyse as pa


'''



import numpy as np
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd


class analyse:
    freq_pert = 40;                # Frequency perturbation 
    sec_har_bw = 10;               # Band-width window 
    lpf_bw = 10;                   # env lpf bandwidth
    har_num = 2;                   # harmonic to use (normally 2)

    blank_samples = 8000;          # set first samples to zero

    max_time = 1.5;                # Maximum time
    max_width = 0.2;                 

    sample_rate = 8000.0;          # sample rate

    def __init__(self,filename):
        self.filename = filename
        self.y = pd.read_csv(self.filename, header=0, delimiter=',')







    def analyse(self):

        max_index_l = round((self.max_time - self.max_width) * self.sample_rate);
        max_index_u = round((self.max_time + self.max_width) * self.sample_rate);

        a = self.y.iloc[:,0].size; 
        # Sample size
        nod = a                    # Number of data points

        dt = 1/self.sample_rate;            # Distance between the data points
        df = self.sample_rate/nod;          # Sample rate

        n = np.array(np.linspace(0,nod,nod))                    # Creating a column vector with 

        t = n*dt;
        f = n*df;

        v = self.y.iloc[:, 0].values # Column 1: Voltage
        i = self.y.iloc[:, 1].values # Column 2: Current

        #v[0:blank_samples] = 0;          # blank voltage
        #i[0:blank_samples] = 0;          # blank current

        Imag = ((abs(np.fft.fft(i)/nod*2)));  # Magnitude of Current (Abselute value of fourier transform

        #FFT filtering
        # frequency domain
        p = np.fft.fft(i);

        #sample position of freq_pert x 2
        sample_freq_pert = self.freq_pert*(2/self.sample_rate)*nod;

        #sample number of lpf_bw
        sample_lpf_bw = (self.sec_har_bw/self.sample_rate)*nod;

        #blanking of fft date
        p_filtered = p;
        p_filtered[1:int(sample_freq_pert-(sample_lpf_bw/2))]=0
        p_filtered[int(sample_freq_pert+(sample_lpf_bw/2)):int(nod-sample_freq_pert-(sample_lpf_bw/2))]=0
        p_filtered[int((nod-sample_freq_pert+(sample_lpf_bw/2))):nod]=0
        # time domain waveform
        p_wave = np.real(np.fft.ifft(p_filtered));



        # Filter size

        n = 2046;

        # Display range

        d1 = 1
        d2 = 10001;

        #Low pass cut off

        fc = self.freq_pert*self.har_num;
        bw = self.sec_har_bw;


        #Full ADC rate

        fs2 = self.sample_rate/2;

        ff = [0, ((fc-bw)/fs2)*0.99,(fc-bw)/fs2, (fc+bw)/fs2, ((fc+bw)/(fs2))*1.01, 1];

        m = [0, 0, 1, 1, 0, 0];
        b = sp.signal.firwin2(
            n ,
            ff,
            m,
            nfreqs=None,
            window="hamming",
            antisymmetric=False) #maybe n+1
        c = b / np.max(b)
        w, h = sp.signal.freqz(c, 1, worN=500)
        gain = (np.max(np.absolute(h)))

        c = c / gain
        ifilt = sp.signal.lfilter(c, 1, i)
        Imagfilt = (np.abs(np.fft.fft(ifilt) / nod * 2))



        i2sin = np.sin(2*np.pi*fc*t)
        i2cosin = np.cos(2*np.pi*fc*t)

        ixsin = ifilt * i2sin;
        ixcosin = ifilt * i2cosin;

        fc2 = self.lpf_bw;
        ff = [0, fc2/fs2, (fc2/fs2)*1.01, 1]; 
        m = [0, 0, 1, 1];
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

        ienv = 2*np.sqrt((ixsin_filt * ixsin_filt) + (ixcosin_filt * ixcosin_filt))
        int_ienv = np.cumsum(ienv);



        #disp(max(ienv(max_index_l:max_index_u)))
        #disp(max(ienv(max_index_l:max_index_u)) / max(ienv(round(nod*0.1):round(nod*0.9))) * 100);

        doff = 1;

        ## Filter ienv (filtfilt = Zero-phase digital filtering)
        filter_length = 200;   
        ienv_filtered = ienv[doff:nod-doff];
        ienv_filtered = sp.signal.filtfilt((np.ones(filter_length)/filter_length),1,ienv_filtered);

        x,y  = t[doff:nod-doff],ienv_filtered
        x[0:self.blank_samples]=0
        y[0:self.blank_samples]=0

        return x,y,ienv_filtered, # where x is time and y is current



#a = analyse('FeCOOH_0_2mM_0_2M_PDS_S6_Run1.csv')
#print(a.freq_pert)
#x,y = a.analyse()
#plt.plot(x,y)
#plt.show()