import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from preswald import matplotlib_plot, text, view, table

# Display title
text("# Network Topology Visualizer")
text("Visualize the topology of a network using Matplotlib and NetworkX.")

# Read the CSV file
df = pd.read_csv("data.csv")

# Display the raw data table
table(df, title="Network Devices")

# Create a graph using NetworkX
G = nx.Graph()

# Add nodes and edges based on the CSV data
for _, row in df.iterrows():
    device = row['Device Name']
    connected_to = row['Connected To']
    
    # Add nodes with attributes
    G.add_node(device, 
               ip_address=row['IP Address'], 
               mac_address=row['MAC Address'], 
               connection_type=row['Connection Type'])
    
    # Add edges
    if connected_to in df['Device Name'].values:
        G.add_edge(device, connected_to)

# Create a Matplotlib figure
plt.figure(figsize=(12, 8))

# Use spring layout for node positioning
pos = nx.spring_layout(G, k=0.5, iterations=50)

# Draw the graph
plt.title("Network Topology Visualization", fontsize=16)

# Draw edges
nx.draw_networkx_edges(G, pos, 
                       edge_color='gray', 
                       width=1, 
                       alpha=0.7)

# Draw nodes with color coding based on connection type
connection_colors = {
    'Wired': '#1E90FF',     # Dodger Blue for Wired
    'Wireless': '#32CD32'   # Lime Green for Wireless
}

node_colors = [connection_colors.get(G.nodes[node]['connection_type'], '#808080') 
               for node in G.nodes()]

nx.draw_networkx_nodes(G, pos, 
                       node_color=node_colors, 
                       node_size=800, 
                       alpha=0.9)

# Add labels to nodes
nx.draw_networkx_labels(G, pos, 
                        font_size=10, 
                        font_weight='bold')

# Add a legend for connection types
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', 
               label=conn_type, 
               markerfacecolor=color, 
               markersize=10)
    for conn_type, color in connection_colors.items()
]
plt.legend(handles=legend_elements, 
           title="Connection Type", 
           loc='best')

# Remove axis
plt.axis('off')

# Add device details as annotations
for node, (x, y) in pos.items():
    # Get device details
    device_data = df[df['Device Name'] == node].iloc[0]
    
    # Create annotation text
    annotation_text = (
        f"IP: {device_data['IP Address']}\n"
        f"MAC: {device_data['MAC Address']}"
    )
    
    # Add annotation slightly offset from the node
    plt.annotate(annotation_text, 
                 (x, y), 
                 xytext=(10, 10),
                 textcoords='offset points',
                 bbox=dict(boxstyle='round,pad=0.2', 
                           fc='yellow', 
                           alpha=0.3),
                 fontsize=8)

# Render the plot
matplotlib_plot(plt.gcf())

# Optional: Add some textual insights
text("## Network Insights")
text(f"- Total Devices: {len(G.nodes())}")
text(f"- Wired Devices: {sum(1 for node in G.nodes() if G.nodes[node]['connection_type'] == 'Wired')}")
text(f"- Wireless Devices: {sum(1 for node in G.nodes() if G.nodes[node]['connection_type'] == 'Wireless')}")