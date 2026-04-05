import instructor
import asyncio
import math
from typing import List, Optional
from pydantic import BaseModel, Field
import networkx as nx

from core.models import DiscoveryCluster
from core.config import LLMConfig
from refinement.prompts import RefinementPrompts

class GeneralizedResponse(BaseModel):
    new_class_name: str = Field(description="The generalized abstract name for the cluster.")
    reasoning: str = Field(description="Reasoning for this abstract classification.")

class GeneralizerEngine:
    """
    Executes Phase 3: Abstraction and Generalization.
    Transforms raw Lexical-heavy DiscoveredBlueprints into Generalized abstractions.
    """
    def __init__(self):
        self.model_name = LLMConfig.get_model_name()
        self.async_client = LLMConfig.get_async_client()
        self.raw_openai = LLMConfig.get_async_raw_openai_client()
        self.embedding_model = LLMConfig.get_embedding_model_name()

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = math.sqrt(sum(a * a for a in vec1))
        magnitude2 = math.sqrt(sum(b * b for b in vec2))
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        return dot_product / (magnitude1 * magnitude2)

    async def apply_latent_space_clustering(self, clusters: List[DiscoveryCluster], threshold: float = 0.85) -> List[DiscoveryCluster]:
        """
        Groups clusters natively by mathematically comparing the vector embeddings of their Lexical representation.
        """
        if len(clusters) < 2:
            return clusters

        print("[*] Generalizer: Firing Latent Space Vectorization...")
        texts = [f"{c.class_name} Data properties: " + ", ".join(c.canonical_predicates) for c in clusters]
        
        try:
            resp = await self.raw_openai.embeddings.create(input=texts, model=self.embedding_model)
            embeddings = [data.embedding for data in resp.data]
        except Exception as e:
            print(f"[ERROR] Embedding request failed: {e}. Skipping Latent Mapping.")
            return clusters

        num_clusters = len(clusters)
        merger_graph = nx.Graph()
        merger_graph.add_nodes_from(range(num_clusters))

        for i in range(num_clusters):
            for j in range(i + 1, num_clusters):
                sim = self._cosine_similarity(embeddings[i], embeddings[j])
                if sim >= threshold:
                    merger_graph.add_edge(i, j)

        temp_clusters = []
        for component in nx.connected_components(merger_graph):
            idx_list = list(component)
            if len(idx_list) == 1:
                temp_clusters.append(clusters[idx_list[0]])
            else:
                # Merge multiple clusters
                merged_nodes = []
                merged_preds = []
                merged_negatives = []
                names = []
                for idx in idx_list:
                    c = clusters[idx]
                    names.append(c.class_name)
                    merged_nodes.extend(c.nodes)
                    merged_preds.extend(c.canonical_predicates)
                    merged_negatives.extend(c.negative_constraints)
                
                merged_cluster = DiscoveryCluster(
                    class_name="MergedPool_Pending_Synthesis",
                    reasoning=f"Latent Spatial Vector Pooling combined ({', '.join(names)}) due to high cosine threshold (>= {threshold}).",
                    nodes=list(set(merged_nodes)),
                    canonical_predicates=list(set(merged_preds)),
                    negative_constraints=list(set(merged_negatives))
                )
                temp_clusters.append(merged_cluster)

        print(f"[+] Generalizer: Semantic pooling combined vectors. Now Synthesizing LLM Universal Labels for groups...")
        final_clusters = await self.apply_taxonomic_lifting(temp_clusters)
        
        print(f"[+] Generalizer: Hybrid Space compressed {len(clusters)} source elements to {len(final_clusters)} shared universal classes.")
        return final_clusters

    async def _safe_taxonomic_lift(self, cluster: DiscoveryCluster, sem: asyncio.Semaphore) -> DiscoveryCluster:
        async with sem:
            class_data_str = cluster.model_dump_json(indent=2)
            res = await self.async_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": RefinementPrompts.TAXONOMIC_LIFTING_SYSTEM},
                    {"role": "user", "content": RefinementPrompts.get_taxonomic_lifting_user(class_data_str)}
                ],
                response_model=GeneralizedResponse
            )
            cluster.class_name = res.new_class_name
            cluster.reasoning = f"[Taxonomic Lift] {res.reasoning}"
            
            with open("logs/generalization_reasoning.md", "a", encoding="utf-8") as f:
                f.write(f"### Class `{cluster.class_name}` (Taxonomic Lifting)\n\n**Reasoning:**\n{res.reasoning}\n\n---\n\n")
                
            return cluster

    async def apply_taxonomic_lifting(self, clusters: List[DiscoveryCluster]) -> List[DiscoveryCluster]:
        if not clusters: return clusters
        print("[*] Generalizer: Applying Taxonomic Lifting (Top-Level Ontology anchors)...")
        sem = asyncio.Semaphore(10)
        tasks = [self._safe_taxonomic_lift(c, sem) for c in clusters]
        return list(await asyncio.gather(*tasks))

    async def apply_structural_role_abstraction(self, clusters: List[DiscoveryCluster], graph: nx.Graph = None) -> List[DiscoveryCluster]:
        if not clusters: return clusters
        print("[*] Generalizer: Analyzing Structural Motifs & Roles (Code-only Mathematical heuristic)...")
        
        if graph is None or len(graph.nodes) == 0:
            for i, c in enumerate(clusters):
                c.class_name = f"Isolated-Component-{i+1}"
                c.reasoning = "[Structural Motifs] No graph topology available. Force defaulted to Isolated."
            return clusters

        cent = nx.degree_centrality(graph)
        all_cents = list(cent.values())
        mean_c = sum(all_cents) / len(all_cents)
        var_c = sum((x - mean_c) ** 2 for x in all_cents) / len(all_cents)
        std_c = math.sqrt(var_c)

        for i, cluster in enumerate(clusters):
            c_vals = [cent[n] for n in cluster.nodes if n in cent]
            if not c_vals:
                cluster.class_name = f"Disconnected-Module-{i+1}"
                cluster.reasoning = "[Structural Motifs] Elements not found in mapped topology."
                continue
            
            c_mean = sum(c_vals) / len(c_vals)
            
            if c_mean >= (mean_c + std_c):
                name = f"High-Degree-Hub-{i+1}"
            elif c_mean <= (mean_c - std_c) or c_mean == 0:
                name = f"Terminal-Leaf-{i+1}"
            else:
                name = f"Intermediate-Bridge-{i+1}"
                
            cluster.class_name = name
            cluster.reasoning = f"[Structural Motifs] Graph Math Assignment: Cluster Mean Centrality = {c_mean:.4f} (Global Mean = {mean_c:.4f}, Std = {std_c:.4f})"
            
            with open("logs/generalization_reasoning.md", "a", encoding="utf-8") as f:
                f.write(f"### Class `{cluster.class_name}` (Structural Roles)\n\n**Reasoning:**\n{cluster.reasoning}\n\n---\n\n")

        return clusters

    async def _safe_seeded_meta(self, cluster: DiscoveryCluster, seeds: List[str], sem: asyncio.Semaphore) -> DiscoveryCluster:
        from enum import Enum
        from pydantic import create_model
        
        SeedEnum = Enum("SeedEnum", {s: s for s in seeds})
        StrictSeededResponse = create_model("StrictSeededResponse", 
                                            new_class_name=(SeedEnum, Field(description="Must exactly match one of the predefined seed classes.")),
                                            reasoning=(str, Field(description="Reasoning explaining this discrete classification.")))

        async with sem:
            seeds_str = ", ".join(seeds)
            class_data_str = cluster.model_dump_json(indent=2)
            
            res = await self.async_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": RefinementPrompts.SEEDED_META_SCHEMA_SYSTEM},
                    {"role": "user", "content": RefinementPrompts.get_seeded_meta_schemas_user(class_data_str, seeds_str)}
                ],
                response_model=StrictSeededResponse
            )
            cluster.class_name = res.new_class_name.value
            cluster.reasoning = f"[Seeded Meta] {res.reasoning}"
            
            with open("logs/generalization_reasoning.md", "a", encoding="utf-8") as f:
                f.write(f"### Class `{cluster.class_name}` (Seeded Meta-Schemas)\n\n**Reasoning:**\n{res.reasoning}\n\n---\n\n")
                
            return cluster

    async def apply_seeded_meta_schemas(self, clusters: List[DiscoveryCluster], seeds: List[str] = None) -> List[DiscoveryCluster]:
        if not clusters: return clusters
        if seeds is None:
            seeds = ["Agent", "Action", "Outcome", "Mechanism", "Context", "Object"]
        print(f"[*] Generalizer: Mapping to Seeded Roots ({len(seeds)} anchors)...")
        sem = asyncio.Semaphore(10)
        tasks = [self._safe_seeded_meta(c, seeds, sem) for c in clusters]
        return list(await asyncio.gather(*tasks))

    async def refine_blueprint(self, 
                               clusters: List[DiscoveryCluster], 
                               graph: nx.Graph = None,
                               do_latent: bool = False,
                               do_taxonomic: bool = False,
                               do_structural: bool = False,
                               do_seeded: bool = False,
                               seeds: List[str] = None) -> List[DiscoveryCluster]:
        """
        Applies selected generalized techniques sequentially over the Blueprint elements.
        """
        # Vector spatial collapse handles duplications before semantic mappings
        if do_latent:
            clusters = await self.apply_latent_space_clustering(clusters)
            # Latent space clustering natively applies taxonomic lifting to synthesize names for
            # both merged and isolated clusters. We prevent double-execution here:
            do_taxonomic = False
            
        if do_structural:
            clusters = await self.apply_structural_role_abstraction(clusters, graph)
            
        if do_taxonomic:
            clusters = await self.apply_taxonomic_lifting(clusters)
            
        if do_seeded:
            clusters = await self.apply_seeded_meta_schemas(clusters, seeds)
            
        return clusters
