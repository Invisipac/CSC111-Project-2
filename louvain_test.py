from networkx.drawing import spring_layout
from Digraph import Digraph
import networkx as nx
import plotly.graph_objs as go
import time
import json_to_graph
import community as community_louvain  # pip install python-louvain

# For a discrete color palette
import plotly.express as px


class Draw_Graph:
    """ Drawing a Louvain graph with discrete community colors (no arrow annotations). """

    graph: Digraph | nx.DiGraph

    def __init__(self, graph: Digraph | nx.DiGraph):
        self.graph = graph

    @staticmethod
    def to_networkx(graph: Digraph) -> nx.DiGraph:
        """
        Convert a custom Digraph to a NetworkX DiGraph.
        """
        nx_graph = nx.DiGraph()
        for v in graph.get_all_vertices():
            nx_graph.add_node(v)
            inc, out = graph.get_incoming_and_outgoing(v)
            # Add all incoming edges (i -> v)
            for i in inc:
                nx_graph.add_edge(i, v)
            # Add all outgoing edges (v -> o)
            for o in out:
                nx_graph.add_edge(v, o)
        return nx_graph

    def visualize(self) -> None:
        """
        1) Convert the Digraph to a NetworkX graph if needed.
        2) Compute Louvain communities (undirected).
        3) Generate a spring layout.
        4) Create an edge trace (simple lines, no arrows).
        5) Create multiple node traces (one per community) with a discrete color palette.
        6) Show the figure with a legend so communities are clearly labeled.
        """

        # --- 1) Ensure we have a NetworkX graph ---
        if not isinstance(self.graph, nx.DiGraph):
            nx_graph = Draw_Graph.to_networkx(self.graph)
        else:
            nx_graph = self.graph

        # --- 2) Compute Louvain communities (treating the graph as undirected) ---
        undirected_g = nx_graph.to_undirected()
        partition = community_louvain.best_partition(undirected_g)
        # partition is a dict: {node: community_id}

        # --- 3) Compute a spring layout ---
        pos = nx.spring_layout(nx_graph, seed=42)

        # --- Build Edge Trace (simple lines, no arrows) ---
        edge_x = []
        edge_y = []
        for edge in nx_graph.edges:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x += [x0, x1, None]
            edge_y += [y0, y1, None]

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines',
            name='Edges',
            showlegend=False  # Usually we don't need a legend entry for edges
        )

        # --- 5) Create multiple node traces (one per community) ---
        # Group nodes by community
        communities = {}
        for node, comm_id in partition.items():
            communities.setdefault(comm_id, []).append(node)

        # Discrete color palette (e.g. 10 colors).
        # If you have more than 10 communities, colors will repeat.
        color_palette = px.colors.qualitative.Plotly

        node_traces = []
        for i, (comm_id, nodes) in enumerate(communities.items()):
            # choose a color from the palette
            color = color_palette[i % len(color_palette)]

            # gather coordinates for these nodes
            x_coords = [pos[n][0] for n in nodes]
            y_coords = [pos[n][1] for n in nodes]

            node_trace = go.Scatter(
                x=x_coords,
                y=y_coords,
                mode='markers',
                name=f'Community {comm_id}',
                marker=dict(
                    color=color,
                    size=7,
                    line_width=1
                ),
                text=[str(n) for n in nodes],
                hovertemplate='Node: %{text}<extra></extra>'
            )
            node_traces.append(node_trace)

        # --- 6) Build the figure, including all traces ---
        fig = go.Figure(
            data=[edge_trace] + node_traces,
            layout=go.Layout(
                title='Louvain Communities (Undirected Modularity)',
                showlegend=True,  # show the legend for communities
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        )

        fig.show()


if __name__ == "__main__":
    # Example usage
    start = time.time()
    g = json_to_graph.get_graph_from_link_data("multiple_words_data.json")
    end = time.time()
    print("Time to load graph:", end - start, "seconds.")
    subgraph = g.extract_test_subgraph_for_networkx(350)

    # Visualize the subgraph (commented by default if it's large)
    draw_graph = Draw_Graph(subgraph)
    draw_graph.visualize()
