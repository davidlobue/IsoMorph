from typing import List, Type, Optional
import time
from pydantic import BaseModel
from core.models import DocumentSource, KnowledgeGraph
from distillation.extractor import DistillationEngine
from designer.ontologist import OntologistEngine
from designer.graph_builder import GraphBuilderEngine
from designer.schema_builder import SchemaBuilder
from discovery.explorer import ExplorerEngine
from discovery.hardener import HardenerEngine

class Orchestrator:
    def __init__(
        self,
        hallucination_filter: bool = True,
        ontology_depth: Optional[int] = None,
        strict_typing: bool = True,
        verbose: bool = False
    ):
        from core.config import LLMConfig
        self.model_name = LLMConfig.get_model_name()
        self.base_url = LLMConfig.get_base_url()
        self.verbose = verbose
        
        # Toggles
        self.hallucination_filter = hallucination_filter
        self.ontology_depth = ontology_depth
        self.strict_typing = strict_typing
        
        print(f"[*] Orchestrator initialized. Model: {self.model_name} | Base URL: {self.base_url}")
        
        # Engines
        self.explorer = ExplorerEngine()
        self.hardener = HardenerEngine()
        self.distillation = DistillationEngine()
        self.ontologist = OntologistEngine()
        self.graph_builder = GraphBuilderEngine()
        self.schema_builder = SchemaBuilder(strict_typing=strict_typing)

    def run_discovery(self, documents: List[DocumentSource]) -> Type[BaseModel]:
        """
        Latent Property Clustering Pipeline intercept.
        """
        import time
        print("====== STAGE 0. DISCOVERY LOOP ======")
        print(f"[*] Executing schema-less triple extraction over {len(documents)} documents...")
        all_triples = []
        for doc in documents:
            start_time = time.time()
            triples = self.explorer.extract_raw_triples(doc)
            print(f"[TIMER] ExplorerEngine.extract_raw_triples for doc '{doc.id}' took: {time.time() - start_time:.2f}s")
            all_triples.extend(triples)
            
        print(f"[+] Extracted {len(all_triples)} raw topological triples.")
        print("[*] Running algorithmic Louvain community detection natively routing the graph...")
        start_time = time.time()
        communities = self.explorer.run_louvain_clustering(all_triples)
        print(f"[TIMER] Louvain graph isolation mapped in {time.time() - start_time:.2f}s")
        print(f"[+] Detected {len(communities)} distinct logic clusters.")
        
        print("[*] Hardening clusters via Canonical Pydantic Schema Translation...")
        clusters = []
        for i, community in enumerate(communities):
            print(f"  -> Validating Cluster {i+1} ({len(community)} nodes)...")
            cluster_logic = self.hardener.canonicalize_cluster(community, all_triples)
            if self.verbose:
                print(f"\\n[VERBOSE] Clustered Discovery Output:\\n{cluster_logic.model_dump_json(indent=2)}")
            clusters.append(cluster_logic)
            
        print("[*] Generating dynamic constraint-based Python models...")
        discovered_schema = self.hardener.generate_dynamic_schema(clusters)
        print(f"[+] Root Discovery Schema Instantiated Successfully: {discovered_schema.__name__}")
        return discovered_schema

    def run_pipeline(self, documents: List[DocumentSource]) -> Type[BaseModel]:
        """
        The overarching end-to-end scanner.
        """
        print("\n\n################ PHASE 1. LATENT DISCOVERY CLUSTERING ################\n")
        discovered_schema = self.run_discovery(documents)
        print("\n\n################ PHASE 2. GRAPH INTERPRETATION ENGINE ################\n")
        
        print("====== I. DISTILLATION ======")
        print(f"[*] Starting hard constrained mapping across {len(documents)} documents...")
        constrained_outputs = []
        for doc in documents:
            start_time = time.time()
            # Force the AI to rigidly align extractions bounds to only what was proven in Latent Discovery
            res = self.distillation.extract_features(doc, dynamic_schema=discovered_schema)
            print(f"[TIMER] Constrained Extraction for doc '{doc.id}' took: {time.time() - start_time:.2f}s")
            if self.verbose:
                print(f"\\n[VERBOSE] Constrained Payload:\\n{res.model_dump_json(indent=2)}")
            constrained_outputs.append(res)
            
        print("\\n[+] SUCCESS: Bypassed Legacy Ontologist entirely. The pipeline output is structurally locked to mathematical heuristics!")
        return constrained_outputs
