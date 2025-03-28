import json_to_graph, Digraph
import random

if __name__ == "__main__":
    graph = json_to_graph.get_graph_from_link_data('multi-discipline_data.json')

    # path finder demo
    print(graph.get_shortest_path("Moonlight", "Differential_calculus"))

    # get random path demo
    random_start = random.choice(graph.get_start_items()) # cannot start on a 'leaf' of the graph (no outgoing)
    random_end = random.choice(graph.get_items())
    print("Random: ", graph.get_shortest_path(random_start, random_end))

