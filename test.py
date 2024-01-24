import numpy as np
import pandas as pd
import networkx as nx
from pyvis.network import Network
import jaal



data = pd.read_csv("edges.csv", header=None)
data.columns = ["start_node", "end_node"]
print(data.head(10))
net = Network(notebook = True, cdn_resources = "remote",
                bgcolor = "#222222",
                font_color = "white",
                height = "750px",
                width = "100%",
                select_menu=True
                
)
nodes = list(set([*data.start_node,*data.end_node]))
edges = data.values.tolist()
net.add_nodes(nodes)
net.add_edges(edges)
net.show_buttons(filter_=["physics"])
net.show("graph.html")