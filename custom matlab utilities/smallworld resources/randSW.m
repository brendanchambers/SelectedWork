function [smallworldness, clustR_b, clustR_w, pathR_b, pathR_w, spars] = randSWdistribution(W_genuine, NUM_RAND_TRIALS)

% assume input W_genuine is thresholded

% this function takes a connectivity matrix (no autapses) 
% returns distribution of smallworldness values for density matched random
% graphs

%% compute sparseness
N = size(W_genuine,1); % number of neurons
edgeIdxs = find(W_genuine(:) > 0);
density = length(edgeIdxs) ./ N^2; % edges out of total possible edges

%% create random graphs
for i_trial = 1:NUM_RAND_TRIALS
    i_trial
   randGraph = zeros(N,N);
   
   % generate graph
   for pre = 1:N
       for post = 1:N
           %if pre ~= post % no autapses, to match genuine matrices
               if rand < density % choose edges randomly
                  % match weight to W_genuine
                  matchIdx = randi(length(edgeIdxs),1,1); % pick one of the edges in W_genuine randomly
                  matchedWeight = W_genuine(edgeIdxs(matchIdx));
                  randGraph(pre,post) = matchedWeight; 
               end
           %end
       end
   end
      
   % test smallworldness
   %smallworldness(i_trial) = testSmallworldness3(randGraph, 0);
   [smallworldness(i_trial), clustR_b(i_trial), clustR_w(i_trial), pathR_b(i_trial), pathR_w(i_trial), spars(i_trial)] = testSmallworldness3(randGraph, 0);
       
end

%smallworldness_genuine = testSmallworldness(W_genuine, 0)
%{
figure();
hist(smallworldness);
title('random sparseness-matched smallworldness');
%}


