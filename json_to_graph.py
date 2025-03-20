import csv
import json
from pprint import pprint

from Digraph import Digraph, _Vertex

WIKILINK_PREFIX = "/wiki/"


def get_graph_from_link_data(link_path: str):
    graph = Digraph()
    with open(link_path) as json_data:
        data = json.load(json_data)
        json_data.close()

        for link in data:
            add_all_vertices(graph, data, link)

    return graph


def add_all_vertices(graph, data, article):
    graph.add_vertex(article.removeprefix(WIKILINK_PREFIX))

    for link in data[article]:
        add_all_vertices(graph, data[article], link)
        graph.add_edge(article.removeprefix(WIKILINK_PREFIX), link.removeprefix(WIKILINK_PREFIX))
        # print("added edge bbetween", article.removeprefix(WIKILINK_PREFIX), link.removeprefix(WIKILINK_PREFIX))


if __name__ == "__main__":
    print(len(get_graph_from_link_data('graph_data_test.json').get_vertex("Computer_science").outgoing))
