from os import read
from loader import Loader
import graph as g

def main():
    reads = Loader('res/9.200-40.txt').loadReads()
    min_overlap = 5

    pairs, reversed_pairs = g.pairUp(reads,min_overlap)

    show_edge_val = True
    show_edge_dir = True
    # g.showGraph(pairs, show_edge_val, show_edge_dir)

    visited = set()
    visited = g.dfs(visited, pairs, list(pairs.keys())[0])

    print("Visited: " + str(100*len(visited)/len(pairs.keys())) + "%")


if __name__ == "__main__":
    main()