import json_to_graph, Digraph
import random
import tkinter as tk
from tkinter import ttk
from tkinter_elements import *
from time import time

g = json_to_graph.get_graph_from_link_data("multi-discipline_data.json")

stats = {"num_paths": 0, "shortest_path_length": 0, "time_to_get_shortest_path": 0, "time_to_get_paths": 0, "percent_paths": 0}
for i in range(10):
    start, end = random.choice(g.get_start_items()), random.choice(g.get_items())

    # print(start, end)
    start_time = time()
    paths = g.get_all_paths(start, end)
    end_time = time()
    diff1 = end_time - start_time

    start_time = time()
    shortest_path = g.get_shortest_path(start, end)
    end_time = time()
    diff2 = end_time - start_time

    stats["num_paths"] += len(paths)
    stats["shortest_path_length"] += len(shortest_path)
    stats["time_to_get_shortest_path"] += diff2
    stats["time_to_get_paths"] += diff1
    num_neighbours = len(g.get_vertex(start).get_outgoing())
    percent = round((len(paths)/num_neighbours) * 100, 2)
    stats["percent_paths"] += percent

stats_average = {s:stats[s]/10 for s in stats}
print(stats_average)
