path = r"C:\Users\nutta\myProject\FileSystem\templates\gen_graph.html"
json_path = r"C:\Users\nutta\myProject\FileSystem\tfdict.json"

from pyvis.network import Network
import json


def json_to_network(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        tfdict = json.load(f)
    for key, value in tfdict.items():
        net.add_node(key, size=value)
    return net


net = Network()

# net.add_node(0, label="a", id=0)
# net.add_node(1, label="b")
# net.add_edge(0, 1, label="ab", font={"align": "top"}, color="red", width=3)

# net.add_node('A', size=10)
# net.add_node('B', size=20)
# net.add_nodes(['C', 'D', 'E'], size=[30, 40, 50])

# net.add_edge('A','B')
# net.add_edge('A','C')
# net.add_edges([('A','D'), ('B','D'), ('D','E')])

net = json_to_network(json_path)

net.show(path, notebook=False)
