from os import read
from src.loader import Loader
import src.graph as g
from os import listdir
from os.path import isfile, join

def main():
    pth = "../res"
    files = [f for f in listdir(pth) if isfile(join(pth, f))]
    # positive/negative instance filter
    positive_random = [f for f in listdir(pth) if isfile(join(pth, f)) and "+" in f and (f[-4] == '+' or f[-2] == '8')]
    positive_what = [f for f in listdir(pth) if isfile(join(pth, f)) and "+" in f and f[-3] == '+' and f[-2] != '8']
    negative_radnom = [f for f in listdir(pth) if isfile(join(pth, f)) and "-" in f and f[-1] == '0']
    negative_repeating = [f for f in listdir(pth) if isfile(join(pth, f)) and "-" in f and f[-1] != '0']

    for i in positive_what:
        run(i)
    print("================================")
    for i in positive_random:
        run(i)
    # run("9.200+20")

    # for i in files[:6]:
    #
    #
    #     #positive/negative instance filter
    #     if ("+" in i):
    #         continue
    #
    #     print(i)
    #
    #     reads = Loader(f'../res/{i}').loadReads()
    #     reads = Loader(f'../res/144.500-12').loadReads()
    #     min_overlap = 5
    #
    #     pairs, reversed_pairs = g.pairUp(reads,min_overlap)
    #
    #     show_edge_val = True
    #     show_edge_dir = True
    #     # g.showGraph(pairs, show_edge_val, show_edge_dir)
    #
    #     # visited = set()
    #     # visited = g.dfs(visited, pairs, list(pairs.keys())[0])
    #     #
    #     # print("Visited: " + str(100*len(visited)/len(pairs.keys())) + "%")
    #     #
    #     # p = sorted(pairs)
    #     # r = sorted(reversed_pairs)
    #     #
    #     # if p == r:
    #     #     print("pairs and reversed_pairs are the same thing just ordered differently")
    #     # else:
    #     #     print("pairs and reversed_pairs are NOT the same thing just ordered differently")
    #
    #
    #
    #     good_connections = g.get_good_connections(pairs,reversed_pairs,reads,6)
    #     # g.showGraph(good_connections, show_edge_val, False)
    #
    #
    #     path = g.simple_path(good_connections,pairs,reversed_pairs,reads)
    #     g.show_path_graph(pairs, show_edge_val, show_edge_dir,path)

def run(filename):
    reads = Loader(f'../res/{filename}').loadReads()
    min_overlap = 9

    pairs, reversed_pairs = g.pairUp(reads, min_overlap)

    show_edge_val = True
    show_edge_dir = True
    # g.showGraph(pairs, show_edge_val, show_edge_dir)

    good_connections = g.get_good_connections(pairs, reversed_pairs, reads, 9)
    # g.showGraph(good_connections, show_edge_val, False)

    path = g.simple_path(good_connections, pairs, reversed_pairs, reads)
    print(filename, "  Path length:  " ,len(path))
    # g.show_path_graph(pairs, show_edge_val, show_edge_dir, path,filename)

if __name__ == "__main__":
    main()