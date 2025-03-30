import csv
import json
from pprint import pprint

from Digraph import Digraph, _Vertex
from urllib.parse import unquote

WIKILINK_PREFIX = ""


def url_to_str(string: str):
    """
    Decode a URL-encoded string and returns the decoded string.
    """
    return unquote(string)


def get_graph_from_link_data(link_path: str) -> Digraph:
    """
    Return a directed graph from the given json of link data, representing all links and linkages in the data.
    """
    graph = Digraph()
    with open(link_path) as json_data:
        data = json.load(json_data)
        json_data.close()

        for link in data:
            add_all_vertices(graph, data, link)

    return graph


def add_all_vertices(graph: Digraph, data: dict, article: str) -> None:
    """
    Add vertices and edges to a Digraph based on the provided link data, modifying the graph in place.
    """
    graph.add_vertex(url_to_str(article.removeprefix(WIKILINK_PREFIX)))

    for link in data[article]:
        add_all_vertices(graph, data[article], link)

        graph.add_edge(url_to_str(article.removeprefix(WIKILINK_PREFIX)), url_to_str(link.removeprefix(WIKILINK_PREFIX)))
        # print("added edge between", article.removeprefix(WIKILINK_PREFIX), link.removeprefix(WIKILINK_PREFIX))


if __name__ == "__main__":
    # print(len(get_graph_from_link_data('multi-discipline_data.json').get_vertex("Computer_science").outgoing))
    pass
