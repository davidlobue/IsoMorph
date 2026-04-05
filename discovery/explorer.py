import instructor
import networkx as nx
from networkx.algorithms.community import louvain_communities
from typing import List
from core.models import DocumentSource, RawTriple, TripleExtractionResult
from core.config import LLMConfig
from core.prompts import Prompts

class ExplorerEngine:
    """
    Executes Phase 1 of the Discovery layer. 
    Focuses on schema-less triplet extraction and mathematical Louvain community detection.
    """
    def __init__(self):
        self.model_name = LLMConfig.get_model_name()
        self.async_client = LLMConfig.get_async_client()

    async def extract_raw_triples(self, document: DocumentSource) -> TripleExtractionResult:
        """
        Uses Instructor to extract raw, unconstrained semantic Triples.
        """
        response = await self.async_client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": Prompts.DISCOVERY_SYSTEM},
                {"role": "user", "content": Prompts.get_discovery_user(document.text_content)}
            ],
            response_model=TripleExtractionResult
        )
        return response

    def run_louvain_clustering(self, all_triples: List[RawTriple], resolution: float = 1.0, advanced_heuristics: bool = True, k_core_pruning: bool = True, neighborhood_isomorphism: bool = True, auto_resolution_tuning: bool = True, verbose: bool = False) -> tuple[List[List[str]], nx.Graph]:
        """
        Loads all unstructured triples actively into NetworkX, and runs standard Louvain community detection.
        
        Args:
            all_triples: Raw relational triplets extracted from the text corpus.
            resolution: The multi-level tuning parameter. Values < 1.0 group nodes into massive "super-communities". Values > 1.0 make the algorithm hypersensitive, isolating fine-grained sub-communities.
            advanced_heuristics: If True, uses a Two-Pass Optimization. Pass 1 applies Predicate Entropy weighting. Pass 2 merges resulting clusters via a Structural Jaccard Fingerprint comparison.
            k_core_pruning: If True, dynamically strips mathematical 'leaf' islands (degree == 1) prior to Louvain processing, resolving back into the topology afterward.
            neighborhood_isomorphism: If True, structurally checks that merged clusters share literal node IDs before Jaccard fusion processing, preserving pure entity anonymity.
            auto_resolution_tuning: If True, initiates a dynamic resolution sweep targeting < 15% cluster-to-triple bounds.
            
        Returns a nested list of communities natively mapped by node identities.
        """
        import math
        graph = nx.Graph() # Undirected graph needed for native Louvain analysis 
        
        for t in all_triples:
            graph.add_edge(t.subject, t.object, label=t.predicate)
            
        if len(graph.nodes) == 0:
            return [], graph
            
        total_triples = len(all_triples)
        
        # 1. K-Core Leaf Pruning
        leaf_parents = {}
        if k_core_pruning:
            leaves = [n for n in graph.nodes if graph.degree(n) == 1]
            for leaf in leaves:
                parent = list(graph.neighbors(leaf))[0]
                leaf_parents[leaf] = parent
            graph.remove_nodes_from(leaves)
            if verbose:
                print(f"[VERBOSE] K-Core Pruning: Sequestered {len(leaves)} leaf noise nodes. Core graph contains {len(graph.nodes)} dense nodes.")
            
            if len(graph.nodes) == 0:
                graph.add_edges_from([(l, p) for l, p in leaf_parents.items()])
                leaf_parents = {}

        if advanced_heuristics:
            # Pass 1: Semantic Entropy ("Community Splitter")
            from collections import Counter
            predicate_counts = Counter([t.predicate for t in all_triples])
            
            for u, v, data in graph.edges(data=True):
                pred = data.get('label', '')
                freq = predicate_counts.get(pred, 1)
                # Weight(e) = log(Total_Triples / Frequency(Predicate))
                weight = max(0.01, math.log(total_triples / freq)) if freq > 0 else 0.1
                graph[u][v]['weight'] = weight
        else:
            for u, v in graph.edges():
                graph[u][v]['weight'] = 1.0

        # Tuning sweep
        if auto_resolution_tuning:
            current_res = 1.5
            limit = int(total_triples * 0.15)
            if verbose:
                print(f"[VERBOSE] Auto-Resolution Sweeper: Target max bounding limit = {limit} communities.")
            # Failsafe limit floor 0.1
            while current_res >= 0.1:
                communities = louvain_communities(graph, resolution=current_res, weight='weight')
                if len(communities) <= limit:
                    if verbose:
                        print(f"[VERBOSE] Auto-Resolution stabilized at sensitivity scale {current_res:.2f} rendering {len(communities)} core distinct logic atoms.")
                    break
                current_res -= 0.2
        else:
            communities = louvain_communities(graph, resolution=resolution, weight='weight')
            
        base_clusters = [list(c) for c in communities]
        
        # Re-attach leaves
        if k_core_pruning and leaf_parents:
            for l, p in leaf_parents.items():
                graph.add_edge(l, p) 
            
            for base_comm in base_clusters:
                base_set = set(base_comm)
                for l, p in leaf_parents.items():
                    if p in base_set:
                        base_comm.append(l)

        if advanced_heuristics:
            # Pass 2: Structural Jaccard ("Class Merger")
            cluster_profiles = []
            cluster_literals = [] # For isomorphism
            for comm in base_clusters:
                preds = set()
                literal_neighbors = set()
                for n in comm:
                    literal_neighbors.update(graph.neighbors(n))
                    for neighbor in graph.neighbors(n):
                        preds.add(graph[n][neighbor].get('label', ''))
                cluster_profiles.append(preds)
                cluster_literals.append(literal_neighbors)
            
            num_clusters = len(base_clusters)
            merger_graph = nx.Graph()
            merger_graph.add_nodes_from(range(num_clusters))
            if verbose:
                print(f"[VERBOSE] Structural Jaccard Merger: Cross-evaluating {num_clusters} atomic communities for logical isomorphism.")
            
            for i in range(num_clusters):
                for j in range(i + 1, num_clusters):
                    # Isomorphism Veto
                    if neighborhood_isomorphism:
                        if len(cluster_literals[i].intersection(cluster_literals[j])) == 0:
                            continue # Veto merge
                            
                    set_i = cluster_profiles[i]
                    set_j = cluster_profiles[j]
                    intersection = len(set_i.intersection(set_j))
                    union = len(set_i.union(set_j))
                    jaccard_sim = intersection / union if union > 0 else 0.0
                    
                    if jaccard_sim >= 0.75:
                        merger_graph.add_edge(i, j)
            
            final_communities = []
            # Extract structurally mirrored groups into unified schema layouts
            for component in nx.connected_components(merger_graph):
                merged = set()
                for idx in component:
                    merged.update(base_clusters[idx])
                final_communities.append(list(merged))
                
            if verbose:
                print(f"[VERBOSE] Topology Refinement: Jaccard overlay compressed {num_clusters} raw logic atoms solidly into exactly {len(final_communities)} unified master schemas.")
                
            return final_communities, graph
        else:
            return base_clusters, graph
