from os import read
from src.loader import Loader
import src.graph as g
from os import listdir
from os.path import isfile, join
import time
import json



def main():
    # positive/negative instance filter
    pth = "../res"
    positive_random = [f for f in listdir(pth) if isfile(join(pth, f)) and "+" in f and (f[-4] == '+' or f[-2] == '8')]
    positive_what = [f for f in listdir(pth) if isfile(join(pth, f)) and "+" in f and f[-3] == '+' and f[-2] != '8']
    negative_random = [f for f in listdir(pth) if isfile(join(pth, f)) and "-" in f and f[-1] == '0']
    negative_repeating = [f for f in listdir(pth) if isfile(join(pth, f)) and "-" in f and f[-1] != '0']

    all_files = [f for f in listdir(pth) if isfile(join(pth, f))]

    results = {}
    results = resultss(all_files, results)


    for j in range(3,10):
        print(f"Minimal overlap:  {j}   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        for i in positive_what:
            run(i,j,results)
        print("===========================================")
        for i in positive_random:
            run(i,j,results)
        print("===========================================")
        for i in negative_random:
            run(i,j,results)
        print("===========================================")
        for i in negative_repeating:
            run(i,j,results)
        print("===========================================")
        # run("62.400+160",j,results)

    with open("results.json", "w") as outfile:
        json.dump(results, outfile)

def run(filename,mo,results):
    reads = Loader(f'../res/{filename}').loadReads()
    min_overlap = mo

    length = best_path_length(filename)

    begin_time = time.time()
    pairs, reversed_pairs = g.pairUp(reads, min_overlap)

    show_edge_val = True
    show_edge_dir = True
    # g.showGraph(pairs, show_edge_val, show_edge_dir)

    good_connections = g.get_good_connections(pairs, reversed_pairs, reads, 9)
    # g.showGraph(good_connections, show_edge_val, False)


    path = g.simple_path(good_connections, pairs, reversed_pairs, reads,length)

    elapsed_time = time.time() - begin_time
    print(filename, "  Path length:  " ,len(path), f"/ {length}  Time: {round(elapsed_time,4)}")
    # g.show_path_graph(pairs, show_edge_val, show_edge_dir, path,filename)

    results[filename]['path'][mo] = len(path)
    results[filename]['time'][mo] = round(elapsed_time,4)
    results[filename]['length'] = length


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

def resultss(filenames, results):
    for f in filenames:
        results[f] = {}
        results[f]['path'] = {}
        results[f]['time'] = {}
        results[f]['length'] = {}
        for mo in range(3, 10):
            results[f]['path'][mo] = {}
            results[f]['time'][mo] = {}
    return results


if __name__ == "__main__":
    main()