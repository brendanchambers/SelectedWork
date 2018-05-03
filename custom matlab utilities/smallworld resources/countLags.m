function [ W_count, spiketally_pre, spiketally_post ] = countLags( raster, LAG_WINDOW )
%COUNT LAGS
    % input population activity N neurons x L frames
    % count 1-frame lags
    % count lags and total spikes
    
        
    N = size(raster,1);
    L = size(raster,2);
    
    W_count = zeros(N,N);
    spiketally_pre = zeros(1,N); % don't count last frame
    spiketally_post = zeros(1,N); % don't count first frame
    
    % testing
    %{
    figure(); imagesc(raster); title('raster');
    %}
    
    for i_frame = LAG_WINDOW+1:L
       activePre = sum(raster(:,i_frame-LAG_WINDOW:i_frame-1),2) >= 1;
       activePost = raster(:,i_frame)==1;
       W_count(activePre, activePost) = W_count(activePre, activePost) + 1; % count lags
       spiketally_pre(activePre) = spiketally_pre(activePre)+1; % keep track of total spikes
       spiketally_post(activePost) = spiketally_post(activePost) + 1;
    end
    
end

