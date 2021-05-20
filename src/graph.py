from networkx.generators import directed
from pyvis.network import Network
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random

def pairUp(reads,min_overlap):
  pairs = {}
  reversed_graph = {}

  for i in range(len(reads)):
    for j in range(len(reads)):

      if (j == i):
        continue

      r1, r2 = reads[i], reads[j]
      o = calculate_overlap(r1,r2)

      if (o >= min_overlap):
        if r1 not in pairs:
          pairs[r1] = np.array([[r2,o]],dtype=object)
        else:
          pairs[r1] = np.concatenate((pairs[r1], [[r2,o]]))
        if r2 not in reversed_graph:
          reversed_graph[r2] = np.array([[r1, o]], dtype=object)
        else:
          reversed_graph[r2] = np.concatenate((reversed_graph[r2], [[r1, o]]))


  return pairs, reversed_graph

def calculate_overlap(r1,r2):

  overlap = 0
  l = len(r1)

  for i in range(l):
    if r1 == r2:
      overlap = len(r1)
      break

    r1 = r1[1:]
    r2 = r2[:-1]

  return overlap


def showGraph(dict,show_edge_val,show_edge_dir):

  g = nx.DiGraph()
  g.add_nodes_from(dict.keys())

  for k, v in dict.items():
    for t in v:
      g.add_edge(k, t[0],label=str(t[1]),arrowStrikethrough=not show_edge_val)


  nt = Network('948px', '1888px',directed=show_edge_dir)

  nt.from_nx(g)
  nt.show('graph.html')

def show_path_graph(dict,show_edge_val,show_edge_dir,path):

  g = nx.DiGraph()
  g.add_nodes_from(dict.keys())

  pos = -1
  for k, v in dict.items():
    for i,n in enumerate(path):
      if n == k:
        pos = i
        break
    for t in v:
      try:
        if k == path[pos] and t[0] == path[pos+1]:
          g.add_edge(k, t[0],label=str(t[1]),arrowStrikethrough=not show_edge_val,color = 'red')
        else:
          g.add_edge(k, t[0], label=str(t[1]), arrowStrikethrough=not show_edge_val)
      except:
        g.add_edge(k, t[0], label=str(t[1]), arrowStrikethrough=not show_edge_val)

  nt = Network('948px', '1888px',directed=show_edge_dir)

  nt.from_nx(g)
  nt.show('graph.html')

def dfs(visited, graph, node):
  if node not in visited:
      visited.add(node)
      for neighbour in graph[node]:
          dfs(visited, graph, neighbour[0])
  return visited

#for now greedy_search returns vertices with max value for each node
def get_good_connections(graph,reversed_graph, all_nodes,min_conn):
  best_connection = len(list(graph.keys())[0]) - 1

  good_conns = {}


  for node in all_nodes:


    #all_nodes can include elements not in reversed_graph or graph
    try:
      bcc = [pointing for pointing in reversed_graph[node] if any(c == int(pointing[1]) for c in range(min_conn,best_connection+1))]
    except:
      bcc = []

    try:
      bc = [pointed for pointed in graph[node] if any(c == int(pointed[1]) for c in range(min_conn,best_connection+1))]
    except:
      bc = []

    tmp = bc+bcc
    good_conns[node] = tmp

  return good_conns

def simple_path(good_conns,graph,reversed_graph,all_nodes):
  tmp = [False for _ in range(len(all_nodes))]
  visited = dict(zip(all_nodes,tmp))

  tmp = get_mid_nodes(good_conns)

  node = starting_node(tmp, graph, reversed_graph)
  visited[node] = True

  seq = [node]

  best_next_node(graph, node, visited, seq)
  best_prev_node(reversed_graph,node, visited, seq)

  check_seq = set(seq)

  return seq

#TODO make the code cleaner
def best_next_node(graph,node,visited,seq):

  nd = graph[node]
  maxx = 9
  next = False
  while (not next):
    for i in nd:
      if int(i[1]) == maxx and visited[i[0]] == False and i[0] in graph:
        next = True
        maxx = int(i[1])
        visited[i[0]] = True
        seq.append(i[0])
        best_next_node(graph, i[0], visited, seq)
    maxx -= 1
    if maxx < 1:
      break

def best_prev_node(graph,node,visited,seq):


    nd = graph[node]
    maxx = 9
    next = False
    while (not next):
      for i in nd:
        if int(i[1]) == maxx and visited[i[0]] == False and i[0] in graph:
          next = True
          maxx = int(i[1])
          visited[i[0]] = True
          seq.insert(0,i[0])
          best_prev_node(graph, i[0], visited, seq)
      maxx -= 1
      if maxx < 1:
        break

def starting_node(good_conns,graph,reversed_graph):
  gc = good_conns
  for node in gc:
    for i in good_conns[node]:
      if i in graph[node]:
        if i in reversed_graph[node]:
          return node

def get_mid_nodes(good_conns):
  mid_nodes = {}

  for node in good_conns:
    connected_nodes = []
    for conn in good_conns[node]:
      if int(conn[1]) == 9:
        connected_nodes.append(conn)
    if len(connected_nodes) > 1:
      mid_nodes[node] = connected_nodes

  return mid_nodes


