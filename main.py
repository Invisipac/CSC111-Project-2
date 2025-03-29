import json_to_graph, Digraph
import random
import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wikilinks App")

    label = tk.Label(root, text="Loading graph data... this might take a while (~10s).")
    label.pack(pady=10)
    root.update()

    print("Loading graph data... this might take a while (~10s).")
    graph = json_to_graph.get_graph_from_link_data('multi-discipline_data.json')

    # path finder demo
    print(graph.get_shortest_path("Computer_science", "Edging_(sexual_practice)"))


    def checkkey(event):

        value = event.widget.get()
        print(value)

        # get data from l
        if value == '':
            data = l
        else:
            data = []
            for item in l:
                if value.lower() in item.lower():
                    data.append(item)

                    # update data in listbox
        update(data)


    def update(data):

        # clear previous data
        lb.delete(0, 'end')

        # put new data
        for item in data:
            lb.insert('end', item)

            # Driver code


    l = graph.get_start_items()

    # creating text box
    start_link = tk.Entry(root)
    start_link.pack()
    start_link.bind('<KeyRelease>', checkkey)

    # creating list box
    lb = tk.Listbox(root)
    lb.pack()
    update(l)

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

