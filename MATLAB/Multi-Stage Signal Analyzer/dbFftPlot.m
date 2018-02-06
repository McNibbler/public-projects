function plt = dbFftPlot(f,FData)
% plots the magnitude and phase of the data

    plot(f/1000,todb(FData));
    ylabel('Amplitude (dBV)');
    ylim([min(todb(FData)) - 10, max(todb(FData)) + 10]);
    
    legend('Magnitude');
    grid on;
    
    [~, maxIndex] = max(abs(FData));
    title(['Output Signal FFT (dBV), Frequency Domain (1st Fund. Phase: ', num2str(phaseCalc(FData, maxIndex)),'°)']);
    xlabel('Frequency (kHz)');

end

