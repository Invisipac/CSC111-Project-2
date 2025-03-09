from __future__ import annotations
from typing import Any


class Digraph:
    """
    A representation of a directed graph data structure.
    """

    _vertices: dict[Any, _Vertex]

    def __init__(self):
        self._vertices = {}

    def add_vertex(self, item: Any):
        self._vertices[item] = _Vertex(item, set())

    def add_edge(self, start: Any, end: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if start or end do not appear as vertices in this graph.

        Preconditions:
            - start != end
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
        vertex = self._vertices[item]
        # remove all incoming connections of the vertex
        for incoming_link in vertex.incoming:
            incoming_link.remove_outgoing_link()

        self._vertices.pop(item)

    def remove_edge(self, start: Any, end: Any) -> None:
        if start in self._vertices and start in self._vertices:
            start_vertex = self._vertices[start]
            end_vertex = self._vertices[end]

            start_vertex.remove_outgoing_link(end_vertex)
            end_vertex.remove_incoming_link(start_vertex)
        else:
            raise ValueError

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
