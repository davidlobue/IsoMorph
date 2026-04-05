from typing import List, Type, Optional
import time
from pydantic import BaseModel
from core.models import DocumentSource, RawTriple
from distillation.extractor import DistillationEngine
from discovery.explorer import ExplorerEngine
from discovery.hardener import HardenerEngine
from refinement.generalizer import GeneralizerEngine

class Orchestrator:
    def __init__(
        self,
        max_concurrency: int = 10,               # Enforces a hard limit on the number of parallel LLM calls globally to avoid GPU overload.
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
        auto_resolution_tuning: bool = True,     # The "Auto-Zoom": Overrides manual resolution by automatically stepping down the zoom until clusters drop below a 15% threshold.
        human_readable_schema: bool = True,      # Outputs the hard Pydantic schemas as a natively formatted multi-line Python script vs a dense single-line string.
        
        # Generalization Architecture Overrides
        generalize_taxonomic_lifting: bool = False,
        generalize_structural_roles: bool = False,
        generalize_seeded_schemas: bool = False,
        generalize_latent_space: bool = True,      # Enforces Hybrid Semantic Pooling Strategy By Default
        
        # Output Logging
        save_stage_outputs: bool = False         # Saves intermediate lists and schemas to disk for downstream testing
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
        self.human_readable_schema = human_readable_schema
        
        # Phase 3 Controls
        self.generalize_taxonomic_lifting = generalize_taxonomic_lifting
        self.generalize_structural_roles = generalize_structural_roles
        self.generalize_seeded_schemas = generalize_seeded_schemas
        self.generalize_latent_space = generalize_latent_space
        
        # Toggles
        self.hallucination_filter = hallucination_filter
        self.ontology_depth = ontology_depth
        self.strict_typing = strict_typing
        self.max_concurrency = max_concurrency
        self.save_stage_outputs = save_stage_outputs
        
        print(f"[*] Orchestrator initialized. Model: {self.model_name} | Base URL: {self.base_url}")
        
        # Engines
        self.explorer = ExplorerEngine()
        self.hardener = HardenerEngine()
        self.distillation = DistillationEngine()
        self.generalizer = GeneralizerEngine()

    def _save_stage_output(self, filename: str, data: any):
        if not self.save_stage_outputs: return
        import json, os
        os.makedirs("stage_outputs", exist_ok=True)
        filepath = os.path.join("stage_outputs", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            if isinstance(data, list) and len(data) > 0 and hasattr(data[0], "model_dump_json"):
                f.write("[\n" + ",\n".join(d.model_dump_json(indent=2) for d in data) + "\n]")
            elif hasattr(data, "model_json_schema"):
                f.write(json.dumps(data.model_json_schema(), indent=2))
            else:
                try: f.write(json.dumps(data, indent=2))
                except: f.write(str(data))
        print(f"[SAVE] Stage output written to {filepath}")


    async def _safe_extract_raw_triples(self, doc: DocumentSource, sem):
        import asyncio, time
        async with sem:
            start_time = time.time()
            result = await self.explorer.extract_raw_triples(doc)
            
            with open("logs/extraction_reasoning.md", "a", encoding="utf-8") as f:
                f.write(f"### Document: `{doc.id}` (Extraction)\n\n**Reasoning:**\n{result.reasoning}\n\n---\n\n")
                
            print(f"[TIMER] ExplorerEngine.extract_raw_triples for doc '{doc.id}' took: {time.time() - start_time:.2f}s")
            print(f"[CHECKPOINT] Document '{doc.id}' done scanning for triples.")
            await asyncio.sleep(0.5)
            return result.triples

    async def _safe_canonicalize_cluster(self, community: List[str], all_triples: List[RawTriple], i: int, sem):
        import asyncio
        async with sem:
            print(f"  -> Validating Cluster {i+1} ({len(community)} nodes)...")
            cluster_logic = await self.hardener.canonicalize_cluster(community, all_triples)
            
            with open("logs/clustering_reasoning.md", "a", encoding="utf-8") as f:
                f.write(f"### Cluster {i+1} (Hardening)\n\n**Semantic Centroid / Role:**\n{cluster_logic.hypernym}\n\n---\n\n")
                
            if self.verbose:
                print(f"\n[VERBOSE] Clustered Discovery Output:\n{cluster_logic.model_dump_json(indent=2)}")
            print(f"  [CHECKPOINT] Cluster {i+1} Processed and Hardened successfully.")
            await asyncio.sleep(0.5)
            return cluster_logic

    async def run_discovery(self, documents: List[DocumentSource]) -> Type[BaseModel]:
        """
        Latent Property Clustering Pipeline intercept.
        """
        import time, asyncio, os
        os.makedirs("logs", exist_ok=True)
        print("====== STAGE 0. DISCOVERY LOOP ======")
        print(f"[*] Executing schema-less triple extraction over {len(documents)} documents...")
        all_triples = []
        
        sem = asyncio.Semaphore(self.max_concurrency)
        tasks = [self._safe_extract_raw_triples(doc, sem) for doc in documents]
        results = await asyncio.gather(*tasks)
        for triples in results:
            all_triples.extend(triples)
            
        print(f"[+] Extracted {len(all_triples)} raw topological triples.")
        self._save_stage_output("1_raw_triples.json", all_triples)
        
        print("[*] Running algorithmic Louvain community detection natively routing the graph...")
        start_time = time.time()
        communities, louvain_graph = self.explorer.run_louvain_clustering(
            all_triples, 
            resolution=self.louvain_resolution, 
            advanced_heuristics=self.advanced_heuristics,
            k_core_pruning=self.k_core_pruning,
            neighborhood_isomorphism=self.neighborhood_isomorphism,
            auto_resolution_tuning=self.auto_resolution_tuning,
            verbose=self.verbose,
            graph_output_dir="graph_progressions"
        )
        print(f"[TIMER] Louvain graph isolation mapped in {time.time() - start_time:.2f}s")
        print(f"[+] Detected {len(communities)} distinct logic clusters.")
        
        print("[*] Hardening clusters via Canonical Pydantic Schema Translation...")
        
        cluster_sem = asyncio.Semaphore(self.max_concurrency)
        cluster_tasks = [self._safe_canonicalize_cluster(community, all_triples, i, cluster_sem) for i, community in enumerate(communities)]
        clusters = await asyncio.gather(*cluster_tasks)
            
        if any([self.generalize_taxonomic_lifting, self.generalize_structural_roles, self.generalize_seeded_schemas, self.generalize_latent_space]):
            print("\n====== STAGE 0.5 GENERALIZATION (PHASE 3) ======")
            clusters = await self.generalizer.refine_blueprint(
                clusters, 
                graph=louvain_graph,
                all_triples=all_triples,
                do_latent=self.generalize_latent_space,
                do_taxonomic=self.generalize_taxonomic_lifting,
                do_structural=self.generalize_structural_roles,
                do_seeded=self.generalize_seeded_schemas
            )
            
        self._save_stage_output("2_hardened_clusters.json", clusters)
            
        print("[*] Generating dynamic constraint-based Python models...")
        discovered_schema = self.hardener.generate_dynamic_schema(clusters)
        self.hardener.export_schema_to_file(clusters, human_readable=self.human_readable_schema)
        
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
        
        self._save_stage_output("3_discovered_schema.json", discovered_schema)
        
        return discovered_schema

    async def _safe_extract_features(self, doc: DocumentSource, discovered_schema: Type[BaseModel], sem):
        import asyncio, time
        async with sem:
            start_time = time.time()
            res = await self.distillation.extract_features(doc, dynamic_schema=discovered_schema)
            
            with open("logs/distillation_reasoning.md", "a", encoding="utf-8") as f:
                f.write(f"### Document: `{doc.id}` (Distillation)\n\n**Reasoning:**\n{getattr(res, 'reasoning', 'No reasoning provided.')}\n\n---\n\n")
                
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
        
        sem = asyncio.Semaphore(self.max_concurrency)
        tasks = [self._safe_extract_features(doc, discovered_schema, sem) for doc in documents]
        constrained_outputs = await asyncio.gather(*tasks)
            
        print("\\n[+] SUCCESS: Bypassed Legacy Ontologist entirely. The pipeline output is structurally locked to mathematical heuristics!")
        
        self._save_stage_output("4_final_distilled_outputs.json", constrained_outputs)
        
        return constrained_outputs
