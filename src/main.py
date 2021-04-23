from os import read
from loader import Loader
import graph as g

def main():
    reads = Loader('res/9.200-40.txt').load()
    min_overlap = 5

    pairs, reversed_pairs = g.pairUp(reads,min_overlap)
    g.showGraph(pairs)
    # print(pairs)

if __name__ == "__main__":
    main()