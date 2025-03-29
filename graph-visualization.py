from networkx.drawing import spring_layout

from Digraph import Digraph
import networkx as nx
import plotly as plt
import plotly.graph_objs as go

class Draw_Graph:
    graph: Digraph

    def __init__(self, graph: Digraph):
        self.graph = graph

    @staticmethod
    def to_networkx(graph: Digraph) -> nx.DiGraph:
        """a"""

        nx_graph = nx.DiGraph()
        for v in graph.get_all_vertices():
            nx_graph.add_node(v)
            inc, out = graph.get_incoming_and_outgoing(v)
            for i in inc:
                nx_graph.add_edge(i, v)
            for o in out:
                nx_graph.add_edge(v, o)

        return nx_graph

    def gen_graph_plot(self) -> tuple:
        """a"""
        nx_graph = Draw_Graph.to_networkx(self.graph)
        pos = getattr(nx, "spring_layout")(nx_graph)
        node_x = [pos[k][0] for k in nx_graph.nodes]
        node_y = [pos[k][1] for k in nx_graph.nodes]
        labels = list(nx_graph.nodes)
        edge_x = []
        edge_y = []
        for edge in nx_graph.edges:
            edge_x += [pos[edge[0]][0], pos[edge[1]][0], None]
            edge_y += [pos[edge[0]][1], pos[edge[1]][1], None]

        # for edge in nx_graph.edges():
        #     x0, y0 = nx_graph.nodes[edge[0]]['pos']
        #     x1, y1 = nx_graph.nodes[edge[1]]['pos']
        #     edge_x.append(x0)
        #     edge_x.append(x1)
        #     edge_x.append(None)
        #     edge_y.append(y0)
        #     edge_y.append(y1)
        #     edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        # node_x = []
        # node_y = []
        # for node in nx_graph.nodes():
        #     x, y = nx_graph.nodes[node]['pos']
        #     node_x.append(x)
        #     node_y.append(y)

        node_trace = go.Scatter(x=node_x,
                                y=node_y,
                                mode='markers',
                                name='nodes',
                                # marker=dict(symbol='circle-dot',
                                #             size=5
                                #             ),
                                text=labels,
                                hovertemplate='%{text}',
                                hoverlabel={'namelength': 0})

        arrow_annotations = []
        for edge in nx_graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            arrow_annotations.append(
                dict(
                    ax=x0, ay=y0, axref='x', ayref='y',
                    x=x1, y=y1, xref='x', yref='y',
                    showarrow=True,
                    arrowhead=3,  # Arrow style
                    arrowsize=2,
                    arrowwidth=1,
                    arrowcolor="black"
                )
            )

        return edge_trace, node_trace, arrow_annotations

    def visualize(self) -> None:
        edge_trace, node_trace, arrow_annotations = self.gen_graph_plot()

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title=dict(
                                text="<br>Network graph made with Python",
                                font=dict(
                                    size=16
                                )
                            ),
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=arrow_annotations,
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )

        fig.show()


if __name__ == "__main__":
    g = Digraph()
    g = g.generate_test_graph()
    draw_graph = Draw_Graph(g)
    draw_graph.visualize()
