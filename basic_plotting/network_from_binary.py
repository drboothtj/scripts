'''
build a network from a feature table
  arguments:
    argv[1]: feature table .csv
'''
import plotly.graph_objects as go
from pylab import rcParams
import numpy as np
import csv
from sys import argv

import networkx as nx
import matplotlib.pyplot as plt

def get_data_from_csv(filename):
  nodes = []
  features = {}
  with open(filename, newline='') as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)[1:]  # Skip 'Node' header
    for row in reader:
        node_id = row[0]
        binary_values = list(map(int, row[1:]))
        nodes.append(node_id)
        features[node_id] = binary_values
  return nodes, features

def create_network(nodes, features):
  G = nx.Graph()
  G.add_nodes_from(nodes)
  for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
      n1, n2 = nodes[i], nodes[j]
      shared = sum(a & b for a, b in zip(features[n1], features[n2]))
      if shared > 5: #modify this with an arg
        G.add_edge(n1, n2, weight=shared)
  return G

def draw_network(G, nodes, features):
  pos = nx.kamada_kawai_layout(G, scale = 20)
  edge_x = []
  edge_y = []
  edge_weights = []

  for u, v, data in G.edges(data=True):
    x0, y0 = pos[u]
    x1, y1 = pos[v]
    edge_x += [x0, x1, None]
    edge_y += [y0, y1, None]
    edge_weights.append(data['weight'])

  edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='gray'),
    hoverinfo='none',
    mode='lines'
  )

  # Create Plotly node traces
  node_x = []
  node_y = []
  node_text = []

  for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(f'Node {node}<br>Features: {features[node]}')

  node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=[str(n) for n in nodes],
    textposition='bottom center',
    hovertext=node_text,
    hoverinfo='text',
    marker=dict(
        color='skyblue',
        size=20,
        line=dict(width=2, color='darkblue')
    )
  )

  # Create and save Plotly figure
  fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Network Graph from Binary Data',
                    titlefont_size=20,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False)
                ))

  # Save to HTML file (view in browser)
  fig.write_html("network_plot.html")

def main(filename):
  nodes, features = get_data_from_csv(filename)
  network = create_network(nodes,features)
  draw_network(network, nodes, features)

filename = argv[1]
main(filename)

