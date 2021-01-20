import networkx as nx
import pandas as pd
from collections import defaultdict


def main():
    get_triangle_counts()
    # get_big_triangle()


def get_big_triangle():
    df = pd.read_csv('edgelists/disease_path_reduced_query.csv')
    dis_dis = defaultdict(set)
    pathway = defaultdict(set)
    for index, row in df.iterrows():
        dis_dis[row[0]].add(row[1])
        dis_dis[row[1]].add(row[0])
        pathway[row[2]].add(row[0])
        pathway[row[2]].add(row[1])
    best_path = defaultdict(list)
    for path in pathway:
        if len(best_path) > 25:
            break
        path_cur = []
        for dis in list(pathway[path]):
            cur = [dis]
            for dis2 in list(pathway[path]):
                if dis in dis_dis[dis2]:
                    cur.append(dis2)
            if len(cur) > len(path_cur):
                path_cur = cur

        if len(path_cur) > 200:
            best_path[path].extend(path_cur)

    for path in best_path:
        print("Caffeine", path, len(best_path[path]))


def get_triangle_counts():
    df = pd.read_csv('edgelists/diseases_pathways_chem_edgelist.csv')
    adj = defaultdict(set)
    dis_dis = defaultdict(set)
    triad_cliques = []
    for index, row in df.iterrows():
        if index < 22399:
            adj[row[0]].add(row[1])
        else:
            dis_dis[row[0]].add(row[1])

    for chemical in adj:
        for index, d1 in enumerate(list(adj[chemical])):
            for d2 in list(adj[chemical])[index+1:]:
                if d2 in dis_dis[d1]:
                    print((chemical, d1, d2))
                    triad_cliques.append((chemical, d1, d2))

    print(len(triad_cliques))
    counts = defaultdict(lambda: 0)
    for tri in triad_cliques:
        counts[tri[0]] += 1
    for key, value in sorted(counts.items(), key=lambda x: x[1]):
        print("{} : {}".format(key, value))


if __name__ == '__main__':
    main()
