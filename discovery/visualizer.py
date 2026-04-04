import os
from pyvis.network import Network
import networkx as nx
from typing import List

class GraphVisualizer:
    @staticmethod
    def render_communities(graph: nx.Graph, communities: List[List[str]], output_file: str = "knowledge_graph.html"):
        """
        Natively visualizes raw triplet extractions coloring nodes dynamically based on Louvain logic groupings!
        """
        net = Network(notebook=False, directed=False, height="800px", width="100%", bgcolor="#0d1117", font_color="white")
        net.force_atlas_2based()
        
        # Color palette for communities
        colors = ["#58a6ff", "#3fb950", "#d29922", "#f85149", "#a371f7", "#2ea043", "#db6d28", "#8957e5"]
        
        color_map = {}
        for i, community in enumerate(communities):
            color = colors[i % len(colors)]
            for node in community:
                color_map[node] = color
                
        for node in graph.nodes:
            net.add_node(
                node, 
                label=node, 
                title=f"Node: {node}",
                color=color_map.get(node, "#8b949e"), 
                size=15
            )
            
        for edge in graph.edges(data=True):
            source, target, data = edge
            predicate = data.get('label', '')
            net.add_edge(source, target, title=predicate, color="#30363d")
            
        net.write_html(output_file)
        return output_file
