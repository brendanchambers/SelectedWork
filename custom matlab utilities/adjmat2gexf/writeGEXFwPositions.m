function [ success ] = writeGEXFwPositions( adjMat, nodePositions, output_path, thresh )
%WRITEGEXFwPositions write an xml file from an adjacency matrix, so gephi can read it
        % include node positions

N = length(adjMat); % number of nodes
THRESH = thresh;

% write header:
docNode = com.mathworks.xml.XMLUtils.createDocument('gexf');
docNode.getDocumentElement.setAttribute('xmlns','http://www.gexf.net/1.2draft');
docNode.getDocumentElement.setAttribute('xmlns:viz','http://www.gexf.net/1.2draft/viz');
docNode.getDocumentElement.setAttribute('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance');
docNode.getDocumentElement.setAttribute('xsi:schemaLocation','http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd');

% meta comments would go here...include meaningless set just in case
metaNode = docNode.createElement('meta');
docNode.getDocumentElement.appendChild(metaNode);
metaNode.setAttribute('lastmodifieddate','2013-03-17');
createrNode = docNode.createElement('creater');
metaNode.appendChild(createrNode);
descriptionNode = docNode.createElement('description');
metaNode.appendChild(descriptionNode);

% graph specification starts here
graphNode = docNode.createElement('graph');
graphNode.setAttribute('defaultedgetype','directed');
graphNode.setAttribute('mode','static');
docNode.getDocumentElement.appendChild(graphNode);

    % nodes
    nodesNode = docNode.createElement('nodes');
    graphNode.appendChild(nodesNode);
    
    for i=1:N
        nodeNode = docNode.createElement('node');
        nodeNode.setAttribute('id',num2str(i));
        nodeNode.setAttribute('label',num2str(i));
        % other attributes go here
        % e.g.  viz:position
            % x="6.5" y="-160" z="0"
        % or size, or color
            positionNode = docNode.createElement('viz:position');
            positionNode.setAttribute('x',num2str(nodePositions(i,1)));
            positionNode.setAttribute('y',num2str(nodePositions(i,2)));
            positionNode.setAttribute('z',num2str(nodePositions(i,3)));
            nodeNode.appendChild(positionNode);
        nodesNode.appendChild(nodeNode);
    end
    
    % edges
    edgesNode = docNode.createElement('edges');
    graphNode.appendChild(edgesNode);
    
    for i=1:N
        for j=1:N
            if adjMat(i,j) > THRESH
                edgeNode = docNode.createElement('edge');
                edgeNode.setAttribute('source',num2str(i));
                edgeNode.setAttribute('target',num2str(j));
                edgeNode.setAttribute('weight',num2str(adjMat(i,j)));
                % attvalues go here if needed
                edgesNode.appendChild(edgeNode);
            end
        end
    end

% write xml file
xmlwrite(output_path,docNode)
success=1;

end


