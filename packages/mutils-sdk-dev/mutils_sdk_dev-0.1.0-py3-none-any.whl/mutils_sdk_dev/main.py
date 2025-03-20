# 1
"""
clc;

% Define signal parameters
fs = 1000;                  % Sampling frequency (Hz)
t = 0:1/fs:1-1/fs;          % Time vector (1-second duration)

% Define frequencies of signal components
f1 = 50; 
f2 = 150; 

% Generate original signal (sum of two sine waves)
x_org = sin(2*pi*f1*t) + sin(2*pi*f2*t);

% Add Gaussian noise to the original signal
noise_amplitude = 0.5; 
noise = noise_amplitude * randn(size(t));
x_noisy = x_org + noise;

% Plot original and noisy signals in time domain
figure;
subplot(2,1,1); plot(t, x_org, 'r'); grid on;
title('Original Signal (Time Domain)'); xlabel('Time (s)'); ylabel('Amplitude');
subplot(2,1,2); plot(t, x_noisy, 'b'); grid on;
title('Noisy Signal (Time Domain)'); xlabel('Time (s)'); ylabel('Amplitude');

% FIR High-Pass Filtering
cutoff_freq = 100;          % Cutoff frequency in Hz
order = 50;                 % FIR filter order

% Design FIR high-pass filter using window method
b_fir = fir1(order, cutoff_freq/(fs/2), 'high');

% Apply FIR filter to noisy signal
x_filtered_fir = filter(b_fir, 1, x_noisy);

% Plot FIR filtering results
figure;
subplot(3,1,1); plot(t, x_org, 'r'); grid on;
title('Original Signal (Time Domain)'); xlabel('Time (s)'); ylabel('Amplitude');
subplot(3,1,2); plot(t, x_noisy, 'b'); grid on;
title('Noisy Signal (Time Domain)'); xlabel('Time (s)'); ylabel('Amplitude');
subplot(3,1,3); plot(t, x_filtered_fir, 'g'); grid on;
title('Filtered Signal with FIR High-Pass Filter (Time Domain)'); 
xlabel('Time (s)'); ylabel('Amplitude');

% Display frequency response of FIR filter
figure;
freqz(b_fir, 1, 1024, fs);
title('Frequency Response of the FIR High-Pass Filter');

% IIR High-Pass Filtering using Butterworth filter
[b_iir, a_iir] = butter(4, cutoff_freq/(fs/2), 'high');

% Apply IIR filter to noisy signal
x_filtered_iir = filter(b_iir, a_iir, x_noisy);

% Plot IIR filtering results
figure;
subplot(3,1,1); plot(t, x_org, 'r'); grid on;
title('Original Signal (Time Domain)'); xlabel('Time (s)'); ylabel('Amplitude');
subplot(3,1,2); plot(t, x_noisy, 'b'); grid on;
title('Noisy Signal (Time Domain)'); xlabel('Time (s)'); ylabel('Amplitude');
subplot(3,1,3); plot(t, x_filtered_iir, 'm'); grid on;
title('Filtered Signal with IIR High-Pass Filter (Time Domain)'); 
xlabel('Time (s)'); ylabel('Amplitude');

% Display frequency response of IIR filter
figure;
freqz(b_iir, a_iir, 1024, fs);
title('Frequency Response of the IIR High-Pass Filter');

% Frequency domain analysis using FFT
X_org = abs(fft(x_org));
X_noisy = abs(fft(x_noisy));
X_filtered_fir = abs(fft(x_filtered_fir));
X_filtered_iir = abs(fft(x_filtered_iir));

% Frequency vector
f = (0:length(t)-1) * fs / length(t);

% Plot signals in frequency domain
figure;
subplot(4,1,1); plot(f, X_org, 'r'); grid on;
title('Original Signal (Frequency Domain)'); xlabel('Frequency (Hz)'); ylabel('Magnitude');
subplot(4,1,2); plot(f, X_noisy, 'b'); grid on;
title('Noisy Signal (Frequency Domain)'); xlabel('Frequency (Hz)'); ylabel('Magnitude');
subplot(4,1,3); plot(f, X_filtered_fir, 'g'); grid on;
title('Filtered Signal with FIR High-Pass Filter (Frequency Domain)');
xlabel('Frequency (Hz)'); ylabel('Magnitude');
subplot(4,1,4); plot(f, X_filtered_iir, 'm'); grid on;
title('Filtered Signal with IIR High-Pass Filter (Frequency Domain)');
xlabel('Frequency (Hz)'); ylabel('Magnitude');
"""

#1.2
"""
fs = 1000; % Sampling frequency (Hz)
t = 0:1/fs:1; % Time vector (1 second duration)
f = 5; % Signal frequency in Hz
x = sin(2*pi*f*t); % Sinusoidal signal

figure;
plot(t, x);
xlabel('Time (s)');
ylabel('Amplitude');
title('Sinusoidal Signal');
grid on;

%1.2 Genertating basic signals

f = 5; % Frequency of the square wave
sq_wave = square(2 * pi * f * t);

figure;
plot(t, sq_wave);
xlabel('Time (s)');
ylabel('Amplitude');
title('Square Wave Signal');
grid on;


%2 Samplig and Aliasing
f_signal = 10; % Signal frequency
fs_low = 15; % Low sampling rate (below Nyquist rate)
fs_high = 50; % High sampling rate

t_low = 0:1/fs_low:1;
t_high = 0:1/fs_high:1;

x_low = sin(2*pi*f_signal*t_low);
x_high = sin(2*pi*f_signal*t_high);

figure;
subplot(2,1,1);
stem(t_low, x_low, 'r'); hold on;
plot(t_high, x_high, 'b');
xlabel('Time (s)'); ylabel('Amplitude');
title('Aliasing Effect (Red: Low Sampling, Blue: Original Signal)');
legend('Low Sampling', 'High Sampling');
grid on;

%checking on square wave 

f_signal = 10; % Signal frequency
fs_low = 15; % Low sampling rate (below Nyquist rate)
fs_high = 150; % High sampling rate

t_low = 0:1/fs_low:1;
t_high = 0:1/fs_high:1;

x_low = square(2*pi*f_signal*t_low);
x_high = square(2*pi*f_signal*t_high);

subplot(2,1,2);
stem(t_low, x_low, 'r'); hold on;
plot(t_high, x_high, 'b');
xlabel('Time (s)'); ylabel('Amplitude');
title('Aliasing Effect (Red: Low Sampling, Blue: Original Signal)');
legend('Low Sampling', 'High Sampling');
grid on;

%fft 
N = length(x);
X = fft(x);
f_axis = linspace(-fs/2, fs/2, N);

figure;
plot(f_axis, abs(fftshift(X)));
xlabel('Frequency (Hz)');
ylabel('Magnitude');
title('Frequency Spectrum of the Signal');
grid on;
"""

#2
"""
clf; clc; clear

N = 51;
noise = 0.8*(rand(N,1) - 0.5); % Generate random noise

m = 0:N-1;
s = 2*m.*(0.9.^m); % Generate uncorrupted signal
x = s + noise'; % Generate noise corrupted signal

subplot(2,1,1);
plot(m,noise','r-',m,s,'g--',m, x,'b-.');
title("Before filtering");
xlabel('Time index n');ylabel('Amplitude');
legend('Noise','Original','Noisy');
x1 = [0 0 x];x2 = [0 x 0];x3 = [x 0 0];
y = (x1 + x2 + x3)/3;
subplot(2,1,2);
plot(m,y(2:N+1),'r-',m,s,'g--');
legend('Filtered','Original');
title("After filtering");
xlabel('Time index n');ylabel('Amplitude');

% Simulation of an M-point Moving Average Filter
% Generate the input signal
n = 0:100;
s1 = cos(2*pi*0.05*n); % A low frequency sinusoid
s2 = cos(2*pi*0.47*n); % A high frequency sinusoid
x = s1+s2;
% Implementation of the moving average filter
M = input('Desired length of the filter = ');
num = ones(1,M);
y = filter(num,1,x)/M;
% Display the input and output signals
clf;
subplot(2,2,1);
plot(n,s1);
axis([0, 100, -2, 2]);
xlabel('Time index n'); ylabel('Amplitude');
title('Signal # 1');
subplot(2,2,2);
plot(n,s2);
axis([0, 100, -2, 2]);
xlabel('Time index n'); ylabel('Amplitude');
title('Signal # 2');
subplot(2,2,3);
plot(n,x);
axis([0, 100, -2, 2]);
xlabel('Time index n'); ylabel('Amplitude');
title('Input Signal');
subplot(2,2,4);
plot(n,y);
axis([0, 100, -2, 2]);
xlabel('Time index n'); ylabel('Amplitude');
title('Output Signal');
axis;

figure;

X = abs(fft(x));
Y = abs(fft(y));
subplot(2, 1, 1); plot(X(1:51)); title('Magnitude of input signal)'); grid on;
subplot(2, 1, 2); plot(Y(1:51)); title('Magnitude of input signal)'); grid on;
"""

#3
"""

clc;
clear;
close all;

x = -50:0.1:50;
ft_values = [0.1, 0.25, 0.4];

figure;
hold on;
for ft = ft_values
    h = sin(2 * pi * ft * x)./(pi * x);
    plot(x, h, 'LineWidth', 1.5, 'DisplayName', sprintf('f_t = %.2f', ft));
end
hold off;

% Customize plot
xlabel('Samples (n)');
ylabel('Amplitude');
title('Impulse Response of Ideal Low-Pass Filter');
legend show;
grid on;


clc;
clear;
close all;

Fs = 2000;
Fc = 460;
M = 20;
N = M + 1;
ft = Fc / Fs;

n = 0:M;
w_lpf = sin(2*pi*ft*(n-M/2))./(pi*(n-M/2));
w_lpf(M/2+1) = 2*ft;

subplot(3, 1, 1); stem(n, w_lpf, 'r', 'LineWidth', 1.5); grid on;
title("Truncated, shifted sinc function")

[H, w] = freqz(w_lpf, 1, 1024, Fs);
subplot(3, 1, 2); plot(w, abs(H), 'r', 'LineWidth', 1.5);
title("Frequency response"); grid on;

subplot(3, 1, 3); plot(w, 20*log10(abs(H)), 'b', 'LineWidth', 1.5);
title("Frequency response (dB)"); grid on;

clc;
clear;
close all;

Fs = 2000;
Fc = 460;
M = 100;
N = M + 1;
ft = Fc / Fs;

n = 0:M;
w_lpf = sin(2*pi*ft*(n-M/2))./(pi*(n-M/2));
w_lpf(M/2+1) = 2*ft;

w_n = 0.54-0.46*cos(2*pi*n/M);
h_n = w_lpf.*w_n;

subplot(3, 1, 1); stem(n, w_lpf, 'LineWidth', 1.5); grid on;
xlabel('Weight number, (n)'); ylabel('Weight Value, w(n)');
title("Truncated, shifted sinc function")

subplot(3, 1, 2); stem(n, w_n, 'LineWidth', 1.5); grid on;
xlabel('Weight number, (n)'); ylabel('Weight Value, w(n)');
title("Hamming Window")

subplot(3, 1, 3); stem(n, h_n, 'LineWidth', 1.5); grid on;
xlabel('Weight number, (n)'); ylabel('Weight Value, w(n)');
title("Product of them")

[H_rect, w_rect] = freqz(w_lpf, 1, 1024, Fs);
[H_hamming, w_hamming] = freqz(h_n, 1, 1024, Fs);

figure
subplot(2, 1, 1); plot( ...
    w_rect, abs(H_rect), 'g', ...
    w_hamming, abs(H_hamming), 'r', 'LineWidth', 1.5);
title("Frequency response"); grid on;

subplot(2, 1, 2); plot( ...
    w_rect, 20*log10(abs(H_rect)), 'g', ...
    w_hamming, 20*log10(abs(H_hamming)), 'r', 'LineWidth', 1.5);
title("Frequency response (dB)"); grid on;


clc;
clear;
close all;

Fs = 44100;
Fc = 5000;
M = 28;
N = M + 1;
ft = Fc / Fs;

n = 0:M;
w_lpf = sin(2*pi*ft*(n-M/2))./(pi*(n-M/2));
w_lpf(M/2+1) = 2*ft;

rectangular = ones(1, N);
[H_rect, w_rect] = freqz(w_lpf.*rectangular, 1, 1024, Fs);

bartlett = 1-2*abs(n-M/2)/M;
[H_br, w_br] = freqz(w_lpf.*bartlett, 1, 1024, Fs);

hanning = 0.5-0.5*cos(2*pi*n/M);
[H_hanning, w_hanning] = freqz(w_lpf.*hanning, 1, 1024, Fs);

hamming = 0.54-0.46*cos(2*pi*n/M);
[H_hamming, w_hamming] = freqz(w_lpf.*hamming, 1, 1024, Fs);

blackman = 0.42 - 0.5*cos(2*pi*n/M)+0.08*cos(4*pi*n/M);
[H_blackman, w_blackman] = freqz(w_lpf.*blackman, 1, 1024, Fs);

subplot(2, 1, 1);
hold on;
plot(w_rect, 20*log10(abs(H_rect)), 'DisplayName', 'Rectangular');
plot(w_br, 20*log10(abs(H_br)), 'DisplayName', 'Bartlett');
plot(w_hanning, 20*log10(abs(H_hanning)), 'DisplayName', 'Hanning');
plot(w_hamming, 20*log10(abs(H_hamming)), 'DisplayName', 'Hamming');
plot(w_blackman, 20*log10(abs(H_blackman)), 'DisplayName', 'Blackman');
hold off;
xlabel('Frequency (Hz)'); ylabel('Magnitude (dB)');
title('Frequency Response');
legend show; grid on;

subplot(2, 1, 2);
hold on;
plot(n, rectangular, 'DisplayName', 'Rectangular');
plot(n, bartlett, 'DisplayName', 'Bartlett');
plot(n, hanning, 'DisplayName', 'Hanning');
plot(n, hamming, 'DisplayName', 'Hamming');
plot(n, blackman, 'DisplayName', 'Blackman');
hold off;
xlabel('Weight number, (n)'); ylabel('Weight Value, w(n)');
title('Impulse Response');
legend show; grid on;

clc;
clear;
close all;

Fs = 40000;
Fc = 10000;
M = 100;
N = M + 1;
ft = Fc / Fs;

n = 0:M;
w_lpf = sin(2*pi*ft*(n-M/2))./(pi*(n-M/2));
w_lpf(M/2+1) = 2*ft;

all_pass = zeros(1, N);
all_pass(M/2+1) = 1;

w_hpf = all_pass - w_lpf;

hamming = 0.54-0.46*cos(2*pi*n/M);

[H_lpf_hamming, w_lpf_hamming] = freqz(w_lpf.*hamming, 1, 1024, Fs);
[H_hpf_hamming, w_hpf_hamming] = freqz(w_hpf.*hamming, 1, 1024, Fs);

hold on;
plot(w_lpf_hamming, 20*log10(abs(H_lpf_hamming)), 'r', 'DisplayName', 'Low Pass hamming');
plot(w_hpf_hamming, 20*log10(abs(H_hpf_hamming)), 'g', 'DisplayName', 'High Pass Hamming');
hold off;
xlabel('Frequency (Hz)'); ylabel('Magnitude (dB)');
title('Frequency Response');
legend show; grid on;


clc;
clear;
close all;

Fs = 30000;
M = 200;
N = M + 1;

Fc_1 = 5000;
Fc_2 = 10000;
ft_1 = Fc_1 / Fs;
ft_2 = Fc_2 / Fs;

n = 0:M;

w_bp = sin(2*pi*ft_2*(n-M/2))./(pi*(n-M/2))-sin(2*pi*ft_1*(n-M/2))./(pi*(n-M/2));
w_bp(M/2+1) = 2*(ft_2-ft_1);

w_bs = sin(2*pi*ft_1*(n-M/2))./(pi*(n-M/2))-sin(2*pi*ft_2*(n-M/2))./(pi*(n-M/2));
w_bs(M/2+1) = 1-2*(ft_2-ft_1);

hamming = 0.54-0.46*cos(2*pi*n/M);

[H_bp_hamming, w_bp_hamming] = freqz(w_bp.*hamming, 1, 1024, Fs);
[H_bs_hamming, w_bs_hamming] = freqz(w_bs.*hamming, 1, 1024, Fs);

hold on;
plot(w_bp_hamming, 20*log10(abs(H_bp_hamming)), 'r', 'DisplayName', 'Band Pass hamming');
plot(w_bs_hamming, 20*log10(abs(H_bs_hamming)), 'g', 'DisplayName', 'Band Stop Hamming');
hold off;
xlabel('Frequency (Hz)'); ylabel('Magnitude (dB)');
title('Frequency Response');
legend show; grid on;

"""

#4
"""
clc; clear; close all;

N = 513; % Total number of frequency samples
f = linspace(0, 0.5, N); % Frequency axis

H = zeros(1, N);
H(1:128) = -16*f(1:128) + 3; % Linear function
% 129:257 Zeros
H(258:385) = 1; % Ones
H(386:513) = sin(2*pi*0.017*(1:128)) + 1; % Sine wave

figure;

% First plot - Desired Frequency Response
subplot(2,1,1); % 2 rows, 1 column, first plot
plot(f, H, 'LineWidth', 1.5);
xlabel('Normalized Frequency');
ylabel('Magnitude');
title('Desired Frequency Response');
grid on;

% Compute IFFT
f = ifft(H, 1024);

% Second plot - Impulse Response from IFFT
subplot(2,1,2); % 2 rows, 1 column, second plot
plot(0:1023, f, 'LineWidth', 1.5);
xlabel('Sample Index');
ylabel('Magnitude');
title('Impulse Response from IFFT');
grid on;


M = 1000;
N = M+1;

for i=0:M/2-1
    ft(M/2-i)=f(1024-i);
end

ft = [ft(1:M/2), f(1:M/2+1), zeros(1, 1024-N)];

figure;
subplot(3,1,1);
stem(1:N, abs(ft(1:N))); grid on;
title('Shifted and Truncated');

w = 0.54-0.46*cos(2*pi*(0:M)/(M));
h = w.*ft(1:N);

subplot(3,1,2);
stem(1:N, abs(h)); grid on;
title('Windowed Impulse Response');

H = fft(h, 1024);

subplot(3,1,3);
plot((0:512)/1024, abs(H(1:513)));
grid on;
title('Obtained Frequency Response');
"""

#5
"""
x=0:.01:20;
y=zeros(size(x));  
y(900:1100)=1;                      % Create a rectangular function y, 200 points wide  
y=y+.01.*randn(size(y));             % Noise added before the convolution  

c=exp(- (1:length(y)) ./150);        % Exponential trailing convolution function, c  
yc=conv(y,c,'full')./sum(c);         % Create exponential trailing rectangular function, yc  

yc=yc+.01.*randn(size(yc));          % Noise added after the convolution  

ydc=deconv(yc, c).*sum(c);            % Attempt to recover y by deconvoluting c from yc  

% Plot all the steps  
subplot(2,2,1);  
plot(x,y);  
title('original y');  

subplot(2,2,2);  
plot(x,c);  
title('c');  

subplot(2,2,3);  
plot(x,yc(1:2001));  
title('yc');  

subplot(2,2,4);  
plot(x, ydc);  
title('recovered y');


function g = gaussian(x, mu, sigma)
    g = exp(-((x - mu).^2) / (2 * sigma^2));
end

function SmoothY = fastsmooth(Y, w, type, ends)
    % Fast smoothing function
    if nargin == 2, ends = 0; type = 1; end
    if nargin == 3, ends = 0; end
    
    switch type
        case 1
            SmoothY = sa(Y, w, ends);
        case 2
            SmoothY = sa(sa(Y, w, ends), w, ends);
        case 3
            SmoothY = sa(sa(sa(Y, w, ends), w, ends), w, ends);
        case 4
            SmoothY = sa(sa(sa(sa(Y, w, ends), w, ends), w, ends), w, ends);
        case 5
            SmoothY = sa(sa(sa(sa(Y, round(1.6*w), ends), round(1.4*w), ends), round(1.2*w), ends), w, ends);
    end
end

function SmoothY = sa(Y, smoothwidth, ends)
    w = round(smoothwidth);
    SumPoints = sum(Y(1:w));
    s = zeros(size(Y));
    halfw = round(w/2);
    L = length(Y);
    
    for k = 1:L-w
        s(k+halfw-1) = SumPoints;
        SumPoints = SumPoints - Y(k) + Y(k+w);
    end
    s(k+halfw) = sum(Y(L-w+1:L));
    SmoothY = s./w;

    % Taper the ends of the signal if ends=1.
    if ends == 1
        startpoint = (smoothwidth + 1)/2;
        SmoothY(1) = (Y(1) + Y(2)) / 2;
        for k = 2:startpoint
            SmoothY(k) = mean(Y(1:(2*k-1)));
            SmoothY(L-k+1) = mean(Y(L-2*k+2:L));
        end
        SmoothY(L) = (Y(L) + Y(L-1)) / 2;
    end
end

% Demonstration of Gaussian convolution and deconvolution.
% Requires Gaussian, fastsmooth functions
% Create a rectangular function y, 400 points wide
increment=.01;
cw=2; % cw = Convolution width of the physical convolution process (unknown)
dw=2.01; % dw = Deconvolution width (estimated) must equal cw for perfect results
SmoothWidth=4; % Width of final smoothing to remove high-frequency noise

% Create simulated signal
x=0:increment:20;
y=zeros(size(x));
y(900:1300)=1.3;
% Add pre-convolution random noise
y=y+.01.*randn(size(y)); % Noise added before the convolution
% Create a centered Gaussian convolution function (maximum at x=zero)
c=gaussian(x,0,cw)+gaussian(x,max(x),cw); % zero centered Gaussian convolution function
c2=gaussian(x,0,dw)+gaussian(x,max(x),dw); % zero centered Gaussian deconvolution function
% Convolute rectangular function with Gaussian
yc=ifft(fft(y).*fft(c))./sum(c); % Create Gaussian convoluted rectangular function
% Add a little bit of post-convolution random noise
yc=yc+.00000001.*randn(size(yc)); % Noise added after the convolution
% Now attempt to recover the original signal by deconvolution (2 methods)
ydc=ifft(fft(yc)./fft(c2)).*sum(c2); % Deconvolution by fft/ifft
% ydc=deconvgauss(x,yc,w); % Deconvolution by "deconvgauss" function
% Plot all the steps
subplot(2,2,1); plot(x,y); title('original y');
%subplot(2,2,2); plot(x,c);title('Convolution function, c');
subplot(2,2,2); plot(x,yc(1:2001)); title(['yc=y convoluted with c.Width = ' num2str(cw) ]);
subplot(2,2,3); plot(x,ydc);title(['ydc=recovered y. Width = ' num2str(dw) ]);
subplot(2,2,4); plot(x,fastsmooth(ydc,SmoothWidth,3));title('smoothed recovered y');
"""


#6
"""
clc;
clear all;
fc = 20;
fs = 750;
x = exp(-2*pi*fc/fs);
a = 1-x;
b = x;
delta = [1,zeros(1,1023)];
y(1) = a * delta(1);
for i=2:length(delta)
    y(i) = a*delta(i) + b*y(i-1);
end
H1 = fft(y);
subplot(2,2,1); plot((1:100), y(1:100));title('Impulse Response (1st order)'); grid on;
subplot(2,2,2); plot((1:512)/1024, abs(H1(1:512))); title("Frequency response (1st order)"); grid on;
z(1) = a*y(1);
for i=2:length(delta)
    z(i) = a*y(i)+ b*z(i-1);
end
H2 = fft(z);
subplot(2,2,3); plot((1:100), z(1:100));title('Impulse Response (2nd order)'); grid on;
subplot(2,2,4); plot((1:512)/1024, abs(H2(1:512))); title("Frequency response (2nd order)"); grid on;
f1=15; f2=150;
t = linspace(0,1,100);
x_noisy=sin(2*pi*f1*t)+sin(2*pi*f2*t);
x(1) = a*x_noisy(1);
for i = 2:length(x_noisy)
    x(i) = a*x_noisy(i) + b*x(i-1);
end
figure;
subplot(3,1,1); plot(1:length(x), x_noisy);
title(['Noisy Signal (f1=', num2str(f1), ' Hz, f2=', num2str(f2), ' Hz)']);  grid on;
subplot(3,1,2); plot(1:length(x), x); title("Filtered signal (1st order)"); grid on;
x_2(1)=a*x(1);
for i=2:length(x)
    x_2(i)=a*x(i)+b*x_2(i-1);
end
subplot(3,1,3); plot(1:length(x_2),x_2); title("Filtered signal (2nd order)");


clc; clear; close all;

fs = 24000;
fc1 = 1600; fc2 = 5000; %cutoff freq

f = (fc1 + fc2)/fs; %centered freq
BW = (fc2 - fc1)/fs; %bandwith

R = 1-3*BW;
X = (1-2*R*cos(2*pi*f)+R^2)/(2-2*cos(2*pi*f));
a0 = 1-X;
a1 = 2*(X-R)*cos(2*pi*f);
a2 = R^2 - X;
b1 = 2*R*cos(2*pi*f);
b2 = -R^2;

delta =[1,zeros(1,200)];
h(1)=a0*delta(1);
h(2) = a0 *delta(2) + a1*delta(1)+b1*h(1);

for i = 3:length(delta)
    h(i) = a0*delta(i) + a1*delta(i-1) + a2*delta(i-2) + b1* h(i-1) + b2* h(i-2);
end

H = fft(h);
subplot(3,2,1); plot(1:200,h(1:200)); title("Impulse response of II"); grid on;
subplot(3,2,2); plot(1:100,abs(H(1:100))); title("Frequency response of II");grid on;

%4th order pass-band IIR filter
y(1)=a0*h(1);
y(2)=a0*h(2)+a1*h(1)+b1*y(1);
for i=3:length(h)
y(i)=a0*h(i)+a1*h(i-1)+a2*h(i-2)+b1*y(i-1)+b2*y(i-2);
end

Y=fft(y);
subplot(3,2,3);plot(1:100,y(1:100));title('Impulse response of IIII');grid on;
subplot(3,2,4);plot(1:100,abs(Y(1:100)));title('Frequency response of IIII');grid on;

t=linspace(0,1,100);
x_noisy=sin(2*pi*300*t)+sin(2*pi*2500*t);
x_filtered=conv(x_noisy,y);
subplot(3,2,5);plot(1:length(x_noisy),x_noisy);title('Noisy Signal');grid on;
subplot(3,2,6);plot(1:100,x_filtered(1:100));title('After filtering');grid on;

syms z
num = [a0, a1, a2];
den = [1, -b1, -b2];

% Create symbolic H(z)
H_sym = (num(1) + num(2)*z^(-1) + num(3)*z^(-2)) / ...
        (den(1) + den(2)*z^(-1) + den(3)*z^(-2));


clc; clear; close all;

fs = 24000;
fc1 = 1600; fc2 = 5000; %cutoff freq

f = (fc1 + fc2)/fs; %centered freq
BW = (fc2 - fc1)/fs; %bandwith

R = 1-3*BW;
X = (1-2*R*cos(2*pi*f)+R^2)/(2-2*cos(2*pi*f));
a0 = X;
a1 = -2*X*cos(2*pi*f);
a2 = X;
b1 = 2*R*cos(2*pi*f);
b2 = -R^2;

delta =[1,zeros(1,200)];
h(1)=a0*delta(1);
h(2) = a0 *delta(2) + a1*delta(1)+b1*h(1);

for i = 3:length(delta)
    h(i) = a0*delta(i) + a1*delta(i-1) + a2*delta(i-2) + b1* h(i-1) + b2* h(i-2);
end

H = fft(h);
subplot(3,2,1); plot(1:200,h(1:200)); title("Impulse response of II"); grid on;
subplot(3,2,2); plot(1:100,abs(H(1:100))); title("Frequency response of II");grid on;

%4th order pass-band IIR filter
y(1)=a0*h(1);
y(2)=a0*h(2)+a1*h(1)+b1*y(1);
for i=3:length(h)
y(i)=a0*h(i)+a1*h(i-1)+a2*h(i-2)+b1*y(i-1)+b2*y(i-2);
end

Y=fft(y);
subplot(3,2,3);plot(1:100,y(1:100));title('Impulse response of IIII');grid on;
subplot(3,2,4);plot(1:100,abs(Y(1:100)));title('Frequency response of IIII');grid on;

t=linspace(0,1,100);
x_noisy=sin(2*pi*300*t)+sin(2*pi*2500*t);
x_filtered=conv(x_noisy,y);
subplot(3,2,5);plot(1:length(x_noisy),x_noisy);title('Noisy Signal');grid on;
subplot(3,2,6);plot(1:100,x_filtered(1:100));title('After filtering');grid on;

syms z
num = [a0, a1, a2];
den = [1, -b1, -b2];

% Create symbolic H(z)
H_sym = (num(1) + num(2)*z^(-1) + num(3)*z^(-2)) / ...
        (den(1) + den(2)*z^(-1) + den(3)*z^(-2));
"""


#7
"""
clc; clear; close all;

n = 2;              % Filter order
Rp = 0.3;             % Ripple
Wn = [0.2 0.4];     % Passband frequencies (normalized)

% Design the filter
[b, a] = cheby1(n, Rp, Wn, 'bandpass');

[h, t]  = impz(b, a, 1024);
[H, f]  = freqz(b, a, 1024);

figure;
subplot(3, 1, 1);
stem(t(1:100), h(1:100));

subplot(3, 1, 2);
plot((0:511)/1024, abs(H(1:512)));

subplot(3, 1, 3);
plot((0:511)/1024, abs(10*log10(H(1:512))));

figure;
t = 0.1:0.001:10;
f1 = 15;
f2=460;
f3=220;
f4=250;

s = sin(2*pi*f1*t)+sin(2*pi*f2*t)+sin(2*pi*f3*t)+sin(2*pi*f4*t);

subplot(2, 1 , 1);
plot((0:511)/1024, abs(10*log10(H(1:512))));


clc; clear; close all;

n1 = 4; n2 = 20;
r = 0.5;

fc = 0.25;
f = (0:511)/1024;

Fs = 0:0.01:1;
x=0:0.01:1;
w = Fs/fc;

T4 = chebyshevT(n1, x);
T20 = chebyshevT(n2, x);
figure(1);
plot(x, T4, 'g', x, T20, 'r'); grid on;
legend('T(4)', 'T(20)');

T4m = chebyshevT(n1, w);
T20m = chebyshevT(n2, w);

G4 = 1./sqrt(1+r.^2.*T4m.^2);
G20 = 1./sqrt(1+r.^2.*T20m.^2);

figure;
plot(w, G4, 'g', w, G20, 'r'); grid on;
title("Frequency response (non-dB)");
legend('T(4)', 'T(20)');

figure;
plot(w, 10*log10(G4), 'g', w, 10*log10(G20), 'r'); grid on;
title("Frequency response (dB)");
legend('T(4)', 'T(20)');

% noisy signal
t = 0:0.001:1;
s = sin(2*pi*25*t)+0.7*sin(2*pi*220*t);

figure;
subplot(2, 1, 1);
plot(s(1:300)); grid on; title("noisy signal");
s_out4 = conv(T4,s);
s_out20 = conv(T20, s);

subplot(2, 1, 2);
plot(t(1:300), s_out4(1:300), 'b', t(1:300), s_out20(1:300), 'r');
grid on; title("filtered signal");


clc; clear; close all;

n=6; r=0.5; fc=0.3;

a0=4.18e-3;
a1=-2.51e-02;
a2=6.28e-02;
a3=-8.37e-02;
a4=6.28e-02;
a5=-2.51e-02;
a6=4.18e-03;

b1=-2.31e+00;
b2=-3.29;
b3=-2.9;
b4=-1.69;
b5=-6.02e-01;
b6=-1.03e-01;

a = [a1, a2, a3, a4, a5, a6];
b = [b1, b2, b3, b4, b5, b6];

fvtool(a, b);

f1=220; f2=250; f3=420;

t = 0:0.001:10;
s = sin(2*pi*f1*t)+0.7*sin(2*pi*f2*t)+0.3*sin(2*pi*f3*t);
s_out = filter(a, b, s);

S = fft(s, 512); S_out=fft(s_out, 512);

figure;
subplot(2, 1, 1); plot(t(1:100), s(1:100), 'b', t(1:100), s_out(1:100), 'r'); grid on;
legend('s(t)', 's_out(t)');

f = (0:512)/1024;

subplot(2, 1, 2); plot(f, abs(S), 'b', t(1:100), s_out(1:100), 'r'); grid on;
legend('s(t)', 's_out(t)');
"""