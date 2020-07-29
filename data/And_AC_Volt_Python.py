import numpy as np
import pandas as pd

file_input = pd.read_csv("10ppm.data", sep=" ", header=None)


freq_pert = 60               #Frequency perturbation
sec_har_bw = 10              #Band-width window
lpf_bw = 10                   #env lpf bandwidth
har_num = 2                   #harmonic to use (normally 2)

blank_samples = 4000          #set first samples to zero

max_time = 1.5                #Maximum time
max_width = 0.2

sample_rate = 8000.0         #sample rate

max_index_l = round((max_time - max_width) * sample_rate)
max_index_u = round((max_time + max_width) * sample_rate)

nod = len(file_input.index)                    # Number of data points
print(nod)

dt = 1/sample_rate           # Distance between the data points
df = sample_rate/nod         # Sample rate

n = np.arange(1, nod)
print(n)
t = n*dt
print(t)
f = n*df
print(f)

v = file_input.iloc[:,0].values                   # Column 1: Voltage
print(v)
i = file_input.iloc[:,1].values                   # Column 2: Current
print(i)

for x in range(0,blank_samples):
    v[x]=0
    i[x]=0

Imag = (np.absolute(np.fft.fft(i)/nod*2))  #Magnitude of Current (Abselute value of fourier transform
print(Imag)
#FFT filtering
#frequency domain
p = np.fft.fft(i)
#sample position of freq_pert x 2
sample_freq_pert = freq_pert*2/sample_rate*nod
#sample number of lpf_bw
sample_lpf_bw = sec_har_bw/sample_rate*nod
#blanking of fft date
p_filtered = p
p_filtered(1:(sample_freq_pert-sample_lpf_bw/2))=0.0
p_filtered((sample_freq_pert+sample_lpf_bw/2):(nod-sample_freq_pert-sample_lpf_bw/2))=0.0
p_filtered((nod-sample_freq_pert+sample_lpf_bw/2):nod)=0.0
#time domain waveform
p_wave = real(ifft(p_filtered));
