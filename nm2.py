# -*- coding: utf-8 -*-
"""
Created on Sun May 13 14:57:04 2018

@author: Siddharth
"""
import networkx as nx
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import *
print(__version__) # requires version >= 1.9.0

G = nx.DiGraph()

"""ADDING THE NODES"""
nodes=open("nodes.csv","r")
for line in nodes.readline():
    continue
for line in nodes.readlines():
    G.add_node(line.split(',')[0],demand=int(line.split(',')[3]))
nodes.close()    

"""ADDING THE EDGES"""
edges=open("edges.csv","r")
for line in edges.readline():
    continue
for line in edges.readlines():
    G.add_edge(line.split(',')[0],line.split(',')[1],weight=int(line.split(',')[2]),capacity=int(line.split(',')[3]))
edges.close()

"""EXECUTING THE MINIMUM COST FLOW PROBLEM"""
flowDict = nx.min_cost_flow(G)
flowCost = nx.cost_of_flow(G,flowDict)

"""PLOTTING THE GRAPH"""
f=open("nodes.csv","r")
for line in f.readline():
    continue
x_list = [float(line.split(',')[2]) for line in f.readlines()]
f.close()

f=open("nodes.csv","r")
for line in f.readline():
    continue
y_list = [float(line.split(',')[1]) for line in f.readlines()]
f.close()

x_y_coord =list(zip(x_list,y_list))
node_coord = {}
for i,node in enumerate(G.nodes):
    node_coord[node] = x_y_coord[i]

edge_trace = Scatter(
    x=[],
    y=[],
    line=Line(width=0.5,color='#888'),
    hoverinfo='text',
    mode='lines')

for edge in G.edges:
    x0, y0 = node_coord[edge[0]]
    x1, y1 = node_coord[edge[1]]
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]

node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='Bluered',
        reversescale=False,
        color=[],
        size=10,
        colorbar=dict(
            thickness=10,
            title='Flow at each node<br>Total cost of this flow is: '+str(flowCost),
            xanchor='right',
            titleside='right'),
    line=dict(width=2)))
        
for node in G.nodes:
    x, y = node_coord[node]
    node_trace['x'].append(x)
    node_trace['y'].append(y)
    node_trace['text'].append(node)

for node in flowDict:
    node_trace['marker']['color'].append(sum([flowDict[node][dest] for dest in flowDict[node]]))
    node_info = '# of connections: '+str(sum([flowDict[node][dest] for dest in flowDict[node]]))
    node_trace['text'].append(node_info)

fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                title="<br>Walmart's Distribution Network in the Pacific-Northwest",
                titlefont=dict(size=20),
                showlegend=True,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

plot(fig, filename="network_graph.html")    

print(flowDict)
print("Total cost of this flow is: $"+str(flowCost))