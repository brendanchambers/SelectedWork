function [ C_cycle C_midman C_in C_out C_all ] = clusterF_fullinfo( F )  % F is the weighted directed matrix defining a network

%CLUSTERF_fullinfo
%   UPDATING to return triangle motifs for every node instead of median
%   summary.

%  account for directed features of the network topology when
%computing clustering coefficient
% F_ij is the weight on connection i -> j

% This works but it's slow--todo write faster code

%   Reference: Fagiolo (2007) Phys Rev E 76:026107.

% WARNING -- weights on F must be >= 0


    N = size(F,1); % number of nodes
    W = zeros(N,N);  % copy of F to work with
    adj = zeros(N,N); % binary version of F for counting degree
    adj(:) = F(:) > 0;

    % normalize to [0,1] and take cube root
    maxVal = max(F(:));
    W(:) = F(:) ./ maxVal;
    W = W .^ (1/3);

    % number of incoming connections
    d_in = sum(adj,1);

    % number of outgoing connections
    d_out = sum(adj,2);

    % number of bidirectional connections
    temp = adj + adj';
    adj_sym = zeros(N,N);
    adj_sym(:) = temp(:)==2;
    d_bi = sum(adj_sym);

    % clustering coefficients separated by motif structure
    C_cycle = zeros(1,N);
    %C_midman = zeros(1,N);
    %C_in = zeros(1,N);
    %C_out = zeros(1,N);
    C_all = zeros(1,N);    

    for i_ref = 1:N % cell of current perspective
        
        % number of triangles having cycle motif
        denom = (d_in(i_ref)*d_out(i_ref) - d_bi(i_ref)); % catch Inf errors
        if denom ~= 0
            temp = W^3 ./ denom; % number of actual cycles div by number of possible cycles
            C_cycle(i_ref) = temp(i_ref, i_ref);
        else
            C_cycle(i_ref) = 0;
        end
        
        % middleman motif
        denom = (d_in(i_ref)*d_out(i_ref) - d_bi(i_ref));
        if denom ~= 0 % catch Inf errors
            temp = ((W * W') * W) / denom; 
            C_midman(i_ref) = temp(i_ref, i_ref);
        else
            C_midman(i_ref) = 0;
        end

        % fan-in motif
        denom = (d_in(i_ref)*(d_in(i_ref) - 1));
        if denom ~= 0
            temp = (W' * W^2) / denom;
            C_in(i_ref) = temp(i_ref, i_ref);
        else
            C_in(i_ref) = 0;
        end

        % fan-out motif
        denom = (d_out(i_ref) * (d_out(i_ref) - 1));
        if denom ~= 0
            temp = (W^2 * W') ./ denom;
            C_out(i_ref) = temp(i_ref, i_ref);
        else
            C_out(i_ref) = 0;
        end
        
        % any cycle
        d_total = d_in(i_ref) + d_out(i_ref);
        allPossibleCycles = d_total .* (d_total - 1) - 2*d_bi(i_ref);
        if allPossibleCycles ~= 0
            temp2 = (W + W')^3 ./ (2*allPossibleCycles);
            C_all(i_ref) = temp2(i_ref, i_ref);
        else
            C_all(i_ref) = 0;
        end
    end
    
    %{
    C_cycle_summary = median(C_cycle);
    C_midman_summary = median(C_midman);
    C_in_summary = median(C_in);
    C_out_summary = median(C_out);
    C_all_summary = median(C_all);
    %}
    
    'finished clusterF_fullinfo'

end

