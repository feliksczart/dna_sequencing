from os import read
from src.loader import Loader
import src.graph as g

def main():
    reads = Loader('../res/9.200-40.txt').loadReads()
    min_overlap = 5

    pairs, reversed_pairs = g.pairUp(reads,min_overlap)

    show_edge_val = True
    show_edge_dir = True
    # g.showGraph(pairs, show_edge_val, show_edge_dir)

    visited = set()
    visited = g.dfs(visited, pairs, list(pairs.keys())[0])

    print("Visited: " + str(100*len(visited)/len(pairs.keys())) + "%")

    p = sorted(pairs)
    r = sorted(reversed_pairs)

    if p == r:
        print("pairs and reversed_pairs are the same thing just ordered differently")
    else:
        print("pairs and reversed_pairs are NOT the same thing just ordered differently")



    good_connections = g.get_good_connections(pairs,reversed_pairs,reads,7)
    g.showGraph(good_connections, show_edge_val, False)

if __name__ == "__main__":
    main()