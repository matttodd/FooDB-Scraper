import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


def main():
    food_df = pd.read_csv('edgelists/food-food_projection.csv')
    chem_df = pd.read_csv('edgelists/chem-chem_projection.csv')
    food_G = nx.Graph()
    chem_G = nx.Graph()
    for index, row in food_df.iterrows():
        food_G.add_edge(row[0], row[1], weight=row[2])
    for index, row in chem_df.iterrows():
        chem_G.add_edge(row[0], row[1], weight=row[2])

    food_d = list(map(lambda x: x[1], nx.degree(food_G)))
    fcc = nx.clustering(food_G)
    chem_d = list(map(lambda x: x[1], nx.degree(chem_G)))
    ccc = nx.clustering(chem_G)

    plt.hist(food_d)
    plt.title('Food Projection Degree Distribution')
    plt.xlabel('Degree')
    plt.savefig('export/proj_food_degree.png')
    plt.close()
    plt.hist(chem_d)
    plt.title('Chemical Projection Degree Distribution')
    plt.xlabel('Degree')
    plt.savefig('export/proj_chem_degree.png')
    plt.close()
    plt.hist(fcc.values())
    plt.title('Food Projection Clustering Distribution')
    plt.xlabel('Clustering')
    plt.savefig('export/proj_food_clustering.png')
    plt.close()
    plt.hist(ccc.values())
    plt.title('Chemical Projection Clustering Distribution')
    plt.xlabel('Clustering')
    plt.savefig('export/proj_chem_clustering.png')
    plt.close()

    print(nx.info(food_G))
    print(nx.info(chem_G))


if __name__ == '__main__':
    main()
