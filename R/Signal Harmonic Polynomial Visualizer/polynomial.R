#####################################
# Polynomial Harmonic Visualization #
# Version 1.3                       #
#                                   #
# February 6, 2018                  #
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
  20*log10(abs(volts))
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
sample.rate = 8192
npts = 1024

dt = 1/npts
t <- 0:(npts - 1) * dt

# Frequency Axis
df <- npts/sample.rate
f <- 0:(npts-1)/df
f.shift <- fftshift(f)
f.shift[1:floor(npts/2)] <- f.shift[1:floor(npts/2)]-f[npts]-df
f.shift <- f.shift*2

# Creating the sine waves
freq <- 1008 # 8 peaks over 250ms
omega <- 2 * pi * freq

peaks <- sample.rate / npts
period <- 1:(npts / (peaks*2))

# Fundamental Frequency
fundamental <- cos(omega*t)

# Harmonics at -100dB
harmonics.2 <- tovolt(-100)*cos(2*omega*t)
harmonics.3 <- tovolt(-100)*cos(3*omega*t)
harmonics.4 <- tovolt(-100)*cos(4*omega*t)
harmonics.5 <- tovolt(-100)*cos(5*omega*t)
harmonics.6 <- tovolt(-100)*cos(6*omega*t)

# There's definitely a better way to do this but I really didn't feel like bothering with matricies right now
signal <- fundamental + harmonics.2 + harmonics.3 + harmonics.4 + harmonics.5 + harmonics.6

# FFT of the signals
f.signal <- fft(signal) / npts
f.signal.db <- todb(abs(f.signal))

f.fundamental <- fft(fundamental) / npts
f.signal.harmonics <- f.signal - f.fundamental
f.signal.harmonics.db <- todb(f.signal.harmonics)

wave.no.fundamental <- Re(fft(f.signal.harmonics, inverse = TRUE))
wave.no.fundamental.trimmed <- wave.no.fundamental[period]
fit.6 <- lm(wave.no.fundamental.trimmed~poly(period, 25, raw = TRUE))

fit.6 <- unname(predict(fit.6, data.frame(x = t)))

poly.expand <- rep(fit.6, length.out = npts)
f.poly.expand <- fft(poly.expand) / npts
f.poly.expand.db <- todb(abs(f.poly.expand))


# Plots results on a pdf
pdf("results.pdf", width = 15, height = 10)

par(mfrow = c(3,4))

plot(t*1000,signal, "l", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "Signal", col = "green")
grid(nx = NULL, col = "gray")

plot(f.shift/1000,abs(fftshift(f.signal)), "l", xlab = "F (kHz)", ylab = "Magnitude (V)", main = "FFT", col = "yellow")
grid(nx = NULL, col = "gray")

plot(f.shift/1000,abs(fftshift(f.signal.harmonics)), "l", xlab = "F (kHz)", ylab = "Magnitude (V)", main = "FFT (Harmonics)", col = "orange")
grid(nx = NULL, col = "gray")

plot(f.shift/1000,fftshift(f.signal.db), "l", xlab = "F (kHz)", ylab = "Magnitude (V)", main = "FFT (dB)", col = "purple")
grid(nx = NULL, col = "gray")

plot(f.shift/1000,fftshift(f.signal.harmonics.db), "l", xlab = "F (kHz)", ylab = "Magnitude (V)", main = "FFT (dB) (Harmonics)", col = "blue")
grid(nx = NULL, col = "gray")

plot(t*1000,wave.no.fundamental, "l", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "Signal (No Fundamental)", col = "turquoise")
grid(nx = NULL, col = "gray")

plot(t[period]*1000,wave.no.fundamental.trimmed, "l", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "Signal (No Fundamental) (One Period)", col = "red")
grid(nx = NULL, col = "gray")

plot(t[period]*1000,fit.6, "l", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "6th Order Polynomial Fit (One Period)", col = "magenta")
grid(nx = NULL, col = "gray")

plot(t*1000,poly.expand, "l", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "6th Order Polynomial Fit", col = "pink")
grid(nx = NULL, col = "gray")

plot(f.shift/1000,abs(fftshift(f.poly.expand)), "l", xlab = "F (kHz)", ylab = "Magnitude (V)", main = "FFT (Polynomial)", col = "cornflowerblue")
grid(nx = NULL, col = "gray")

plot(f.shift/1000,fftshift(f.poly.expand.db), "b", xlab = "F (kHz)", ylab = "Magnitude (V)", main = "FFT (dB) (Polynomial)", col = "darkorchid1")
grid(nx = NULL, col = "gray")



dev.off()












