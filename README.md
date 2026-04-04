# IsoMorph ⚙️

IsoMorph is a powerful **Agentic Knowledge Engineering Pipeline** designed to ingest highly unstructured, masked, or noisy domain text (such as raw clinical/behavioral records) and automatically distill them into rigid, structured **Pydantic Ontologies** and Knowledge Graphs.

By bridging asynchronous Large Language Models (LLMs) via `instructor` with sophisticated mathematical graph-theoretic algorithms using `NetworkX`, IsoMorph entirely bypasses standard semantic hallucinations. It prevents "schema explosion" by geometrically analyzing how textual entities interact within the system before resolving them into programmatically enforced constraints.

---

## 🚀 The Pipeline Architecture

The workflow is split into two primary automated processes:

### Phase 1: Latent Discovery Clustering
Instead of attempting zero-shot schema extraction, IsoMorph first maps the textual corpus natively.
1. **Schema-less Triplet Extraction:** Async engines scan all source documents parallelized via strict semaphores to extract `(Subject) -> [Predicate] -> (Object)` relationships blindly without preconceived schemas.
2. **Topological Graph Algorithms:** The triples are loaded into a `NetworkX` mesh where the engine executes complex algorithmic refinements and applies weighted Louvain community detection to group the knowledge natively into purely logical shapes.
3. **Pydantic Hardening:** Highly isolated communities are pulled out of the mesh and translated via the LLM into explicit constraints, locking down hallucination-proof Pydantic models mapping explicit negative traits.

### Phase 2: Graph Interpretation (Distillation)
The hardened Python Pydantic classes formulated in Phase 1 are injected back into the LLM logic engines as strict validation models. The raw text is then blasted against these newly generated master models to yield universally categorized, highly structured JSON configurations matching reality.

---

## 🧬 Extreme Network Topology Optimizations

To handle severely anonymized data (e.g., heavily masked IDs, hyper-fragmented syntax arrays), IsoMorph deploys a localized custom **Two-Pass Optimization Sequence** before and during the network clustering layer:

### 1. The Semantic Entropy Splitter
Before mapping communities mathematically, IsoMorph calculates literal Information Theory constraints. It analyzes global predicate occurrence metrics and automatically weights edges based on their mathematical rarity: `$Weight = \max\left(0.01, \log\left(\frac{\text{Total Triples}}{\text{Frequency}}\right)\right)$`. 
This acts as a "community splitter". Generic features mathematically repulse while structurally rare relationship links algorithmically attract.

### 2. K-Core "Leaf" Pruning 
To minimize topological noise drastically, IsoMorph executes a pre-parse K-Core algorithmic guard. It catalogs and explicitly vaporizes any isolated "leaf" nodes (where `degree == 1`) entirely out of the active graph matrix before evaluating Louvain communities. Post-computation, native Python reconstructs the missing branches exactly into whatever array bracket their tracked neighbor landed in.

### 3. Structural Jaccard Merging
Once Louvain has successfully isolated sub-networks across the data, IsoMorph crosses into **Pass 2: The Merging Engine**. It establishes a Jaccard intersection baseline (default roughly $\ge 0.75$) profiling the exact predicate types active within separate isolated networks. If two communities mirror the exact same functional role structure within the overall document, IsoMorph explicitly draws a new mapping and securely collapses them into one unified, master schema structure.

### 4. Neighborhood Isomorphism ("The Anonymity Guard")
During the Jaccard Merger logic cross-check, the script runs a localized exact text intersection protocol. If `Cluster A` and `Cluster B` structurally reflect the exact same mathematical properties, the merge is unconditionally **vetoed** if they do not explicitly share literal overlapping neighbor names. This ensures distinct patients mapping perfectly identical profiles are never mathematically crushed into the same schema representation!

### 5. Resolution Sweeping ("Auto-Zoom")
To prevent runaway schema generation, the Engine ignores static variables and executes a descending bounded `while` sweep on the Louvain resolution target. It scales down systematically until the algorithmic isolation limits comfortably cross below a hard mathematical $15\%$ boundary limit, returning maximum compression efficiency!
