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
        self.client = LLMConfig.get_client()

    def extract_raw_triples(self, document: DocumentSource) -> List[RawTriple]:
        """
        Uses Instructor to extract raw, unconstrained semantic Triples.
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": Prompts.DISCOVERY_SYSTEM},
                {"role": "user", "content": Prompts.get_discovery_user(document.text_content)}
            ],
            response_model=TripleExtractionResult,
            max_tokens=8000
        )
        return response.triples

    def run_louvain_clustering(self, all_triples: List[RawTriple]) -> List[List[str]]:
        """
        Loads all unstructured triples actively into NetworkX, and runs standard Louvain community detection.
        Returns a nested list of communities natively mapped by node identities.
        """
        graph = nx.Graph() # Undirected graph needed for native Louvain analysis 
        
        for t in all_triples:
            graph.add_edge(t.subject, t.object, label=t.predicate)
            
        if len(graph.nodes) == 0:
            return []
            
        communities = louvain_communities(graph)
        return [list(c) for c in communities]
