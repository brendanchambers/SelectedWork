% created by Sadovsky. Normalizes fluomat, typical preVoogle preprocessing
function [fluoMat, fluoMatRaw] = processFluomat(fluomatFile,frameTimeMs)
    fluoMatRaw=load(fluomatFile);
    
    fluoMat=fluoMatRaw;

    %drop the first frame 
    %also the last frame is always fux0r3d so lets drop it
    fluoMat=fluoMat(:,2:end-1);
    
    %flip and filter
    flipped = fliplr (fluoMat);
    fluoMat=filterFluomat([flipped fluoMat flipped],frameTimeMs);
    
    %cut it back to size
    fluoMat=fluoMat(:,size(flipped,2)+1:size(flipped,2)*2);
        
    %normalize data    
    for (i=1:size(fluoMat,1))
        fluoMat(i,:)=fluoMat(i,:) - min(fluoMat(i,:));
        fluoMat(i,:)=fluoMat(i,:) / max(fluoMat(i,:));
    end
        
    % experimental - bc   try z-scores instead of normalizing between 0 and
    % 1  ... hmm seems better to do this after my additional filtering
    % steps
    %fluoMat = zscore(fluoMat,0,2);

    
end