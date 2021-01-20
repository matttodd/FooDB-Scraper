import networkx as nx
import pandas as pd
import matplotlib as plt
from pylab import *
from bokeh.io import export_png, export_svgs
from bokeh.models import ColumnDataSource, DataTable, TableColumn
import powerlaw


def main():
    df = pd.read_csv('edgelists/tripartite.csv')
    G = nx.Graph()
    for index, row in df.iterrows():
        G.add_edge(row[0], row[1])
        if index < 786:
            nx.set_node_attributes(G, values={row[0]: 0, row[1]: 1}, name="partition")
        else:
            nx.set_node_attributes(G, values={row[1]: 2}, name="partition")

    print(nx.info(G))
    # pos = nx.multipartite_layout(G, subset_key="partition")
    # show()
    hist = nx.degree_histogram(G)
    alpha = powerlaw.Fit(hist).alpha
    print(alpha, alpha+1)
    print(len(G['Caffeine']))
    generate_subgraph_stats(G)


def generate_attribute_stats(G):
    parts = nx.get_node_attributes(G, "partition")

    foods = list(filter(lambda x: parts[x] == 0, G.nodes()))
    chems = list(filter(lambda x: parts[x] == 1, G.nodes()))
    disease = list(filter(lambda x: parts[x] == 2, G.nodes()))
    print(len(foods), len(chems), len(disease))

    food_d = list(map(lambda x: x[1], nx.degree(G, foods)))
    chem_d = list(map(lambda x: x[1], nx.degree(G, chems)))
    disease_d = list(map(lambda x: x[1], nx.degree(G, disease)))
    print(max(nx.degree(G, foods), key=lambda x: x[1]))
    print(max(nx.degree(G, chems), key=lambda x: x[1]))
    print(max(nx.degree(G, disease), key=lambda x: x[1]))

    fig, axs = plt.subplots(1, 3, tight_layout=True)
    axs[0].hist(food_d)
    axs[0].set_title('Food Degree')
    axs[1].hist(chem_d)
    axs[1].set_title('Chemical Degree')
    axs[2].hist(disease_d)
    axs[2].set_title('Disease Degree')
    plt.show()


def generate_subgraph_stats(G):
    parts = nx.get_node_attributes(G, "partition")

    foods = list(filter(lambda x: parts[x] == 0, G.nodes()))
    chems = list(filter(lambda x: parts[x] == 1, G.nodes()))
    disease = list(filter(lambda x: parts[x] == 2, G.nodes()))
    food_chem = G.subgraph(foods + chems)
    chem_disease = G.subgraph(chems + disease)
    print(len(foods), len(chems), len(disease))

    food_d = list(map(lambda x: x[1], nx.degree(food_chem, foods)))
    chem_food_d = list(map(lambda x: x[1], nx.degree(food_chem, chems)))
    chem_disease_d = list(map(lambda x: x[1], nx.degree(chem_disease, chems)))
    disease_d = list(map(lambda x: x[1], nx.degree(chem_disease, disease)))
    print(mean(food_d))
    print(mean(chem_food_d))
    print(mean(chem_disease_d))
    print(mean(disease_d))
    sort_food = sorted(nx.degree(food_chem, foods), key=lambda x: x[1], reverse=True)
    sort_food_chem = sorted(nx.degree(food_chem, chems), key=lambda x: x[1], reverse=True)
    sort_food_disease = sorted(nx.degree(chem_disease, chems), key=lambda x: x[1], reverse=True)
    sort_disease = sorted(nx.degree(chem_disease, disease), key=lambda x: x[1], reverse=True)

    # fig, axs = plt.subplots(1, 4, tight_layout=True)
    # axs[0].hist(food_d)
    # axs[0].set_title('Food Degree')
    # axs[1].hist(chem_food_d)
    # axs[1].set_title('Chemical Food Degree')
    # axs[2].hist(chem_disease_d)
    # axs[2].set_title('Chemical Disease Degree')
    # axs[3].hist(disease_d)
    # axs[3].set_title('Disease Degree')
    # plt.show()

    tab = {"food": [], "food_degree": [], "chemical_food": [], "chemical_food_degree": [], "chemical_disease": [],
           "chemical_disease_degree": [], "disease": [], "disease_degree": []}
    # for i in range(10):
    #     tab["food"].append(sort_food[i][0])
    #     tab["food_degree"].append(sort_food[i][1])
    #     tab["chemical_food"].append(sort_food_chem[i][0])
    #     tab["chemical_food_degree"].append(sort_food_chem[i][1])
    #     tab["chemical_disease"].append(sort_food_disease[i][0])
    #     tab["chemical_disease_degree"].append(sort_food_disease[i][1])
    #     tab["disease"].append(sort_disease[i][0])
    #     tab["disease_degree"].append(sort_disease[i][1])
    # degree_df = pd.DataFrame(data=tab)
    # save_df_as_image(degree_df, "export/degree_table.png")


def save_df_as_image(df, path):
    source = ColumnDataSource(df)
    df_columns = []
    df_columns.extend(df.columns.values)
    columns_for_table = []
    for column in df_columns:
        columns_for_table.append(TableColumn(field=column, title=column))

    data_table = DataTable(source=source, columns=columns_for_table, index_position=None, width=1600, height=280)
    export_png(data_table, filename=path)


if __name__ == '__main__':
    main()
