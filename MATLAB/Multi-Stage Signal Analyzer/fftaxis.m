function f=fftaxis(t);
% f=fftaxis(t);
% by Chuck DiMarzio
% Northeastern University
% June 2002
% given a vector of equally-spaced time values, computes the
%       corresponding frequency values for an fft.
% Usage:
% plot(t,elk);
% moose=fft(elk);
% f=fftaxis(t);
% plot(f,real(moose),f,imag(moose));
%
% rev = 0.00;
%
% see also FFTAXISSHIFT
%
df=(t(2)-t(1))*length(t);
f=([1:length(t)]-1)/df;
