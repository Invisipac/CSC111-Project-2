

import json_to_graph
import random
from time import time

g = json_to_graph.get_graph_from_link_data("multiple_words_data.json")
ITERS = 10


def get_stats(graph, iterations, start=None, end=None):
    """Given a graph and a number of iterations, if start and end are None, each iteration generate
    a random pair of start and end points and computer a variety of statistics for these nodes
    and return them as a dict.
    If iterations is 1, then also return the list of paths and the shortest path so that they can then be displayed
    in the console

    Preconditions:
        - iterations >= 1

    """
    stats = {"num_paths": 0, "shortest_path_length": 0, "time_to_get_shortest_path": 0, "time_to_get_paths": 0, "percent_paths": 0}
    shortest_path, paths = [], []
    for i in range(iterations):
        if not start or not end:
            start, end = random.choice(graph.get_start_items()), random.choice(graph.get_items())
        # print(start, end)
        start_time = time()
        paths = graph.get_all_paths(start, end)
        # print(len(paths))
        end_time = time()
        diff1 = end_time - start_time

        start_time = time()
        shortest_path = graph.get_shortest_path(start, end)
        end_time = time()
        diff2 = end_time - start_time

        stats["num_paths"] += len(paths)
        stats["shortest_path_length"] += len(shortest_path)
        stats["time_to_get_shortest_path"] += diff2
        stats["time_to_get_paths"] += diff1
        num_neighbours = len(graph.get_vertex(start).get_outgoing())
        percent = round((len(paths)/num_neighbours) * 100, 2)
        stats["percent_paths"] += percent
        # print(stats)

    stats_average = {s: round(stats[s] / iterations, 2) for s in stats}
    stats_average["iterations"] = iterations
    if iterations == 1:
        return stats_average, shortest_path, paths
    return stats_average


def display_path(path: list):
    """Given a list of nodes, display the path that they represent using an arrow '-->'.
     """
    print("\t")
    for n in path[:-1]:
        print(n, end=' --> ')

    print(path[-1])


def display_multiple_paths(paths: list):
    """Display all the paths in the list paths"""
    for p in paths:
        if p:
            display_path(p)


def display_data_for_pair(start, end, graph):
    """Neatly display the data collected for a singular pair of nodes

    Preconditions:
        - start, end in graph.get_all_vertices()

    """
    stats, shortest_path, paths = get_stats(graph, 1, start, end)
    print(f"The nodes {start} and {end}:\n")
    print("\t -----The data measured of the two nodes:-----\n")
    output_results(stats)
    print("\n")
    print("\t -----The shortest path between the two nodes:-----\n")
    display_path(shortest_path)
    print("\n")
    print("\t -----All of the shortest paths between the two nodes:----\n")
    display_multiple_paths(paths)



def output_results(stats: dict):
    """Neatly display all the data in the stats dictionary

    Preconditions:
        - "iterations","num_paths", "shortest_path_length",
        "time_to_get_shortest_path", "time_to_get_paths","percent_paths" in stats

    """
    iterations = stats["iterations"]
    if iterations > 1:
        print(f"Out of {iterations} iterations, on average, every pair of start and end point:\n")

    for s in stats:
        match s:
            case "num_paths":
                print(f"\t- had {stats[s]} shortest paths connecting them.")

            case "shortest_path_length":
                print(f"\t- had a shortest path length of {stats[s]}.")

            case "time_to_get_shortest_path":
                print(f"\t- took {stats[s]} seconds to determine the shortest path.")

            case "time_to_get_paths":
                print(f"\t- took {stats[s]} seconds to determine all of the paths.")

            case "percent_paths":
                print(f"\t- {stats[s]} percent of the starting vertex's neighbours had a path to the ending vertex")


if __name__ == "__main__":
    start, end = random.choice(g.get_start_items()), random.choice(g.get_items())
    display_data_for_pair(start, end, g)
    stats = get_stats(g, ITERS)
    output_results(stats)
