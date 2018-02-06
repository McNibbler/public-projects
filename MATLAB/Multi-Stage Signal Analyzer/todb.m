function x = todb(v);
    % Converts a voltage signal to dB
    x = 20*log10(abs(v));
end

