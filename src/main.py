from os import read
from src.loader import Loader
import src.graph as g
from os import listdir
from os.path import isfile, join

def main():
    # positive/negative instance filter
    pth = "../res"
    positive_random = [f for f in listdir(pth) if isfile(join(pth, f)) and "+" in f and (f[-4] == '+' or f[-2] == '8')]
    positive_what = [f for f in listdir(pth) if isfile(join(pth, f)) and "+" in f and f[-3] == '+' and f[-2] != '8']
    negative_random = [f for f in listdir(pth) if isfile(join(pth, f)) and "-" in f and f[-1] == '0']
    negative_repeating = [f for f in listdir(pth) if isfile(join(pth, f)) and "-" in f and f[-1] != '0']

    for j in range(9,10):
        print(f"Minimal overlap:  {j}   ~~~~~~~~~~~~~~~~~~")

        for i in positive_what:
            run(i,j)
        print("================================")
        for i in positive_random:
            run(i,j)
        # for i in negative_random:
        #     run(i,j)
        # print("================================")
        # for i in negative_repeating:
        #     run(i,j)
        # run("9.200+80",j)

def run(filename,mo):
    reads = Loader(f'../res/{filename}').loadReads()
    min_overlap = mo

    pairs, reversed_pairs = g.pairUp(reads, min_overlap)

    show_edge_val = True
    show_edge_dir = True
    # g.showGraph(pairs, show_edge_val, show_edge_dir)

    good_connections = g.get_good_connections(pairs, reversed_pairs, reads, 9)
    # g.showGraph(good_connections, show_edge_val, False)

    length = best_path_length(filename)
    path = g.simple_path(good_connections, pairs, reversed_pairs, reads,length)
    print(filename, "  Path length:  " ,len(path), f"/ {length}")
    # g.show_path_graph(pairs, show_edge_val, show_edge_dir, path,filename)

def best_path_length(filename):
    for index, i in enumerate(filename):
        if i == ".":
            length = filename[index+1:index+4]
            break

    if "-" in filename:
        for index, i in enumerate(filename):
            if i == "-":
                return int(length) - int(filename[index+1:])
    else:
        return int(length)




if __name__ == "__main__":
    main()