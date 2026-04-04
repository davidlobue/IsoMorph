from typing import List, Type, Optional
import time
from pydantic import BaseModel
from core.models import DocumentSource, RawTriple
from distillation.extractor import DistillationEngine
from discovery.explorer import ExplorerEngine
from discovery.hardener import HardenerEngine

class Orchestrator:
    def __init__(
        self,
        # LLM Engine Controls
        hallucination_filter: bool = True,       # Enforces strict "negative constraint" rules on the LLM to prevent data hallucination.
        ontology_depth: Optional[int] = None,    # (Optional) Hard limit on the maximum depth the schema graph will explore.
        strict_typing: bool = True,              # Forces the final PyDantic schemas to output exact programmatic types (e.g., Dates, Ints).
        verbose: bool = False,                   # If True, prints massive blocks of JSON debugging payloads to the terminal.
        
        # Graph Geometry Scaling
        louvain_resolution: float = 1.5,         # Base algorithm sensitivity. Higher sweeps aggressively split large node blobs into tiny, isolated communities.
        
        # Topology Physics Overrides
        advanced_heuristics: bool = True,        # Enables the Two-Pass Pipeline (Weights relationships based on rarity, then merges clusters that perform the same role).
        k_core_pruning: bool = True,             # The "Noise Reducer": Strips off isolated endpoints (Degree=1) before clustering, then re-attaches them after mapping.
        neighborhood_isomorphism: bool = True,   # The "Anonymity Guard": Forcibly vetoes a cluster merge if they do not share literal exact neighbors (prevents masking collisions).
        auto_resolution_tuning: bool = True      # The "Auto-Zoom": Overrides manual resolution by automatically stepping down the zoom until clusters drop below a 15% threshold.
    ):
        from core.config import LLMConfig
        self.model_name = LLMConfig.get_model_name()
        self.base_url = LLMConfig.get_base_url()
        self.verbose = verbose
        self.louvain_resolution = louvain_resolution
        self.advanced_heuristics = advanced_heuristics
        self.k_core_pruning = k_core_pruning
        self.neighborhood_isomorphism = neighborhood_isomorphism
        self.auto_resolution_tuning = auto_resolution_tuning
        
        # Toggles
        self.hallucination_filter = hallucination_filter
        self.ontology_depth = ontology_depth
        self.strict_typing = strict_typing
        
        print(f"[*] Orchestrator initialized. Model: {self.model_name} | Base URL: {self.base_url}")
        
        # Engines
        self.explorer = ExplorerEngine()
        self.hardener = HardenerEngine()
        self.distillation = DistillationEngine()


    async def _safe_extract_raw_triples(self, doc: DocumentSource, sem):
        import asyncio, time
        async with sem:
            start_time = time.time()
            triples = await self.explorer.extract_raw_triples(doc)
            print(f"[TIMER] ExplorerEngine.extract_raw_triples for doc '{doc.id}' took: {time.time() - start_time:.2f}s")
            print(f"[CHECKPOINT] Document '{doc.id}' done scanning for triples.")
            await asyncio.sleep(0.5)
            return triples

    async def _safe_canonicalize_cluster(self, community: List[str], all_triples: List[RawTriple], i: int, sem):
        import asyncio
        async with sem:
            print(f"  -> Validating Cluster {i+1} ({len(community)} nodes)...")
            cluster_logic = await self.hardener.canonicalize_cluster(community, all_triples)
            if self.verbose:
                print(f"\n[VERBOSE] Clustered Discovery Output:\n{cluster_logic.model_dump_json(indent=2)}")
            print(f"  [CHECKPOINT] Cluster {i+1} Processed and Hardened successfully.")
            await asyncio.sleep(0.5)
            return cluster_logic

    async def run_discovery(self, documents: List[DocumentSource]) -> Type[BaseModel]:
        """
        Latent Property Clustering Pipeline intercept.
        """
        import time, asyncio
        print("====== STAGE 0. DISCOVERY LOOP ======")
        print(f"[*] Executing schema-less triple extraction over {len(documents)} documents...")
        all_triples = []
        
        sem = asyncio.Semaphore(10)
        tasks = [self._safe_extract_raw_triples(doc, sem) for doc in documents]
        results = await asyncio.gather(*tasks)
        for triples in results:
            all_triples.extend(triples)
            
        print(f"[+] Extracted {len(all_triples)} raw topological triples.")
        print("[*] Running algorithmic Louvain community detection natively routing the graph...")
        start_time = time.time()
        communities, louvain_graph = self.explorer.run_louvain_clustering(
            all_triples, 
            resolution=self.louvain_resolution, 
            advanced_heuristics=self.advanced_heuristics,
            k_core_pruning=self.k_core_pruning,
            neighborhood_isomorphism=self.neighborhood_isomorphism,
            auto_resolution_tuning=self.auto_resolution_tuning
        )
        print(f"[TIMER] Louvain graph isolation mapped in {time.time() - start_time:.2f}s")
        print(f"[+] Detected {len(communities)} distinct logic clusters.")
        
        print("[*] Hardening clusters via Canonical Pydantic Schema Translation...")
        
        cluster_sem = asyncio.Semaphore(10)
        cluster_tasks = [self._safe_canonicalize_cluster(community, all_triples, i, cluster_sem) for i, community in enumerate(communities)]
        clusters = await asyncio.gather(*cluster_tasks)
            
        print("[*] Generating dynamic constraint-based Python models...")
        discovered_schema = self.hardener.generate_dynamic_schema(clusters)
        
        import json
        if self.verbose:
            print("\\n[VERBOSE] Explicit Hardened Pydantic Blueprint Configuration:")
            print(json.dumps(discovered_schema.model_json_schema(), indent=2))
        
        print(f"[+] Root Discovery Schema Instantiated Successfully: {discovered_schema.__name__}")
        
        # Deploy Graph Rendering Natively
        from discovery.visualizer import GraphVisualizer
        print("[*] Rendering Discovery Layout to PyVis topological network...")
        visualizer_start = time.time()
        viz_file = GraphVisualizer.render_communities(louvain_graph, communities, "knowledge_graph.html")
        print(f"[TIMER] Graphical parsing took: {time.time() - visualizer_start:.2f}s")
        print(f"[+] Interactive UI Community Layout generated at: {viz_file}")
        
        return discovered_schema

    async def _safe_extract_features(self, doc: DocumentSource, discovered_schema: Type[BaseModel], sem):
        import asyncio, time
        async with sem:
            start_time = time.time()
            res = await self.distillation.extract_features(doc, dynamic_schema=discovered_schema)
            print(f"[TIMER] Constrained Extraction for doc '{doc.id}' took: {time.time() - start_time:.2f}s")
            print(f"[CHECKPOINT] Document '{doc.id}' done constrained mapping.")
            if self.verbose:
                print(f"\n[VERBOSE] Constrained Payload:\n{res.model_dump_json(indent=2)}")
            await asyncio.sleep(0.5)
            return res

    async def run_pipeline(self, documents: List[DocumentSource]) -> List[BaseModel]:
        """
        The overarching end-to-end scanner.
        """
        import asyncio
        print("\n\n################ PHASE 1. LATENT DISCOVERY CLUSTERING ################\n")
        discovered_schema = await self.run_discovery(documents)
        print("\n\n################ PHASE 2. GRAPH INTERPRETATION ENGINE ################\n")
        
        print("====== I. DISTILLATION ======")
        print(f"[*] Starting hard constrained mapping across {len(documents)} documents...")
        
        sem = asyncio.Semaphore(10)
        tasks = [self._safe_extract_features(doc, discovered_schema, sem) for doc in documents]
        constrained_outputs = await asyncio.gather(*tasks)
            
        print("\\n[+] SUCCESS: Bypassed Legacy Ontologist entirely. The pipeline output is structurally locked to mathematical heuristics!")
        return constrained_outputs
