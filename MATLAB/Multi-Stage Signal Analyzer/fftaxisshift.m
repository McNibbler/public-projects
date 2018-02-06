function fs=fftaxisshift(f);
% fs=fftaxisshift_00_00(f);
% by Chuck DiMarzio
% Northeastern University
% June 2002
% 
% Rev. 0.00
% usage:
% vs=fftshift(v);
% fs=fftaxisshift(f);
% plot(fs,real(vs)fs,imag(vs));xlabel('frequency');ylabel('Spectrum');

df=f(2)-f(1);
fs=fftshift(f);
fs(1:floor(length(f)/2))=fs(1:floor(length(f)/2))-f(length(f))-df;
