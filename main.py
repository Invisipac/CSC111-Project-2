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


# if __name__ == "__main__":
#     root = tk.Tk()
#     root.title("Wikilinks App")
#
#     label = tk.Label(root, text="Loading graph data... this might take a while (~10s).")
#     label.pack(pady=10)
#     root.update()
#
#     print("Loading graph data... this might take a while (~10s).")
#     graph = json_to_graph.get_graph_from_link_data('multiple_words_data.json')
#
#     # path finder demo
#     print(graph.get_shortest_path("Computer_science", "Edging_(sexual_practice)"))
#
#     # Update label once graph has loaded
#     label.config(text="Graph loaded!")
#     root.update()
#
#     s = sorted(graph.get_start_items())
#     s2 = sorted(graph.get_items())
#
#     frame = tk.Frame(root, width=600, height=160)
#     frame.pack()
#
#     # creating text box
#     start_link = AutocompleteText(frame, autocomplete = lambda word : [x for x in s if x.startswith(word)])
#     start_link.place(x=10, y=10, height=60, width=240)
#
#     end_link = AutocompleteText(frame, autocomplete = lambda word: [x for x in s2 if x.startswith(word)])
#     end_link.place(x=330, y=10, height=60, width=240)
#
#     def runPath():
#         start = start_link.get("0.1", tk.END).strip()
#         end = end_link.get("0.1", tk.END).strip()
#         print(graph.get_shortest_path(start,  end))
#
#     button1 = tk.Button(frame, text="Run!", command=runPath)
#     button1.place(x=10, y=70, height=30, width=100)
#
#     root.update()
#     root.mainloop()



    # count = 0
    # for p in range(1):
    #     # get random path demo
    #     random_start = random.choice(graph.get_start_items()) # cannot start on a 'leaf' of the graph (no outgoing)
    #     random_end = random.choice(graph.get_items())
    #     path = graph.get_shortest_path(random_start, random_end)
    #     print("Random: ", path)
    #     count += len(path)
    # print("Average path length (n = 1000): ", count/1000)
