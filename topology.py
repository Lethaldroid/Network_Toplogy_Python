import networkx as nx
import matplotlib.pyplot as plt
import random
import time

# Define a function to update the status of a node or edge
def update_status(obj, status):
  obj["status"] = status
  
#get status of node
def get_status(obj):
    return obj["status"]



# Define a function to transmit a packet through the network
def transmit_packet(G, packet, source, target):
  # Find the shortest path from the source to the target
  path = nx.dijkstra_path(G, source, target)
#   path_edges = list(zip(path,path[1:]))

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

packet = "Hello, World!"

# Create an empty graph
G = nx.Graph()
# Define the positions of the nodes in the rectangle
pos = {}
Avg_total_Overhead = 0
bs1 = 1
bs2 = 2
no_packets = 11
delivery_ratio = 0
delivered_packets = 0
source_node = random.randint(3,30) # can be made random
destination_node = source_node+70 # can be made random

# Set the initial status of the nodes and edges
nx.set_node_attributes(G, "idle", "status")
nx.set_edge_attributes(G, "idle", "status")

# Add 98 nodes to the graph
for i in range(1, 101):
    if i == destination_node:
        G.add_node(destination_node, size=10, color='red', interfaces=['eth0', 'eth1', 'eth2'])
    elif i== source_node:
        G.add_node(source_node, size=10, color='red', interfaces=['eth0', 'eth1', 'eth2'])
    elif i == bs1:
        G.add_node(bs1, size=10, color='green', interfaces=['eth0', 'eth1', 'eth2','eth3','eth4'])
    elif i == bs2:
        G.add_node(bs2, size=10, color='green', interfaces=['eth0', 'eth1', 'eth2','eth3','eth4'])
    else:
        G.add_node(i, interfaces=['eth0', 'eth1', 'eth2', 'eth3', 'eth4'])


# Define a dictionary that maps each node to the number of free interfaces it has
free_interfaces = {}

# Iterate through all of the nodes in the graph
for i in G.nodes():
    # Assume that all of the interfaces are free
    free_interfaces[i] = len(G.nodes[i]['interfaces'])

# connect base stations with each other
G.add_edge(bs1, bs2, weight = (1 / 15))

#decrement free interfaces of base stations
free_interfaces[bs1] -= 1
free_interfaces[bs2] -= 1

# Iterate through all of the nodes in the graph
for i in G.nodes():
    # Compare the number of free interfaces for the current node to the other nodes in the graph
    for j in G.nodes():
        if i == j:
            continue
        if(free_interfaces[i] == 0):
            break
        if free_interfaces[j] != 0:
            # if the node is a base station, then add an edge with weight 1/15
            if i == bs1 or i == bs2:
                G.add_edge(i, j, weight = (1 / 15))
                free_interfaces[i] -= 1
                free_interfaces[j] -= 1
                continue
            # Add an edge between the two nodes
            G.add_edge(i, j, weight = 1 / random.randint(1, 15))
            free_interfaces[i] -= 1
            free_interfaces[j] -= 1


# connect base stations with each other
G.add_edge(bs1, bs2, weight = (1 / 15))

shortest_path = nx.dijkstra_path(G, source_node, destination_node)
send = []
receive = []
# send 10 packets from source to destination and save the state of source and destination in each list

for i in range(no_packets):
    transmit_packet(G, packet, source_node, destination_node)
    send.append(get_status(G.nodes[source_node]))
    # add a delay of 5 seconds in the execution of code
    receive.append(get_status(G.nodes[destination_node]))
    
path_edges = list(zip(shortest_path,shortest_path[1:]))

for i in range(no_packets):
    if send[i] == "transmitting" and receive[i] == "received":
        delivered_packets += 1
delivery_ratio = (delivered_packets/no_packets) * 100
        

print("-----------Details---------")
# Print the path and the total weight
print(f"Shortest path: {shortest_path}")
print()
print("Node status:")
print()
print(nx.get_node_attributes(G, "status"))
print("Edge status:")
print()
print(nx.get_edge_attributes(G, "status"))
print(f"Number of Hops: {len(shortest_path)-1}")
print(f"Number of Hello packet sent: {no_packets}")
print(f"Delivery Ratio: {delivery_ratio} %")


cos = nx.random_layout(G)
fixed_pos = {bs1: (0.10, 0.5), bs2: (0.90, 0.5)}
cos.update(fixed_pos)

nx.draw(G, cos,with_labels=True)
nx.draw_networkx_edges(G, cos,edgelist=path_edges,edge_color='r',width= 3)
nx.draw_networkx_nodes(G, cos, nodelist=[source_node, destination_node], node_color='red')
nx.draw_networkx_nodes(G, cos, nodelist=[bs1,bs2], node_color='yellow')

# Show the plot
plt.show()