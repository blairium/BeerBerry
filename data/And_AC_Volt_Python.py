import numpy

file_input = open("5ppm.data", "r")


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

a = size(file_input)                   # Sample size
print(a)
nod = a                    # Number of data points
print(nod)

dt = 1/sample_rate           # Distance between the data points
df = sample_rate/nod         # Sample rate

n = []
for x in range(1, nod+1)    # Creating a column vector with
    n[x-1] = x

t = n*dt
print(t)
f = n*df
#
# v = file_input(:,1)                   # Column 1: Voltage
# i = file_input(:,2)                   # Column 2: Current
#
# v(1:blank_samples) = 0         # blank voltage
# i(1:blank_samples) = 0         # blank current
#
#
# Imag = ((abs(fft(i)/nod*2)))  #Magnitude of Current (Abselute value of fourier transform
#
# #FFT filtering
# #frequency domain
# p = fft(i)
# #sample position of freq_pert x 2
# sample_freq_pert = freq_pert*2/sample_rate*nod
# #sample number of lpf_bw
# sample_lpf_bw = sec_har_bw/sample_rate*nod
# #blanking of fft date
# p_filtered = p
# p_filtered(1:(sample_freq_pert-sample_lpf_bw/2))=0.0
# p_filtered((sample_freq_pert+sample_lpf_bw/2):(nod-sample_freq_pert-sample_lpf_bw/2))=0.0
# p_filtered((nod-sample_freq_pert+sample_lpf_bw/2):nod)=0.0
# #time domain waveform
# p_wave = real(ifft(p_filtered));
