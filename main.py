"""CSC111 Project 2 WikiMap Team

Module Description
==================
This module runs the WikiMap app and provides helper functions to access all other functionality of the project.


Copyright and Usage Information
===============================
This file is Copyright (c) 2025 CSC111 WikiMap Team
"""

import python_ta
import json_to_graph
import random
from tkinter_elements import *
import graph_visualization as vis
import louvain_test as louvain
import stats

if __name__ == "__main__":
    # hello groupmates (and maybe examiner)
    # heres the figma file that I used to get the coordinates for ui
    # https://www.figma.com/design/5z95NPKZOqNYSsIcEinEHF/Untitled?node-id=1-7&t=XhewlutMdVN6NP3T-1

    root = tk.Tk()
    root.title("WikiMap App")

    label = tk.Label(root, text="Loading graph data... this might take a while (~10s).")
    label.pack(pady=10)
    root.update()

    print("Loading graph data... this might take a while (~10s).")
    graph = json_to_graph.get_graph_from_link_data('multi-discipline_data.json')
    show_advanced_stats = tk.IntVar()

    # Update label once graph has loaded
    label.config(text="Graph loaded!")
    root.update()

    possible_starts = sorted(graph.get_start_items())
    possible_starts = [start.replace("_", " ") for start in possible_starts]

    possible_ends = sorted(graph.get_items())
    possible_ends = [end.replace("_", " ") for end in possible_ends]

    frame = tk.Frame(root, width=600, height=240)
    frame.pack()

    # creating text box
    start_link = AutocompleteText(frame, autocomplete=lambda word: [x for x in possible_starts if x.startswith(word)])
    start_link.place(x=24, y=24, height=60, width=238)

    end_link = AutocompleteText(frame, autocomplete=lambda word: [x for x in possible_ends if x.startswith(word)])
    end_link.place(x=338, y=24, height=60, width=238)

    to_text = tk.Label(frame, font=("Helvetica", 24), text="to")
    to_text.place(x=288, y=35)

    path_label = tk.Label(frame, text="", wraplength=500)
    path_label.place(x=24, y=180, width=552)


    def beautify_list(path: list) -> str:
        string = ""
        for item in path:
            string += item.replace("_", " ")
            string += " ⮕ "
        return string[:-2]


    def run_path() -> None:
        start = start_link.get("0.1", tk.END).strip()
        end = end_link.get("0.1", tk.END).strip()

        if start in possible_starts and end in possible_ends:
            start = start.replace(" ", "_")
            end = end.replace(" ", "_")
            path_label.config(text=beautify_list(graph.get_shortest_path(start, end)))
            path_label.update()

            if show_advanced_stats.get() == 1:
                print(stats.display_data_for_pair(start, end, graph))


    def randomise_path() -> None:
        random_start = random.choice(possible_starts)
        random_end = random.choice(possible_ends)

        start_link.delete("1.0", tk.END)
        start_link.insert(tk.END, random_start)
        end_link.delete("1.0", tk.END)
        end_link.insert(tk.END, random_end)


    def graph_visualisation() -> None:
        label.config(text="Visualising graph may take upwards of 1-3 minutes."
                          "\nCheck the console to see articles being added, and PyCharm plots to see the finished graph.")
        label.update()

        subgraph = graph.extract_test_subgraph_for_networkx(150)
        draw_graph = vis.Draw_Graph(subgraph)
        draw_graph.visualize()


    def louvain_visualisation() -> None:
        label.config(text="Calculating communities may take upwards of 1 minute."
                          "\nCheck the console to see articles being added, and PyCharm plots to see the finished graph.")
        label.update()

        subgraph = graph.extract_test_subgraph_for_networkx(150)
        draw_graph = louvain.DrawGraph(subgraph)
        draw_graph.visualize()


    button1 = tk.Button(frame, text="Run!", command=run_path, bg='light green')
    button1.place(x=21, y=135, height=34, width=122)

    button2 = tk.Button(frame, text="Randomise Path", command=randomise_path, bg='light green')
    button2.place(x=166, y=135, height=34, width=122)

    see_graph = tk.Button(frame, text="See Graph", command=graph_visualisation, bg='gray')
    see_graph.place(x=145 + 166, y=135, height=34, width=122)

    see_communities = tk.Button(frame, text="See Communities", command=louvain_visualisation, bg='gray')
    see_communities.place(x=166 + 145 + 145, y=135, height=34, width=122)
    #
    # python_ta.check_all(config={
    #     'extra-imports': [],  # the names (strs) of imported modules
    #     'allowed-io': [],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 120
    # })

    extended_stats_button = tk.Checkbutton(frame, text="Advanced Stats (in console, " +
                                                       "this can take a loooong time, recommended only once)",
                                           variable=show_advanced_stats,
                                           onvalue=1,
                                           offvalue=0)
    extended_stats_button.place(x=70, y=100)

    root.update()
    root.mainloop()
