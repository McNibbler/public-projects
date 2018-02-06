%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Generic Data Analyzer       %
% Version 1.0                 %
%                             %
% February 6, 2018            %
% Thomas Kaunzinger           %
% Xcerra Corp.                %
%                             %
% Referrences:                %
% fftaxisshift.m + fftaxis.m  %
% Charles DiMarzio (NEU 2002) %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Importing New Data %%

% Clears all variables and closes graphs when running
clc;
close all;
clear all;

% Working directories for data
addpath(genpath(pwd));

dataFile1 = '\DATA\anonymous data 1.xlsx';
dataFile2 = '\DATA\anonymous data 2.xlsx';

% Reads time from source excel spreadsheet (all signals should use same
% time intervals)
t = xlsread(dataFile1, 'A:A');

% Reads data and stores in matrix
data1 = xlsread(dataFile1, 'B:B');
data2 = xlsread(dataFile2, 'B:B');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% USE TO SELECT RANGE OF VIEW FOR FFT (multiples of fundamental freq) %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
width = 14; %i.e. width = 5 means graphs will show up to 5x the FF in the x axis


%% Preparing Gathered Data %%

% Number of samples (4096 from AudioPrecision over 0.064 seconds)
npts = length(t);

% converts to frequency domain
f = fftaxis(t);             % x-Axis
fShift = fftaxisshift(fftaxis(t));      % x-axis shifted over y-axis

df = (t(2) - t(1)) * npts; 


% All data
Fdata1 = fft(data1)/npts;
Fdata2 = fft(data2)/npts;

% Axis-shifted versions of FFT data for visualization in negative frequencies
Fdata1Shift = fftshift(Fdata1);
Fdata2Shift = fftshift(Fdata2);


% finds appropriate range for displaying the fourier transform to
%-- make relevant data more visible
%-- testingFrequency should be exactly 1008Hz in this situation
[~, maxIndex] = max(abs(Fdata1));     % to find where the biggest spike in the FFT resides (in case of sine wave, the first harmonic)
testingFrequency = f(maxIndex);
test = find(abs(f)<width*testingFrequency);    % creates a range for where data is most relevant
testShift = find(abs(fShift)<width*testingFrequency);

fundamentalFreq = testingFrequency;

% Number of steps between harmonics
increment = maxIndex - 1;


% Calculates phases at fundamental frequency
phase1 = phaseCalc(Fdata1, maxIndex);
phase2 = phaseCalc(Fdata2, maxIndex);


% Calculates FFTs of signals phase adjusted to compensate for the phase of
% the Fundamental Frequency
Fdata1Adjusted = phaseShifter(Fdata1,deg2rad(0),increment);
Fdata1AdjustedShift = fftshift(Fdata1Adjusted);

Fdata2Adjusted = phaseShifter(Fdata2,deg2rad(0),increment);
Fdata2AdjustedShift = fftshift(Fdata2Adjusted);


% Calculates the gain at different multiples of the fundamental frequency
steps = 1:5;
data1HarmonicAmplitudes = Fdata1Adjusted(steps*increment + 1);
data2HarmonicAmplitudes = Fdata2Adjusted(steps*increment + 1);

maxIndicies = maxIndex:increment:10*increment;

% Gain at the first fundamental frequency
gain = abs(data2HarmonicAmplitudes(1) ./ data1HarmonicAmplitudes(1));

% Resultant error vectors of distortion between stages
resultants = Fdata2Adjusted./gain - Fdata1Adjusted;


% Checks the accuracy of the resultant vectors

% Checks input phase rotated to output
checker1 = gain*(phaseShifter(Fdata1, deg2rad(0+phase2),increment) + phaseShifter(resultants, deg2rad(0+phase2),increment));
finalSum(1) = sum(checker1 - phaseShifter(Fdata2,deg2rad(0+phase2),increment));

% Checks output phase rotated to input
checker2 = gain*(phaseShifter(Fdata1,deg2rad(0+phase1),increment) + phaseShifter(resultants, deg2rad(0 + phase1), increment));
finalSum(2) = sum(checker2-phaseShifter(Fdata2, deg2rad(0 + phase1), increment));

% Checks both rotated to 0
checker3 = gain*(Fdata1Adjusted + resultants);
finalSum(3) = sum(checker3 - Fdata2Adjusted);


% Checks that transfer test is successful under a tolerance of -250dB
if todb(finalSum) < -250
    fprintf("Test passed\n\n");
else
    fprintf("Test failed\n\n");
end

%% First plot %%

% Plots the wave form
max1 = max(max(data1), max(data2));
limit1 = [(-1.1*max1),(1.1*max1)];

figure(1);
subplot(3,2,1);
plot(t*1000,data1);
grid on;
title('Output Signal 1, Time Domain');
xlabel('Time (ms)');
ylabel('Signal (V)');
ylim(limit1);

subplot(3,2,2);
plot(t*1000,data2);
grid on;
title('Output Signal 2, Time Domain');
xlabel('Time (ms)');
ylabel('Signal (V)');
ylim(limit1);

% Plots the fourier transform of the data including imaginary components
max2 = max(max(abs(Fdata1)), max(abs(Fdata2)));
limit2 = [(-1.1*max2),(1.1*max2)];

subplot(3,2,3);
linearFftPlot(fShift(testShift),Fdata1Shift(testShift));
ylim(limit2);

subplot(3,2,4);
linearFftPlot(fShift(testShift),Fdata2Shift(testShift));
ylim(limit2);

% Plots THD
subplot(3,2,5);
thd(data1, npts/max(t), 5);

subplot(3,2,6);
thd(data2, npts/max(t), 5);

%% dB plot details %%

% Limits
figure(2);
lowerLimit = min([min(todb(Fdata1)),min(todb(Fdata2))]);
upperLimit = max([max(todb(Fdata1)),max(todb(Fdata2))]);
limits = [lowerLimit - 10, upperLimit + 10];

% text() is a stupid function that makes this more annoying than it needs
% to be. It's based on the graph itself instead of indicies
xText = steps*f(increment + 1)/1000;

% Y positions
data1YText = todb(Fdata1Adjusted(steps*increment + 1));
data2YText = todb(Fdata2Adjusted(steps*increment + 1));

% Arrows to point to the harmonics
labels = strcat('\leftarrow', arrayfun(@num2str, steps, 'UniformOutput', false));

% I hate everything about this but it works
string1 = strcat('M:',num2str(abs(Fdata1Adjusted(steps*increment + 1))),' P:',num2str(angle(Fdata1Adjusted(steps*increment + 1))),'° M:',...
    num2str(data1YText(steps)),'dB R:',num2str(real(resultants(steps*increment + 1))),'+',...
    num2str(imag(resultants(steps*increment + 1))),'j');
string2 = strcat('M:',num2str(abs(Fdata2Adjusted(steps*increment + 1))),' P:',num2str(angle(Fdata2Adjusted(steps*increment + 1))),'° M:',...
    num2str(data2YText(steps)),'dB');

% Plots data
subplot(2,2,1);
dbFftPlot(f(test),Fdata1Adjusted(test));
ylim(limits);
title(['Input Signal FFT (dBV), Frequency Domain (Shifted ', num2str(phase1), '°)']);
text(xText,data1YText, labels, 'fontsize', 20, 'Color', [.8 .2 .2]);
legend(string1);
legend('boxoff');

subplot(2,2,2);
dbFftPlot(f(test),Fdata2Adjusted(test));
ylim(limits);
title(['Output Signal FFT (dBV), Frequency Domain (Shifted ', num2str(phase2), '°), Gain = ', num2str(gain)]);
text(xText,data2YText, labels, 'fontsize', 20, 'Color', [.8 .2 .2]);
legend(string2);
legend('boxoff');

% Plots all signals against each other at once
subplot(2,1,2);
plot(f(test)/1000,todb(Fdata1Adjusted(test)),'m');
hold on;
plot(f(test)/1000,todb(Fdata2Adjusted(test)),'b');
grid on;
ylabel('Amplitude (dBV)');
xlabel('Frequency (kHz)');
title('Signal Comparison FFT (dBV), Frequency Domain (Phase Corrected)');
ylim(limits);
legend('Input', 'Output');


%% Plotting Original vs Adjusted Waveforms %%

figure(3);

% Plots input data
subplot(2,1,1);
plot(t*1000,data1)
hold on;
plot(t*1000, ifft(Fdata1Adjusted*npts,'symmetric'));
grid on;
ylim(limit1);
title('Input Data vs Corrected Phase');
legend('Original Wave', 'Corrected');
ylabel('Amplitude (V)');
xlabel('Time (ms)');

% Plots output data
subplot(2,1,2);
plot(t*1000,data2)
hold on;
plot(t*1000, ifft(Fdata2Adjusted*npts,'symmetric'));
grid on;
ylim(limit1);
title('Output Data vs Corrected Phase');
legend('Original Wave', 'Corrected');
ylabel('Amplitude (V)');
xlabel('Time (ms)');


%% Plotting Original vs Adjusted Linear FFTs %%

figure(4);

% Input
subplot(2,2,1);
plot(fShift(testShift)/1000,real(Fdata1Shift(testShift)),fShift(testShift)/1000,imag(Fdata1Shift(testShift)));
ylim(limit2);
grid on;
title('Input: Original Linear FFT Signal');
legend('Real', 'Imag');
ylabel('Amplitude (V)');
xlabel('Frequency (kHz)');

subplot(2,2,2);
plot(fShift(testShift)/1000,real(Fdata1AdjustedShift(testShift)),fShift(testShift)/1000,imag(Fdata1AdjustedShift(testShift)));
ylim(limit2);
grid on;
title('Input: Phase Adjusted Linear FFT Signal');
legend('Real', 'Imag');
ylabel('Amplitude (V)');
xlabel('Frequency (kHz)');

% Output
subplot(2,2,3);
plot(fShift(testShift)/1000,real(Fdata2Shift(testShift)),fShift(testShift)/1000,imag(Fdata2Shift(testShift)));
ylim(limit2);
grid on;
title('Output: Original Linear FFT Signal');
legend('Real', 'Imag');
ylabel('Amplitude (V)');
xlabel('Frequency (kHz)');

subplot(2,2,4);
plot(fShift(testShift)/1000,real(Fdata2AdjustedShift(testShift)),fShift(testShift)/1000,imag(Fdata2AdjustedShift(testShift)));
ylim(limit2);
grid on;
title('Output: Phase Adjusted Linear FFT Signal');
legend('Real', 'Imag');
ylabel('Amplitude (V)');
xlabel('Frequency (kHz)');


%% Notable Points of Selected Detailed Data %%

% Extremes
maximum1 = max(data1);
minimum1 = min(data1);
maximum2 = max(data2);
minimum2 = min(data2);

% Values at first harmonic
ampFirstHarmonic1 = abs(Fdata1(maxIndex));
ampFirstHarmonic2 = abs(Fdata2(maxIndex));

% Total harmonic distortion
THD1 = thd(data1, npts/max(t), 5);
THD2 = thd(data2, npts/max(t), 5);

fprintf("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
fprintf('INPUT DATA RESULTS\n\n')
fprintf('Frequency of measured first harmonic = %f\n\n', testingFrequency)
fprintf('Output Signal\nV(max) = %f, V(min) = %f\n\n', maximum1, minimum1)
fprintf('Amplitude at first harmonic = %f V\n', ampFirstHarmonic1)
fprintf('Amplitude at first harmonic = %f dB\n\n', todb(ampFirstHarmonic1))
fprintf('Phase at first harmonic = %f°\n\n', phase1)
fprintf('Total harmonic distortion = %f\n\n\n\n', THD1)

fprintf('OUTPUT DATA RESULTS\n\n')
fprintf('Frequency of measured first harmonic = %f\n\n', testingFrequency)
fprintf('Output Signal\nV(max) = %f, V(min) = %f\n\n', maximum2, minimum2)
fprintf('Amplitude at first harmonic = %f V\n', ampFirstHarmonic2)
fprintf('Amplitude at first harmonic = %f dB\n\n', todb(ampFirstHarmonic2))
fprintf('Phase at first harmonic = %f°\n\n', phase2)
fprintf('Total harmonic distortion = %f\n\n', THD2)

%% Restultant Results %%

fprintf("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
fprintf("Resultant Vector\n\n")
fprintf("\t\tFF\t\t\t\t\t\t\t2\t\t\t\t\t\t\t3\t\t\t\t\t\t\t4\t\t\t\t\t\t\t5\n")
fprintf("Result:\t%f + %fj\t\t%f + %fj\t\t%f + %fj\t\t%f + %fj\t\t%f + %fj\n",real(resultants(increment+1)),imag(resultants(increment+1)),...
    real(resultants(increment*2+1)),imag(resultants(increment*2+1)),real(resultants(increment*3+1)),imag(resultants(increment*3+1)),...
    real(resultants(increment*4+1)),imag(resultants(increment*4+1)),real(resultants(increment*5+1)),imag(resultants(increment*5+1)));

