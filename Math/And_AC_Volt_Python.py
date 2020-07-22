
file_input = open("LTUSensorNewTue Sep 10 14-37-32 CE 3.data", "r")


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
