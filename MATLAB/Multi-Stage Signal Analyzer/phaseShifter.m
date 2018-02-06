function adjustedData = phaseShifter(fourierData,ang,maxIndex)
    % This function shifts a signal first to the phase of the fundamental
    % frequency and then to any additional specified phase


    % fourierData is data already in the frequency domain
    % ang is the desired angle of the wave (0 is centered)
    % maxIndex is the increment of the harmonics

    % Referrences: Richard Liggiero (XCerra)
    dataMag = abs(fourierData);
    phaseData = angle(fourierData);
    phaseData = atan2(imag(fourierData(1:length(fourierData))),real(fourierData(1:length(fourierData))));
    
    binBoi = 0:length(dataMag) - 1;
    phaseRotate = phaseData(1:length(dataMag))' - (binBoi/maxIndex)*phaseData(maxIndex+1);
    phaseRotate = phaseRotate + ang;
    
    % Real Part
    bindex = 2:length(dataMag) / 2;
    FdataAdjustedReal(bindex) = dataMag(bindex)'.*cos(phaseRotate(bindex));
    FdataAdjustedImag(bindex) = dataMag(bindex)'.*sin(phaseRotate(bindex));
    FdataAdjusted(bindex) = complex(FdataAdjustedReal(bindex), FdataAdjustedImag(bindex));
    
    % Imaginary Part
    bindex = length(dataMag):-1:length(dataMag)/2+2;
    FdataAdjustedReal(bindex) = dataMag(bindex)'.*cos(phaseRotate(bindex));
    FdataAdjustedImag(bindex) = dataMag(bindex)'.*sin(phaseRotate(bindex));
    FdataAdjusted(bindex) = complex(FdataAdjustedReal(bindex), FdataAdjustedImag(bindex));
    
    % Add DC and combine
    FdataAdjusted(1) = fourierData(1);
    FdataAdjusted(length(dataMag)/2+1) = fourierData(length(dataMag)/2+1);
    
    FdataAdjusted = FdataAdjusted.';
    adjustedData = FdataAdjusted;
    
% THIS DIDN'T WORK RIP
%
%     % ignoring DC, only doing front
%     windowSize = 2:length(dataMag)/2;    
%     phaseDataPos = phaseData(windowSize) - (f(windowSize)/fundamentalFreq)'.*(ang);
%     
%     windowSize = length(dataMag):-1:length(dataMag)/2 + 2;
%     phaseDataNeg = phaseData(windowSize) - ((f(windowSize)/fundamentalFreq)'.*(ang));
%     
%     phaseDataNew = cat(phaseDataNeg, phaseData(1), phaseDataPos);
%     
%     adjustedData(1) = dataMag(1);
%     adjustedData = dataMag.*cos(phaseDataNew) + i.*dataMag.*sin(phaseDataNew);
%     
%     adjustedData(length(dataMag)/2+1) = fourierData(length(dataMag)/2+1);
%     adjustedData = adjustedData.';
    
end

