import networkx as nx

# Create a graph object
G = nx.Graph()

# Add nodes to the graph
G.add_node(1)
G.add_node(2)
G.add_node(3)

# Add edges to the graph
G.add_edge(1, 2)
G.add_edge(2, 3)

# Set the initial status of the nodes and edges
nx.set_node_attributes(G, "idle", "status")
nx.set_edge_attributes(G, "idle", "status")

# Define a function to update the status of a node or edge
def update_status(obj, status):
  obj["status"] = status

# Define a function to transmit a packet through the network
def transmit_packet(G, packet, source, target):
  # Find the shortest path from the source to the target
  path = nx.shortest_path(G, source, target)

  # Update the status of the source node
  update_status(G.nodes[source], "transmitting")

  # Transmit the packet along the path
  for i in range(len(path) - 1):
    # Update the status of the current edge
    update_status(G[path[i]][path[i+1]], "transmitting")

    # Update the status of the next node
    update_status(G.nodes[path[i+1]], "receiving")

  # Update the status of the target node
  update_status(G.nodes[target], "received")

# Send a packet from node 1 to node 3
packet = "Hello, World!"
transmit_packet(G, packet, 1, 3)

# Print the status of the nodes and edges
print("Node status:")
print(nx.get_node_attributes(G, "status"))
print("Edge status:")
print(nx.get_edge_attributes(G, "status"))