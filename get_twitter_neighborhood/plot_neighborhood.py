__author__ = 'Brendan'

import matplotlib.pyplot as plt
import json
import numpy as np
import networkx as nx

json_neighborhood_file = open('my friend neighborhood_partial.json','r')
neighborhood_graph = json.load(json_neighborhood_file)

vertices = neighborhood_graph['vertices']
edges = neighborhood_graph['edges']
adjmat = np.array(neighborhood_graph['adjacency_matrix']) # edge(a,b) a is friends with b

reference_node = vertices[0]['screen_name']
node_size_scalar = 20
node_sizes = []
node_labels = {}

print vertices[0]
N = len(vertices)
print N
print edges[0]

# CONSTRUCT THE netoworkx graph
DG = nx.DiGraph()
node_colors = [];
for v in vertices:
    DG.add_node(v['screen_name'])
    node_sizes.append(node_size_scalar)
    node_labels[v['screen_name']] = v['screen_name'] # this has to be a dictionary for networkx drawing
    node_colors.append([0,0,0,1])
for e in edges:
    #if e['source'] == reference_node or e['target'] == reference_node:
    #    print ' omit edges touching ' + reference_node
    #else:
    DG.add_edge(e['source'],e['target'],{"weight":e['weight']}) # optional third argument, weight

print node_sizes
print node_labels

fig = plt.figure()
innerShellIDs = vertices[0]['screen_name']
middleShellIDs = []
for v in vertices[1:int(np.floor(N/2))]:
    middleShellIDs.append(v['screen_name'])
outerShellIDs = []
for v in vertices[int(np.floor(N/2)):]:
    outerShellIDs.append(v['screen_name']) # make a third shell to spread things out a little
nx.draw_shell(DG,nlist = [[innerShellIDs], middleShellIDs, outerShellIDs], node_size=node_sizes,labels=node_labels, with_labels=False) # ,node_color=[0,0,0,1],edge_color=[0,0,0])
#nx.draw_spring(DG,node_size=node_sizes)
plt.title('friendship wheel for @societyoftrees')
plt.show()

fig = plt.figure()
plt.imshow(adjmat)
plt.title('adjmat')
plt.show()


