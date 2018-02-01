#####################################
# Polynomial Harmonic Visualization #
# Version 1.0                       #
#                                   #
# January 26, 2018                  #
# Thomas Kaunzinger                 #
# XCerra Corp.                      #
#####################################

# Library
library(SynchWave)


###################
# HELPER FUNCTION #
###################

# todb: number -> number
# Converts a number from volts to decibels
# Given 0.1V, expect -20dB
todb <- function(volts){
  20*log10(volts)
}

# tovolt: number -> number
# Converts a number from decibels to volts
# Given 20dB, expect 10V
tovolt <- function(db){
  10^(db/20)
}

####################
# END OF FUNCTIONS #
####################


# Creating the sine waves
sample.rate = 65536/8
npts = 1024/2

dt = 1/npts
t <- 0:(npts - 1) * dt

# Frequency Axis
df <- npts/sample.rate
f <- 0:(npts-1)/df
f.shift <- fftshift(f)
f.shift[1:floor(npts/2)] <- f.shift[1:floor(npts/2)]-f[npts]-df
f.shift <- f.shift*2

# Creating the sine waves
freq <- 1008 # 5 peaks over 250ms
omega <- 2 * pi * freq

# Fundamental Frequency
fundamental <- cos(omega*t)

# Harmonics at -100dB
harmonics.2 <- tovolt(-100)*cos(2*omega*t)
harmonics.3 <- tovolt(-100)*cos(3*omega*t)
harmonics.4 <- tovolt(-100)*cos(4*omega*t)
harmonics.5 <- tovolt(-100)*cos(5*omega*t)
harmonics.6 <- tovolt(-100)*cos(6*omega*t)


signal <- fundamental + harmonics.2 + harmonics.3 + harmonics.4 + harmonics.5 + harmonics.6

f.signal <- fft(signal) / npts
f.signal.db <- todb(abs(f.signal))

f.fundamental <- fft(fundamental) / npts
f.signal.harmonics <- f.signal - f.fundamental
f.signal.harmonics.db <- todb(f.signal.harmonics)


pdf("results.pdf", width = 15, height = 10)

par(mfrow = c(2,3))

plot(t*1000,signal, "l", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "Signal", col = "green")
grid(nx = NULL, col = "gray")

plot(f.shift/1000,fftshift(f.signal), "l", xlab = "F (kHz)", ylab = "Magnitude (V)", main = "FFT", col = "yellow")
grid(nx = NULL, col = "gray")

plot(f.shift/1000,fftshift(f.signal.harmonics), "l", xlab = "F (kHz)", ylab = "Magnitude (V)", main = "FFT (harmonics)", col = "yellow")
grid(nx = NULL, col = "gray")

plot(f.shift/1000,fftshift(f.signal.db), "l", xlab = "F (kHz)", ylab = "Magnitude (V)", main = "FFT (dB)", col = "purple")
grid(nx = NULL, col = "gray")

plot(f.shift/1000,fftshift(f.signal.harmonics.db), "l", xlab = "F (kHz)", ylab = "Magnitude (V)", main = "FFT (dB) (harmonics)", col = "blue")
grid(nx = NULL, col = "gray")

plot(t*1000,fft(f.signal.harmonics, inverse = TRUE), "l", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "Signal (No Fundamental)", col = "turquoise")
grid(nx = NULL, col = "gray")

dev.off()












