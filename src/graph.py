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

def show_path_graph(dict,show_edge_val,show_edge_dir,path,filename):

  g = nx.DiGraph()
  g.add_nodes_from(dict.keys())

  pos = False
  for k, v in dict.items():
    for i,n in enumerate(path):
      if n == k:
        pos = i
        break
    for next_node in v:
      try:
        if next_node[0] == path[pos+1]:
          pass
        else:
          g.add_edge(k, next_node[0], label=str(next_node[1]), arrowStrikethrough=not show_edge_val)
      except:
        g.add_edge(k, next_node[0], label=str(next_node[1]), arrowStrikethrough=not show_edge_val)
    pos = None

#drawing path
  for i, conn in enumerate(path):
    try:
      g.add_edge(conn, path[i+1], label=str(" "), arrowStrikethrough=not show_edge_val, color='red',
                 width=10)
    except:
      pass

  nt = Network('948px', '1888px',directed=show_edge_dir)

  nt.barnes_hut(spring_length=2)
  nt.from_nx(g)

  nt.show(f'{filename}.html')

def dfs(visited, graph, node):
  if node not in visited:
      visited.add(node)
      for neighbour in graph[node]:
          dfs(visited, graph, neighbour[0])
  return visited

#returns vertices with value in range for each node
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

def simple_path(good_conns,graph,reversed_graph,all_nodes,max_length):
  tmp = [False for _ in range(len(all_nodes))]
  visited = dict(zip(all_nodes,tmp))

  mid_nodes = get_mid_nodes(good_conns)

  node = starting_node(mid_nodes, graph, reversed_graph, visited)
  visited[node] = True

  seq = [node]

  best_next_node(graph, node, visited, seq)
  best_prev_node(reversed_graph,node, visited, seq)

#finding all the major disconnected graphs
  if len(seq) < max_length:
    sequences = []
    while(True):
      node = starting_node(mid_nodes, graph, reversed_graph, visited)

      if node is None:
        sequences.append(seq)
        sorted_seq = []
        for s in sequences:
          sorted_seq.append((len(s), s))

        sorted_seq.sort(reverse= True)

        seq = []
        for s in sorted_seq:
          if (len(seq) + s[0]) < max_length:
            seq += s[1]
          else:
            return seq

        return seq

      visited[node] = True

      tmps = [node]
      best_next_node(graph, node, visited, tmps)
      best_prev_node(reversed_graph, node, visited, tmps)

      sequences.append(tmps)

  return seq

#TODO make the code cleaner
#recursive function - finds the best next node in a greedy way
#appends the node to the path
def best_next_node(graph,node,visited,seq):

  nd = graph[node]
  maxx = 9
  next = False
  while (not next):
    for i in nd:
      if int(i[1]) == maxx and visited[i[0]] == False and i[0] in graph:
        next = True
        maxx = 0
        visited[i[0]] = True
        seq.append(i[0])
        best_next_node(graph, i[0], visited, seq)
        break

    if maxx < 1:
      break

    for i in nd:
      if int(i[1]) == maxx and visited[i[0]] == False:
        next = True
        maxx = 0
        visited[i[0]] = True
        seq.append(i[0])
        if (i[0] in graph):
          best_next_node(graph, i[0], visited, seq)
        break



    maxx -= 1
    if maxx < 1:
      break

#recursive function - finds the best previous node (from reversed graph) in a greedy way
#puts the node at index 0 of the path list
def best_prev_node(graph,node,visited,seq):

    nd = graph[node]
    maxx = 9
    next = False
    while (not next):
      for i in nd:
        if int(i[1]) == maxx and visited[i[0]] == False and i[0] in graph:
          next = True
          maxx = 0
          visited[i[0]] = True
          seq.insert(0,i[0])
          best_prev_node(graph, i[0], visited, seq)
          break

      if maxx < 1:
        break

      for i in nd:
        if int(i[1]) == maxx and visited[i[0]] == False:
          next = True
          maxx = 0
          visited[i[0]] = True
          seq.insert(0, i[0])
          if (i[0] in graph):
            best_prev_node(graph, i[0], visited, seq)
          break

      maxx -= 1
      if maxx < 1:
        break

def starting_node(good_conns,graph,reversed_graph,visited):
  for node in good_conns:
    if not visited[node]:
      for i in good_conns[node]:
        for j in good_conns[node]:
          try:
            if i in graph[node] and j in reversed_graph[node] and i is not j:
              return node
          except:
            pass
  return None


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



