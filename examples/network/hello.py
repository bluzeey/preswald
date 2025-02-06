import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import sys
import traceback
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/preswald_network_debug.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

from preswald import matplotlib_plot, text, view, table

def debug_environment():
    """Check and log environment details"""
    logger.info("Python Executable: %s", sys.executable)
    logger.info("Python Version: %s", sys.version)
    logger.info("Current Working Directory: %s", os.getcwd())
    
    # Check key dependencies
    try:
        import pandas as pd
        logger.info("Pandas Version: %s", pd.__version__)
    except ImportError:
        logger.error("Pandas not installed")
    
    try:
        import matplotlib
        logger.info("Matplotlib Version: %s", matplotlib.__version__)
    except ImportError:
        logger.error("Matplotlib not installed")
    
    try:
        import networkx as nx
        logger.info("NetworkX Version: %s", nx.__version__)
    except ImportError:
        logger.error("NetworkX not installed")

def main():
    try:
        # Debug environment
        debug_environment()

        # Display title
        text("# Network Topology Visualizer")
        text("Visualize the topology of a network using Matplotlib and NetworkX.")

        # Read the CSV file with extensive error handling
        logger.info("Attempting to read data.csv")
        try:
            # Use absolute path to ensure file is found
            import os
            csv_path = os.path.join(os.getcwd(), 'data.csv')
            logger.info(f"Attempting to read CSV from: {csv_path}")
            
            df = pd.read_csv(csv_path)
            logger.info(f"CSV loaded successfully. Rows: {len(df)}")
            logger.info(f"DataFrame columns: {df.columns}")
            logger.info(f"First few rows:\n{df.head()}")
        except FileNotFoundError:
            logger.error(f"CSV file not found at {csv_path}")
            logger.error("Current directory contents: %s", os.listdir())
            text(f"## Error\nCSV file not found at {csv_path}")
            return
        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
            logger.error(traceback.format_exc())
            text(f"## Error\nFailed to read CSV: {e}")
            return

        # Display the raw data table
        table(df, title="Network Devices")

        # Create a graph using NetworkX
        logger.info("Creating NetworkX graph")
        G = nx.Graph()

        # Add nodes and edges based on the CSV data
        logger.info("Adding nodes and edges to the graph")
        for idx, row in df.iterrows():
            try:
                device = row['Device Name']
                connected_to = row['Connected To']
                
                # Log node addition details
                logger.info(f"Adding node: {device}")
                logger.info(f"Connection details: Connected to {connected_to}")
                
                # Add nodes with attributes
                G.add_node(device, 
                           ip_address=row['IP Address'], 
                           mac_address=row['MAC Address'], 
                           connection_type=row['Connection Type'])
                
                # Add edges
                if connected_to in df['Device Name'].values:
                    G.add_edge(device, connected_to)
                    logger.info(f"Added edge between {device} and {connected_to}")
            except Exception as e:
                logger.error(f"Error processing row {idx}: {e}")
                logger.error(traceback.format_exc())

        # Log graph details
        logger.info(f"Graph created. Nodes: {len(G.nodes())}, Edges: {len(G.edges())}")

        # Create a Matplotlib figure
        logger.info("Creating Matplotlib figure")
        plt.figure(figsize=(12, 8))

        # Use spring layout for node positioning
        logger.info("Calculating node positions")
        try:
            pos = nx.spring_layout(G, k=0.5, iterations=50)
            logger.info(f"Node positions calculated. Positions: {pos}")
        except Exception as e:
            logger.error(f"Error calculating node positions: {e}")
            logger.error(traceback.format_exc())
            raise

        # Draw the graph
        plt.title("Network Topology Visualization", fontsize=16)

        # Draw edges
        logger.info("Drawing graph edges")
        nx.draw_networkx_edges(G, pos, 
                               edge_color='gray', 
                               width=1, 
                               alpha=0.7)

        # Draw nodes with color coding based on connection type
        connection_colors = {
            'Wired': '#1E90FF',     # Dodger Blue for Wired
            'Wireless': '#32CD32'   # Lime Green for Wireless
        }

        logger.info("Calculating node colors")
        node_colors = []
        for node in G.nodes():
            try:
                color = connection_colors.get(G.nodes[node]['connection_type'], '#808080')
                node_colors.append(color)
                logger.info(f"Node {node}: Color {color}")
            except Exception as e:
                logger.error(f"Error processing node color for {node}: {e}")
                logger.error(traceback.format_exc())

        # Draw nodes
        logger.info("Drawing network nodes")
        nx.draw_networkx_nodes(G, pos, 
                               node_color=node_colors, 
                               node_size=800, 
                               alpha=0.9)

        # Add labels to nodes
        logger.info("Adding node labels")
        nx.draw_networkx_labels(G, pos, 
                                font_size=10, 
                                font_weight='bold')

        # Add a legend for connection types
        logger.info("Creating legend")
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
        logger.info("Adding device annotations")
        for node, (x, y) in pos.items():
            try:
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
                logger.info(f"Annotation added for node {node}")
            except Exception as e:
                logger.error(f"Error adding annotation for {node}: {e}")
                logger.error(traceback.format_exc())

        # Render the plot
        logger.info("Rendering Matplotlib plot")
        matplotlib_plot(plt.gcf())

        # Optional: Add some textual insights
        text("## Network Insights")
        text(f"- Total Devices: {len(G.nodes())}")
        text(f"- Wired Devices: {sum(1 for node in G.nodes() if G.nodes[node]['connection_type'] == 'Wired')}")
        text(f"- Wireless Devices: {sum(1 for node in G.nodes() if G.nodes[node]['connection_type'] == 'Wireless')}")

    except Exception as e:
        logger.error(f"Unhandled exception in script: {e}")
        logger.error(traceback.format_exc())
        text(f"## Error\nAn error occurred: {e}")

# Call the main function
main()