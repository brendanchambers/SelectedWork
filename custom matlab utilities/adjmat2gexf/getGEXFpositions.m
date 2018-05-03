function nodePositions = getGEXFpositions(gexf_file)
% take a adjMat and a gefx file
% obtain a list of {x y z} positions for each node
% assume standard gexf formatting


%gexf_file = 'celegans.gexf'; example file for testing

datastruct = xml2struct(gexf_file);

nodeCell = datastruct.gexf.graph.nodes.node; % get the tree of nodes
N = length(nodeCell);

nodePositons = zeros(N,3); % dimensions := N by (x, y, z)
for i=1:N
    nodePositions(i,1) = str2double(nodeCell{i}.viz_colon_position.Attributes.x);
    nodePositions(i,2) = str2double(nodeCell{i}.viz_colon_position.Attributes.y);
    nodePositions(i,3) = str2double(nodeCell{i}.viz_colon_position.Attributes.z);
end

end