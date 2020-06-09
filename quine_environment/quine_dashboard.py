from collections import deque

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from draw_tree import buchheim

RED = '#ff0000'
GREEN = '#00ff00'


class Tree:
    def __init__(self, hash, parent, livable):
        self.hash = hash
        self.parent = parent
        self.livable = livable
        self.children = []

    def __repr__(self):
        return self.hash


def create_tree(hash, quine_dict):
    node = Tree(hash, None, quine_dict[hash].livable)
    for child_hash in quine_dict[hash].children:
        node.children.append(create_tree(child_hash, quine_dict))

    return node


def build_tree(quine_info):
    raw_tree = create_tree(quine_info.root_hash, quine_info.quine_dict)
    return buchheim(raw_tree)


class QuineDashboard:
    def __init__(self, quine_info):
        self.quine_info = quine_info

        app = dash.Dash(__name__)
        app.layout = html.Div(
            children=[
                dcc.Interval(id='interval-component',
                             interval=1 * 1000,
                             n_intervals=0),
                html.Div(children=[dcc.Graph(id='live-update-graph-bar')]),
            ]
        )

        app.callback(Output('live-update-graph-bar', 'figure'), [Input('interval-component', 'n_intervals')])(
            self.update_graph)

        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
        app.run_server(debug=True)

    def update_graph(self, _n_intervals):
        print("Dasboard", len(self.quine_info.quine_dict), self.quine_info.root_hash)

        node_xs, node_ys, node_labels, node_colors, edge_xs, edge_ys = self.get_nodes()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edge_xs,
                                 y=edge_ys,
                                 mode='lines',
                                 name='ancestry',
                                 line=dict(color='rgb(210,210,210)', width=3),
                                 hoverinfo='none'
                                 ))
        fig.add_trace(go.Scatter(x=node_xs,
                                 y=node_ys,
                                 mode='markers',
                                 name='quine',
                                 marker=dict(symbol='circle-dot',
                                             size=18,
                                             color=node_colors,
                                             line=dict(color='rgb(50,50,50)', width=1)
                                             ),
                                 text=node_labels,
                                 hoverinfo='text',
                                 opacity=0.8
                                 ))

        fig['layout']['yaxis']['autorange'] = "reversed"
        return fig

    def get_nodes(self):
        quine_tree = build_tree(self.quine_info)

        # node coordinates
        node_xs = []
        node_ys = []
        node_labels = []
        node_colors = []

        # edge coordinates
        edge_xs = []
        edge_ys = []

        print("Get coordinates")

        next_nodes = deque()
        next_nodes.append(quine_tree)
        while next_nodes:
            current_node = next_nodes.pop()
            print(f"x: {current_node.x}, y: {current_node.y}, {current_node.tree}")
            node_xs.append(current_node.x)
            node_ys.append(current_node.y)
            node_labels.append(current_node.tree.hash)
            node_colors.append(GREEN if current_node.tree.livable else RED)

            for child_node in current_node.children:
                next_nodes.append(child_node)
                edge_xs += [current_node.x, child_node.x, None]  # None is for the separator
                edge_ys += [current_node.y, child_node.y, None]

        return node_xs, node_ys, node_labels, node_colors, edge_xs, edge_ys
