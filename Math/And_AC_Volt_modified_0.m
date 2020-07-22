%% AC_Voltammetry
clc;
clear;
close all;

%%

% Data is collected as a sound file (.data). After uploading the file in
% this script, first enter the frequency used during the measurements. The
% uncertainty frequency (± window) is defined next (sec_hr_bw).  

% ------------------------------Data Analysis-----------------------------% 

[file] = uigetfile('*.data'); % opens UI
y = load(file);       % File name in .data format

freq_pert = 60;                % ;Frequency perturbation 
sec_har_bw = 3;                % Band-width window 
lpf_bw = 10;                    % env lpf bandwidth
har_num = 2;                    % harmonic to use (normally 2)

blank_samples = 100;          % set first samples to zero

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


% Filter size

n = 2046;

% Display range

d1 = 001;
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

gain = (max(abs(h)));
c = c/gain;


ifilt = filter(c,1,i);
Imagfilt = ((abs(fft(ifilt)/nod*2)));

i2sin = sin(2*pi*fc.*t)';
i2cosin = cos(2*pi*fc.*t)';

ixsin = ifilt .* i2sin;
ixcosin = ifilt .* i2cosin;



fc2 = lpf_bw;
ff = [0 fc2/fs2 fc2/fs2*1.01 1]; m = [0 0 1 1];
b = fir2(n,ff,m);
c = b./max(b);
[h,w] = freqz(c,1,100001);

gain = (max(abs(h)));
c = c/gain;

ixsin_filt = filter(c,1,ixsin);
ixcosin_filt = filter(c,1,ixcosin);

ienv = 2*sqrt(ixsin_filt .* ixsin_filt + ixcosin_filt .* ixcosin_filt);
int_ienv = cumsum(ienv);

% vfilt = filter(c,1,v);

disp(max(ienv(max_index_l:max_index_u)))
disp(max(ienv(max_index_l:max_index_u)) / max(ienv(round(nod*0.1):round(nod*0.9))) * 100);

doff = 1;

%% Filter ienv (filtfilt = Zero-phase digital filtering)
filter_length = 200;   
ienv_filtered = ienv(doff:nod-doff);
ienv_filtered = filtfilt(ones(filter_length,1)/filter_length,1,ienv_filtered);
%% Figure 1: Plot of Current (S.U) vs. Time (S)
% It is obtained after applying the filter to extract the 2nd Harmonic FT
% of the signal.

figure
subplot(6,1,1), plot(t(doff:nod),i(doff:nod))
title('Raw Data');
subplot(6,1,2), plot(f(1:round(nod/2)),Imag(1:round(nod/2)))
title('Harmonics');
subplot(6,1,3), plot(t(doff:nod),ifilt(doff:nod))
title('Filtered Data'); %I'm not sure about this title
subplot(6,1,4), plot(f(1:round(nod/2)),Imagfilt(1:round(nod/2)))
title('Second Harmonic Only');
subplot(6,1,5), plot(t(doff:nod),ienv(doff:nod))
title('Upper envelope of filtered data');
subplot(6,1,6), plot(t(doff:nod),int_ienv(doff:nod))
title('Integrated Area');

%% ------------------------- Plot Current vs. Time ------------------------%
% Plot filtered version

figure
plot(t(doff:nod),int_ienv(doff:nod),'-r','linewidth',2);
xlabel('Time (s)');
ylabel('Current (S.U)');
title('Integrated Area');
set(gca,'linewidth',2);

figure
plot(t(doff:nod-doff),ienv_filtered,'-r','linewidth',2);
xlabel('Time (s)');
ylabel('Current (S.U)');
title('Upper env of filtered data');
set(gca,'linewidth',2);
hold on

%% ----------------------------------END---------------------------------%%
