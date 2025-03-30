from __future__ import annotations
from typing import Any
from collections import deque
import random
import networkx as nx

class Digraph:
    """
    A representation of a directed graph data structure.
    """

    _vertices: dict[Any, _Vertex]

    def __init__(self):
        self._vertices = {}

    def get_all_vertices(self) -> list[Any]:
        return [v for v in self._vertices]

    def get_incoming_and_outgoing(self, v: Any) -> tuple[list[Any], list[Any]]:
        inc, out = [n.item for n in self._vertices[v].incoming], [n.item for n in self._vertices[v].outgoing]
        return inc, out

    @staticmethod
    def generate_test_graph() -> Digraph:
        graph = Digraph()
        wikipedia_topics = [
            "Machine Learning", "Artificial Intelligence", "Data Science",
            "Deep Learning", "Neural Networks", "Computer Vision",
            "Natural Language Processing", "Big Data", "Reinforcement Learning"
        ]

        for topic in wikipedia_topics:
            graph.add_vertex(topic)

        graph.add_edge("Machine Learning", "Artificial Intelligence")
        graph.add_edge("Machine Learning", "Data Science")
        graph.add_edge("Artificial Intelligence", "Deep Learning")
        graph.add_edge("Artificial Intelligence", "Natural Language Processing")
        graph.add_edge("Data Science", "Big Data")
        graph.add_edge("Deep Learning", "Neural Networks")
        graph.add_edge("Neural Networks", "Computer Vision")
        graph.add_edge("Natural Language Processing", "Reinforcement Learning")
        return graph

    def extract_test_subgraph_for_networkx(self, num_paths) -> nx.DiGraph:
        paths = []
        for i in range(num_paths):
            random_start = random.choice(self.get_start_items())  # cannot start on a 'leaf' of the graph (no outgoing)
            random_end = random.choice(self.get_items())
            path = self.get_shortest_path(random_start, random_end)
            # print(path)
            if path:
                print(path, len(path))
                paths.append(path)

        nx_graph = nx.DiGraph()
        for p in paths:
            for i in range(len(p) - 1):
                nx_graph.add_edge(p[i], p[i + 1])

        return nx_graph


    def add_vertex(self, item: Any) -> None:
        """
        Adds a vertex to the digraph.

        >>> graph = Digraph()
        >>> graph.add_vertex("Cool Topic")
        >>> len(graph._vertices)
        1

        :param item:
        :return:
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, set())

    def add_edge(self, start: Any, end: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if start or end do not appear as vertices in this graph.

        Preconditions:
            - start != end

        >>> graph = Digraph()
        >>> graph.add_vertex("Cool Topic")
        >>> graph.add_vertex("Cool Topic 2")
        >>> graph.add_edge("Cool Topic", "Cool Topic 2")
        >>> len(graph._vertices["Cool Topic"].outgoing)
        1
        """
        if start in self._vertices and start in self._vertices:
            start_vertex = self._vertices[start]
            end_vertex = self._vertices[end]

            # Add the new edge (directional)
            start_vertex.add_outgoing_link(end_vertex)
            end_vertex.add_incoming_link(start_vertex)
        else:
            raise ValueError

    def remove_vertex(self, item):
        """ Removes a vertex by item value from the digraph.

        >>> graph = Digraph()
        >>> graph.add_vertex("Cool Topic")
        >>> graph.add_vertex("Cool Topic 2")
        >>> graph.add_edge("Cool Topic", "Cool Topic 2")
        >>> graph.remove_vertex("Cool Topic 2")
        >>> len(graph._vertices)
        1
        >>> "Cool Topic 2" in graph._vertices
        False
        >>> graph.add_vertex("Cool Topic 3")
        >>> graph.add_edge("Cool Topic", "Cool Topic 3")
        >>> graph.remove_vertex("Cool Topic")
        >>> len(graph._vertices)
        1
        >>> "Cool Topic" in graph._vertices
        False
        >>> "Cool Topic 3" in graph._vertices
        True
        """
        vertex = self._vertices[item]

        # remove all incoming connections of the vertex
        for incoming_link in vertex.incoming:
            incoming_link.remove_outgoing_link(vertex)

        self._vertices.pop(item)

    def remove_edge(self, start: Any, end: Any) -> None:
        """ Removes the edge between two items in the digraph.

        >>> graph = Digraph()
        >>> graph.add_vertex("Topic A")
        >>> graph.add_vertex("Topic B")
        >>> graph.add_edge("Topic A", "Topic B")
        >>> graph._vertices["Topic B"] in graph._vertices["Topic A"].outgoing
        True
        >>> graph._vertices["Topic A"] in graph._vertices["Topic B"].incoming
        True
        >>> graph.remove_edge("Topic A", "Topic B")
        >>> graph._vertices["Topic B"] in graph._vertices["Topic A"].outgoing
        False
        >>> graph._vertices["Topic A"] in graph._vertices["Topic B"].incoming
        False
        """

        if start in self._vertices and end in self._vertices and self._vertices[end] in self._vertices[start].outgoing:
            start_vertex = self._vertices[start]
            end_vertex = self._vertices[end]

            start_vertex.remove_outgoing_link(end_vertex)
            end_vertex.remove_incoming_link(start_vertex)
        else:
            raise ValueError

    def shortest_path_length(self, src: Any, dest: Any) -> int:
        """
        Return shortest path from src to dest in graph, return -1 if no path exists
        (Iterative BFS style search)

        >>> graph = Digraph()
        >>> graph.add_vertex("A")
        >>> graph.add_vertex("B")
        >>> graph.add_vertex("C")
        >>> graph.add_vertex("D")
        >>> graph.add_edge("A", "B")
        >>> graph.add_edge("B", "C")
        >>> graph.add_edge("A", "D")
        >>> graph.add_edge("D", "C")
        >>> graph.shortest_path_length("A", "C")
        2
        >>> graph.shortest_path_length("A", "B")
        1
        >>> graph.shortest_path_length("C", "A")
        -1
        """

        queue = deque([(src, 0)])
        visited = set([src])
        while queue:
            cur, d = queue.popleft()
            if cur == dest:
                return d
            for node in self._vertices[cur].outgoing:
                val = node.item
                if val not in visited:
                    queue.append((val, d+1))
        return -1

    def get_shortest_path(self, src: Any, dest: Any) -> list[Any] | None:
        """
        Returns a list representing a path from the src to the destination, as items in the graph. If no
        such path is found, returns None.
        """

        queue = deque([src])
        visited = {src}
        parent = {src: None}

        while queue:
            cur = queue.popleft()

            if cur == dest:
                path = []
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                return path[::-1]

            for node in self._vertices[cur].outgoing:
                val = node.item
                if val not in visited:
                    queue.append(val)
                    visited.add(val)
                    parent[val] = cur

        return None

    def is_path(self, src: Any, dest: Any) -> bool:
        """ Return if there is a valid path from src to dest
            (DFS style search for kosaraju's)
        """

        stack = deque([src])
        visited = set([src])
        while stack:
            cur = stack.pop()
            if cur == dest:
                return True
            for node in self._vertices[cur].outgoing:
                val = node.item
                if val not in visited:
                    stack.append(val)
        return False

    def compute_transpose(self) -> Digraph:
        """ Compute and return the transpose of the graph
            (Where all the edges are flipped)
        """
        transpose = Digraph()

        # add all the nodes to our transpose
        for node in self._vertices:
            transpose.add_vertex(node)

        # reverse all the edges
        for node in self._vertices:
            for neighbours in self._vertices[node].outgoing:
                transpose.add_edge(neighbours.item, node)

        return transpose

    def _dfs(self, src, visited, stack):
        """ Traverses graph and uptades visited and stack
        """
        visited.add(src)
        for neighbour in self._vertices[src].outgoing:
            val = neighbour.item
            if val not in visited:
                self._dfs(val, visited, stack)
        stack.append(src)

    def _fill_order(self, visited, stack):
        """ helper that calls dfs util
        """
        for node in self._vertices:
            if node not in visited:
                self._dfs(node, visited, stack)

    def _dfs_util(self, src, visited, component):
        """ Helper for kosaraju's, checks connected nodes for our tranposed graph
        """
        visited.add(src)
        component.add(src)
        for node in self._vertices[src].outgoing:
            if node.item not in visited:
                self._dfs_util(node.item, visited, component)

    def kosaraju(self):
        """ Return the strongly connected components
        """

        # create empty stack
        stack = deque()
        visited = set()

        self._fill_order(visited, stack)

        transposed_graph = self.compute_transpose()

        visited = set()
        scc = []
        while stack:
            node = stack.pop()
            if node not in visited:
                component = set()
                transposed_graph._dfs_util(node, visited, component)
                scc.append(component)
        return scc

    def __contains__(self, node: Any):
        return node in self._vertices

    def get_vertex(self, item: Any) -> _Vertex:
        """
        Returns the vertex object of a given item in graph.

        Representation Invariant:
        - item in self._vertices
        """
        return self._vertices[item]

    def count_edges(self) -> int:
        """
        Returns the number of directed edges in the graph.
        """

        count = 0
        for vertex in self._vertices:
            count += len(self._vertices[vertex].outgoing)
        return count

    def count_vertices(self) -> int:
        """
       Returns the number of vertices in the graph.
       """
        return len(self._vertices)

    def get_start_items(self) ->  list[Any]:
        """
        Returns a list of items of vertices in the graph which have at least one outgoing connection.
        """
        lst = []

        for ver in self._vertices:
            ver_obj = self._vertices[ver]
            if len(ver_obj.outgoing) != 0:
                lst.append(ver_obj.item)

        return lst

    def get_items(self) -> list[Any]:
        """
        Returns a list of items of vertices in the graph.
        """
        return [self._vertices[vert].item for vert in self._vertices]

class _Vertex:
    item: Any
    incoming: set[_Vertex]
    outgoing: set[_Vertex]

    def __init__(self, item: Any, outgoing: set[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.incoming = set()
        self.outgoing = outgoing

    def add_incoming_link(self, vertex: _Vertex):
        self.incoming.add(vertex)

    def add_outgoing_link(self, vertex: _Vertex):
        self.outgoing.add(vertex)

    def remove_incoming_link(self, vertex):
        self.incoming.remove(vertex)

    def remove_outgoing_link(self, vertex):
        self.outgoing.remove(vertex)
