#########################
# Optimal Caputring Sim #
# Version 1.0           #
#                       #
# January 25, 2018      #
# Thomas Kaunzinger     #
# XCerra Corp.          #
#########################

# Library
library(SynchWave)

# Simulation sampling rate and number of samples
sample.rate <- 2^16
npts <- 2^8

# Creates time axis
t <- 0:(npts-1)
t <- t/sample.rate

df <- npts/sample.rate
f <- 0:(npts-1)/df
f.shift <- fftshift(f)
f.shift[1:floor(npts/2)] <- f.shift[1:floor(npts/2)]-f[npts]-df
f.shift <- f.shift*2

# Frequencies of each of the simulated signals, from best to worst
freq.1 <- 272  # Prime number of peaks (17)
freq.2 <- 240  # Odd number of peaks   (15)
freq.3 <- 288  # Even number of peaks  (18)
freq.4 <- 256  # 2^n number of peaks   (16)

# Sample set 2
#freq.1 <- 1072  # Prime number of peaks (67)
#freq.2 <- 1008  # Odd number of peaks   (63)
#freq.3 <- 1056  # Even number of peaks  (66)
#freq.4 <- 1024  # 2^n number of peaks   (64)


# Converts to angular frequency
omega.1 <- freq.1 * 2 * pi
omega.2 <- freq.2 * 2 * pi
omega.3 <- freq.3 * 2 * pi
omega.4 <- freq.4 * 2 * pi

# Creates the signals
v.1 <- cos(omega.1*t + pi)
v.2 <- cos(omega.2*t + pi)
v.3 <- cos(omega.3*t + pi)
v.4 <- cos(omega.4*t + pi)

# Creates noisy signals
v.1.noisy <- rnorm(npts,0,0.5) + v.1
v.2.noisy <- rnorm(npts,0,0.5) + v.2
v.3.noisy <- rnorm(npts,0,0.5) + v.3
v.4.noisy <- rnorm(npts,0,0.5) + v.4

# Takes an FFT of raw signals
f.v.1 <- fft(v.1)/npts
f.v.2 <- fft(v.2)/npts
f.v.3 <- fft(v.3)/npts
f.v.4 <- fft(v.4)/npts

# Takes an FFT of the noisy signals
f.v.1.noisy <- fft(v.1.noisy)/npts
f.v.2.noisy <- fft(v.2.noisy)/npts
f.v.3.noisy <- fft(v.3.noisy)/npts
f.v.4.noisy <- fft(v.4.noisy)/npts

# FFT raw signals (dB)
f.v.1.db <- 20*log10(abs(f.v.1))
f.v.2.db <- 20*log10(abs(f.v.2))
f.v.3.db <- 20*log10(abs(f.v.3))
f.v.4.db <- 20*log10(abs(f.v.4))

# FFT noisy signals (dB)
f.v.1.noisy.db <- 20*log10(abs(f.v.1.noisy))
f.v.2.noisy.db <- 20*log10(abs(f.v.2.noisy))
f.v.3.noisy.db <- 20*log10(abs(f.v.3.noisy))
f.v.4.noisy.db <- 20*log10(abs(f.v.4.noisy))


############
# PLOTTING #
############

# Raw sine waves
pdf("RawWaves.pdf", width = 15, height = 10)

par(mfrow = c(2,2))

plot(t*1000,v.1, "b", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "Prime Waves", col = "green")
grid(nx = NULL, col = "gray")

plot(t*1000,v.2, "b", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "Odd Waves", col = "yellow")
grid(nx = NULL, col = "gray")

plot(t*1000,v.3, "b", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "Even Waves", col = "orange")
grid(nx = NULL, col = "gray")

plot(t*1000,v.4, "b", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "2^n Waves", col = "red")
grid(nx = NULL, col = "gray")

dev.off()


# Noisy sine waves
pdf("NoisyWaves.pdf", width = 15, height = 10)

par(mfrow = c(2,2))

plot(t*1000,v.1.noisy, "b", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "Prime Waves (Noisy)", col = "green")
grid(nx = NULL, col = "gray")

plot(t*1000,v.2.noisy, "b", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "Odd Waves (Noisy)", col = "yellow")
grid(nx = NULL, col = "gray")

plot(t*1000,v.3.noisy, "b", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "Even Waves (Noisy)", col = "orange")
grid(nx = NULL, col = "gray")

plot(t*1000,v.4.noisy, "b", xlab = "Time (ms)", ylab = "Magnitude (V)", main = "2^n Waves (Noisy)", col = "red")
grid(nx = NULL, col = "gray")

dev.off()


# Linear FFT raw
pdf("LinearFFTRaw.pdf", width = 15, height = 10)

par(mfrow = c(2,2))

plot(f.shift, fftshift(abs(f.v.1)), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (V)", main = "Prime FFT", col = "green")
grid(nx = NULL, col = "gray")

plot(f.shift, fftshift(abs(f.v.2)), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (V)", main = "Odd FFT", col = "yellow")
grid(nx = NULL, col = "gray")

plot(f.shift, fftshift(abs(f.v.3)), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (V)", main = "Even FFT", col = "orange")
grid(nx = NULL, col = "gray")

plot(f.shift, fftshift(abs(f.v.4)), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (V)", main = "2^n FFT", col = "red")
grid(nx = NULL, col = "gray")

dev.off()


# Linear FFT noisy
pdf("LinearFFTNoisy.pdf", width = 15, height = 10)

par(mfrow = c(2,2))

plot(f.shift, fftshift(abs(f.v.1.noisy)), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (V)", main = "Prime FFT (Noisy)", col = "green")
grid(nx = NULL, col = "gray")

plot(f.shift, fftshift(abs(f.v.2.noisy)), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (V)", main = "Odd FFT (Noisy)", col = "yellow")
grid(nx = NULL, col = "gray")

plot(f.shift, fftshift(abs(f.v.3.noisy)), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (V)", main = "Even FFT (Noisy)", col = "orange")
grid(nx = NULL, col = "gray")

plot(f.shift, fftshift(abs(f.v.4.noisy)), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (V)", main = "2^n FFT (Noisy)", col = "red")
grid(nx = NULL, col = "gray")

dev.off()


# dB FFT raw
pdf("dbFFT.pdf", width = 15, height = 10)

par(mfrow = c(2,2))

plot(f.shift, fftshift(f.v.1.db), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (dB)", main = "Prime FFT (dB)", col = "green")
grid(nx = NULL, col = "gray")

plot(f.shift, fftshift(f.v.2.db), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (dB)", main = "Odd FFT (dB)", col = "yellow")
grid(nx = NULL, col = "gray")

plot(f.shift, fftshift(f.v.3.db), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (dB)", main = "Even FFT (dB)", col = "orange")
grid(nx = NULL, col = "gray")

plot(f.shift, fftshift(f.v.4.db), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (dB)", main = "2^n FFT (dB)", col = "red")
grid(nx = NULL, col = "gray")

dev.off()


# dB FFT noisy
pdf("dbFFTNoisy.pdf", width = 15, height = 10)

par(mfrow = c(2,2))

plot(f.shift, fftshift(f.v.1.noisy.db), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (dB)", main = "Prime FFT (dB) (Noisy)", col = "green")
grid(nx = NULL, col = "gray")

plot(f.shift, fftshift(f.v.2.noisy.db), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (dB)", main = "Odd FFT (dB) (Noisy)", col = "yellow")
grid(nx = NULL, col = "gray")

plot(f.shift, fftshift(f.v.3.noisy.db), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (dB)", main = "Even FFT (dB) (Noisy)", col = "orange")
grid(nx = NULL, col = "gray")

plot(f.shift, fftshift(f.v.4.noisy.db), "b", xlab = "Frequency (Hz)", ylab = "Magnitude (dB)", main = "2^n FFT (dB) (Noisy)", col = "red")
grid(nx = NULL, col = "gray")

dev.off()






