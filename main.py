import json_to_graph, Digraph
import random
import tkinter as tk
from tkinter import ttk
from tkinter_elements import *
from time import time

if __name__ == "__main__":
    # hello groupmates (and maybe examiner)
    # heres the figma file that I used to get the coordinates for ui
    # https://www.figma.com/design/5z95NPKZOqNYSsIcEinEHF/Untitled?node-id=1-7&t=XhewlutMdVN6NP3T-1

    root = tk.Tk()
    root.title("Wikilinks App")

    label = tk.Label(root, text="Loading graph data... this might take a while (~10s).")
    label.pack(pady=10)
    root.update()

    print("Loading graph data... this might take a while (~10s).")
    graph = json_to_graph.get_graph_from_link_data('multi-discipline_data.json')

    # path finder demo
    print(graph.get_shortest_path("Computer_science", "Edging_(sexual_practice)"))

    possible_starts = sorted(graph.get_start_items())
    possible_ends = sorted(graph.get_items())



    frame = tk.Frame(root, width=600, height=200)
    frame.pack()

    # creating text box
    start_link = AutocompleteText(frame, autocomplete = lambda word : [x for x in possible_starts if x.startswith(word)])
    start_link.place(x=24, y=24, height=60, width=238)

    end_link = AutocompleteText(frame, autocomplete = lambda word: [x for x in possible_ends if x.startswith(word)])
    end_link.place(x=338, y=24, height=60, width=238)

    to_text = tk.Label(frame, font=("Helvetica", 24), text="to")
    to_text.place(x=288, y=35)

    def runPath():
        start = start_link.get("0.1", tk.END).strip()
        end = end_link.get("0.1", tk.END).strip()
        print(graph.get_shortest_path(start,  end))

    def randomisePath():
        random_start = random.choice(possible_starts)
        random_end = random.choice(possible_ends)
        start_link.delete("1.0", tk.END)
        start_link.insert(tk.END, random_start)
        end_link.delete("1.0", tk.END)
        end_link.insert(tk.END, random_end)

    button1 = tk.Button(frame, text="Run!", command=runPath)
    button1.place(x=181, y=115, height=34, width=238)

    button2 = tk.Button(frame, text="Randomise Path", command=randomisePath)
    button2.place(x=181, y=150, height=34, width=238)

    root.update()
    root.mainloop()



    # count = 0
    # for p in range(1):
    #     # get random path demo
    #     random_start = random.choice(graph.get_start_items()) # cannot start on a 'leaf' of the graph (no outgoing)
    #     random_end = random.choice(graph.get_items())
    #     path = graph.get_shortest_path(random_start, random_end)
    #     print("Random: ", path)
    #     count += len(path)
    # print("Average path length (n = 1000): ", count/1000)

