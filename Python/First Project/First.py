#########################
# Basic Plotting Script #
#                       #
# January 23, 2018      #
# Thomas Kaunzinger     #
# XCerra Corp.          #
#########################

# Imports appropriate libraries
import numpy as np
import matplotlib.pyplot as plt

# Imports the data from the text file
data = np.genfromtxt("ADCData4192k_AFE_site1.txt", delimiter="\n", skip_header=0)

# Given sample rate
sampleRate = 192000

# Number of Samples
npts = len(data)

# Creating time axis
dt = 1 / sampleRate
index = range(0, npts, 1)
time = [i * dt for i in index]
tMili = [i * 1000 for i in time]

# Creating frequency axis
df = (time[1] - time[0]) * npts
frequency = [i / df for i in index]
fKilo = [i / 1000 for i in frequency]

# Shifting the frequency axis
shiftIndex = range(-1*(npts//2),npts//2,1)
freqShift = [i*2 / df for i in shiftIndex]
fShiftKilo = [i / 1000 for i in freqShift]

# FFT of the data
Fdata = np.fft.fft(data)
Fdata = [i / npts for i in Fdata]
FdataShift = np.fft.fftshift(Fdata, axes = None)
FdataDb = [20*np.log10(abs(i)) for i in FdataShift]


############
# PLOTTING #
############

# Creating the figure
plt.figure(1)

# Raw Wave
plt.subplot(221)
plt.plot(tMili, data, color = "green")
plt.xlabel("Time (ms)")
plt.ylabel("Magnitude (V)")
plt.title("ADC Data (Raw)")
plt.grid(color = "lightgray")

# Trimmed Wave
plt.subplot(222)
plt.plot(tMili[:1000], data[:1000], color = "magenta")
plt.xlabel("Time (ms)")
plt.ylabel("Magnitude (V)")
plt.title("ADC Data (Trimmed)")
plt.grid(color = "lightgray")

# FFT (Linear)
plt.subplot(223)
imag = plt.plot(fShiftKilo, np.imag(FdataShift), color = "blue", label = "imag")
real = plt.plot(fShiftKilo, np.real(FdataShift), color = "red", label = "real")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Amplitude (V)")
plt.title("ADC FFT (Linear)")
plt.legend()
plt.grid(color = "lightgray")

# FFT (dB)
plt.subplot(224)
plt.plot(fShiftKilo, FdataDb, color = "turquoise")
plt.xlabel("Frequency (kHz)")
plt.ylabel("Amplitude (dB)")
plt.title("ADC FFT (dB)")
plt.grid(color = "lightgray")

# Displays the plots
plt.show()
