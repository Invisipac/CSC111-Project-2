import csv
import json
from pprint import pprint

from Digraph import Digraph, _Vertex

WIKILINK_PREFIX = "/wiki/"


def get_graph_from_link_data(link_path: str):
    #this isnt done
    graph = Digraph()
    with open(link_path) as json_data:
        data = json.load(json_data)
        json_data.close()

        for link in data:
            add_all_vertices(graph, data, link)


def add_all_vertices(graph, data, article):
    graph.add_vertex(article.remove_prefix(WIKILINK_PREFIX))

    for link in data[article]:
        graph.add_vertex(graph, data[article][link], link)



if __name__ == "__main__":
    get_graph_from_link_data('graph_data_test.json')
