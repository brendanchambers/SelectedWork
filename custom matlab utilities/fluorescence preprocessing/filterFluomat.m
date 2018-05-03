function [fluoMat] = filterFluomat(fluoMat,frameRate)
    %highpass
    seconds=25;  % why 25 seconds?
    %seconds = 300; %
    nyquist=(1000/frameRate)/2;
    fMax=(1/seconds)/nyquist;
    [b,a] = butter(1,fMax,'high');
    
    figure(); plot(fluoMat(51,:)); title(' raw ');
    
    for i=1:size(fluoMat,1)
        fluoMat(i,:)=filtfilt(b,a,fluoMat(i,:));
        %fluoMat(i,:) = fluoMat(i,:) ./ mean(fluoMat(i,:),2);
    end
    figure(); plot(fluoMat(51,:)); title(' after hi pass and normalization');
    
    % lopass % experimentally adding this, BC 2-18-2015
    [b,a] = butter(1,0.4,'low');
    for i=1:size(fluoMat,1)
        fluoMat(i,:) = filtfilt(b,a,fluoMat(i,:));
    end
    figure(); plot(fluoMat(51,:)); title(' after lo pass');
    
end

% 87.9232 = 1.5/nyquist
% 75.7856 = 1.25