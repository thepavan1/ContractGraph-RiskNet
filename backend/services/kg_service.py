import networkx as nx
from typing import Dict, Any

class KGService:
    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_base_graph()

    def _build_base_graph(self):
        """
        Builds the baseline Contract Knowledge Graph based on the 11 nodes and 9 edges
        from the research architecture.
        """
        # Define 11 core nodes (Risk Factors & Outcomes)
        nodes = [
            {"id": "Contract", "group": 1, "val": 20, "color": "#3b82f6"}, # Blue
            {"id": "Delay Risk", "group": 2, "val": 15, "color": "#ef4444"}, # Red
            {"id": "Financial Stress", "group": 2, "val": 15, "color": "#ef4444"},
            {"id": "Quality Defect", "group": 2, "val": 10, "color": "#f59e0b"}, # Amber
            {"id": "Scope Creep", "group": 2, "val": 10, "color": "#f59e0b"},
            {"id": "Force Majeure", "group": 3, "val": 10, "color": "#8b5cf6"}, # Purple
            {"id": "Regulatory Change", "group": 3, "val": 10, "color": "#8b5cf6"},
            {"id": "Cost Overrun", "group": 4, "val": 18, "color": "#dc2626"}, # Strong Red
            {"id": "Time Extension", "group": 4, "val": 12, "color": "#d97706"}, 
            {"id": "Dispute", "group": 5, "val": 15, "color": "#9f1239"}, # Rose
            {"id": "Termination", "group": 5, "val": 25, "color": "#000000"} # Black/Fatal
        ]
        
        # Add nodes to networkx
        for node in nodes:
            self.graph.add_node(node["id"], **node)
            
        # Define 9 causal edges based on infrastructure contract dynamics
        edges = [
            ("Contract", "Delay Risk", 5),
            ("Contract", "Financial Stress", 4),
            ("Contract", "Scope Creep", 3),
            ("Delay Risk", "Time Extension", 8),
            ("Delay Risk", "Cost Overrun", 7),
            ("Financial Stress", "Cost Overrun", 6),
            ("Scope Creep", "Cost Overrun", 5),
            ("Cost Overrun", "Dispute", 7),
            ("Dispute", "Termination", 9)
        ]
        
        for source, target, weight in edges:
            self.graph.add_edge(source, target, weight=weight)

    def get_graph_data(self) -> Dict[str, Any]:
        """
        Returns the graph data formatted for react-force-graph.
        """
        nodes = [{"id": n, **self.graph.nodes[n]} for n in self.graph.nodes()]
        links = [{"source": u, "target": v, "val": d["weight"]} for u, v, d in self.graph.edges(data=True)]
        
        # Calculate centrality for dynamic sizing if needed
        centrality = nx.degree_centrality(self.graph)
        for node in nodes:
            node["centrality"] = centrality[node["id"]]
            
        return {
            "nodes": nodes,
            "links": links
        }

kg_service = KGService()
