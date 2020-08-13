%% AC_Voltammetry
%clc;
%clear;
%close all;

%%

% Data is collected as a sound file (.data). After uploading the file in
% this script, first enter the frequency used during the measurements. The
% uncertainty frequency (� window) is defined next (sec_hr_bw).

% ------------------------------Data Analysis-----------------------------%

y = load('5ppm.data');       % File name in .data format
%testy = load('../atesty.txt');
%testi = load('../atesti.txt');
%testc = load('../atestc.txt');

freq_pert = 60;                % Frequency perturbation
sec_har_bw = 10;                % Band-width window
lpf_bw = 10;                    % env lpf bandwidth
har_num = 2;                    % harmonic to use (normally 2)

blank_samples = 4000;          % set first samples to zero

max_time = 1.5;                % Maximum time
max_width = 0.2;

sample_rate = 8000.0;          % sample rate

max_index_l = round((max_time - max_width) * sample_rate);
max_index_u = round((max_time + max_width) * sample_rate);

a = size(y);                   % Sample size
nod = a(1);                    % Number of data points

dt = 1/sample_rate;            % Distance between the data points
df = sample_rate/nod;          % Sample rate

n = 1:nod;                     % Creating a column vector with

t = n*dt;
f = n*df;

v = y(:,1);                    % Column 1: Voltage
i = y(:,2);                    % Column 2: Current

v(1:blank_samples) = 0;          % blank voltage
i(1:blank_samples) = 0;          % blank current

Imag = ((abs(fft(i)/nod*2)));  % Magnitude of Current (Abselute value of fourier transform

%FFT filtering
% frequency domain
p = fft(i);
%sample position of freq_pert x 2
sample_freq_pert = freq_pert*2/sample_rate*nod;
%sample number of lpf_bw
sample_lpf_bw = sec_har_bw/sample_rate*nod;
%blanking of fft date
p_filtered = p;
p_filtered(1:(sample_freq_pert-sample_lpf_bw/2))=0.0;
p_filtered((sample_freq_pert+sample_lpf_bw/2):(nod-sample_freq_pert-sample_lpf_bw/2))=0.0;
p_filtered((nod-sample_freq_pert+sample_lpf_bw/2):nod)=0.0;
% time domain waveform
p_wave = real(ifft(p_filtered));




% Filter size

n = 2046;

% Display range

d1 = 1;
d2 = 10001;

% Low pass cut off

fc = freq_pert*har_num;
bw = sec_har_bw;

% Full ADC rate

fs2 = sample_rate/2;

ff = [0 (fc-bw)/fs2*0.99 (fc-bw)/fs2 (fc+bw)/fs2 (fc+bw)/fs2*1.01 1]; m = [0 0 1 1 0 0];
b = fir2(n,ff,m);
c = b./max(b);
[h,~] = freqz(c,1,100001);
