function [ C_cycle, C_midman, C_in, C_out, C_all, meanShortestPath_b, meanShortestPath_w, sparseness, W, adj ] = smallworldnessHelper( adjmat, thresh )
%GETSWSTATS input an adjmat and threshold percent 

% and output
% 1. median of local clustering coefficients (binary/directed & weighted/directed)
%        UPDATED 7-9-14. Clustering metric was enforcing symmetry on
%        matrices, so it was really an undirected measure. Updating to look
%        at weighted directed triangles.
%          Modifications could be made to look at BINARY directed
%          triangles, which would be useful for counting motif occurence.
% 2. mean shortest path (characteristic distance for (1 - W)
% 3. sparseness

% UPDATED 7-7-14 to use my own code for clustering, based on Fagiolo

%%   threshold adjmat

      W = adjmat; % rename for convenience

      % thresholding
      cutoff = thresh; % weight cutoff as a percent of non-zero values
      thresh_real = prctile(W(W(:) > 0), cutoff); % threshold at top % of links iteratively    
      % binary
      adj = zeros(size(W));
      adj(W(:) < thresh_real) = 0; % lower than cutoff percent
      adj(W(:) >= thresh_real) = 1; % higher than cutoff percent
      % weighted
      W(W(:) < thresh_real) = 0; % lower than cutoff percent
 %%      % sparseness
      
      numEdges = sum(sum(adj,1),2); % compare sparseness across graphs
      sparseness = numEdges / length(W(:));
%%      clustering
      % compute local weighted directed clustering
      %clusterDist_wd = clustering_coef_wd(W); % binary & directed version
      %clustering_wd = median(clusterDist_wd(:)); % (clusterDist_wd(:) > 0)) % optional: don't include isolated nodes
        
      % compute local binary directed clustering
      %clusterDist_bd = clustering_coef_bd(adj); % binary & directed version
      %clustering_bd = median(clusterDist_bd(:)); % (clusterDist_bd(:) > 0)) % optional: don't include isolated nodes
      
      % this the new clustering code--mine. Looks at directed triangles.
      [ C_cycle C_midman C_in C_out C_all ] = clusterF(W);
      %figure(); bar([ mean(C_cycle) mean(C_midman) mean(C_in) mean(C_out) mean(C_all) clustering_wd]); title('testing: comparison of clustering measures');
      
    %% shortest paths
    
    costMat_b = zeros(size(adjmat));
    costMat_b(adj(:) == 0) = Inf; % no path exists
    costMat_b(adj(:) > 0) = 1;
    
    costMat_w = zeros(size(adjmat));
    costMat_w(W(:) == 0) = Inf;
    costMat_w(W(:) > 0) = 1 - W(W(:) > 0); % cost is complement of weight (inverse could also work)
    
    costMat_b = zeros(size(adjmat));
    costMat_b(W(:) == 0) = Inf;
    costMat_b(W(:) > 0) = 1;
    
    costpaths_w = dijkstra(adj, costMat_w);
    costpaths_b = dijkstra(adj, costMat_b);
    meanShortestPath_w = median(costpaths_w(:));
    meanShortestPath_b = median(costpaths_b(:)); % well now technically this is not 'mean' shortest path
    
      % characteristic paths
      %meanShortestPath_w = charpath(costMat_w);  % the old way, that works better--  % unconnected nodes: cost = 1
                                            % connected nodes: cost < 1
      %meanShortestPath_b = charpath(costMat_b);  % unconnected nodes: cost = 100.
                                                       % connected nodes: cost = 1
      %[L,EGlob,C,ELoc] = graphProperties(adj)
     

end

