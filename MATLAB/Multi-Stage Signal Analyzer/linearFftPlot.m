function plt = linearFftPlot(f,FData)
    plot(f/1000,real(FData), f/1000, imag(FData), f/1000, abs(FData));
    legend('Re','Im','Abs');
    grid on;
    title('Output Signal FFT (Linear), Frequency Domain');
    xlabel('Frequency (kHz)');
    ylabel('Signal (V)');
end

