from __future__ import annotations
from typing import Any

class Digraph:
    """

    """

    def __init__(self):
        pass

class _Vertex:

    item: Any
    neighbours: set[_Vertex]

    def __init__(self, item: Any, neighbours: set[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours
