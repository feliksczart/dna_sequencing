from pyvis.network import Network
import networkx as nx
import numpy as np

def pairUp(reads,min_overlap):
  pairs = {}
  reversed_pairs = {}

  for i in range(len(reads)):
    for j in range(len(reads)):

      if (j == i):
        continue
      
      r1, r2 = reads[i], reads[j]
      o = calculate_overlap(r1,r2)
      o_rev = calculate_overlap(r2,r1)

      if (o >= min_overlap):
        if r1 not in pairs:
          pairs[r1] = np.array([[r2,o]],dtype=object)
        else:
          pairs[r1] = np.concatenate((pairs[r1], [[r2,o]]))

      if (o_rev >= min_overlap):
        if r2 not in reversed_pairs:
          reversed_pairs[r2] = np.array([[r1,o_rev]],dtype=object)
        else:
          reversed_pairs[r2] = np.concatenate((reversed_pairs[r2], [[r1,o_rev]]))

  return pairs, reversed_pairs

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


def showGraph(dict):

  g = nx.DiGraph()
  g.add_nodes_from(dict.keys())

  for k, v in dict.items():
    g.add_edges_from(([(k, t[0]) for t in v]))

  # for k, v in dict.items():
  #   for t in v:
  #     g.add_weighted_edges(k, t[0],weight=str(t[1]))


  nt = Network('1500px', '1500px')

  nt.from_nx(g)
  nt.show('graph.html')