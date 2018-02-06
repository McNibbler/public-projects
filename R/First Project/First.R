#########################
# Basic Plotting Script #
#                       #
# January 17, 2018      #
# Thomas Kaunzinger     #
# XCerra Corp.          #
#########################

# Clears working environment
rm(list=ls())

# Library I installed that contains fftshift()
library(SynchWave)

# Imports the set of data from the text file
imported.data <- read.table("C://Users//tkaunzin//Desktop//Projects//projects//R//First Project//ADCData4192k_AFE_site1.txt", header = F)

# Converts first column of Data Frame to a workable vector
data <- imported.data[,1]

# 192kHz sample rate as specified by the filename
sampling.rate <- 192000

# Creating the time axis
t <- 0:(length(data) - 1)
t <- t / sampling.rate

# Number of Samples
npts <-  length(t)

# Creating the frequency axis
# Based on fftaxis.m by Charles DiMarzio (2002 NEU)
df <- (t[2]-t[1])*npts
f <- (1:npts-1)/df
f.shift <- fftshift(f)
f.shift[1:floor(npts/2)] <- f.shift[1:floor(npts/2)]-f[npts]-df
f.shift <- f.shift*2

# Fast Fourier Transfer of data
data.fft <- fft(data)/npts
data.fft.shift <- fftshift(data.fft)
data.fft.db <- fftshift(20*log10(abs(data.fft)))


############
# PLOTTING #
############

# To save graphs to pdf
pdf("results.pdf", width = 15, height = 10)

# 4 graphs viewed in a 2x2 grid
par(mfrow = c(2,2))

# Raw Wave
plot(t*1000,data, "l", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "ADC Data (Raw)", col = "green")
grid(nx = NULL, col = "gray")

# Trimmed Wave for visibility
plot(t[0:1000]*1000,data[0:1000], "l", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "ADC Data (Trimmed)", col = "magenta")
grid(nx = NULL, col = "gray")

# FFT (linear)
plot(f.shift/1000, Im(data.fft.shift), "l", col = "blue", xlab = "Frequency (kHz)", ylab = "Amplitude (V)", main = "ADC FFT (Linear)")
lines(f.shift/1000, Re(data.fft.shift), col = "red")
grid(nx = NULL, col = "gray")
legend("topright",, c("Real", "Imag"), c("red", "blue"))

# FFT (dB)
plot(f.shift/1000, data.fft.db,"l", col = "turquoise", xlab = "Frequency (kHz)", ylab = "Amplitude (dB)", main = "ADC FFT (dB)")
grid(nx = NULL, col = "gray")

# Closes the plots
dev.off()







