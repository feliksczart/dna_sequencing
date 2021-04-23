from os import read
from loader import Loader
import graph as g

def main():
    reads = Loader('res/9.200-40.txt').load()
    pairs, reversed_pairs = g.pairUp(reads)

    print(pairs)

if __name__ == "__main__":
    main()