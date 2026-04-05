# Stage Outputs Reference

When `save_stage_outputs=True` is enabled in the `Orchestrator`, intermediate data structures and final outputs from the various pipeline stages are serialized as JSON blocks for downstream testing, debugging, or partial re-runs.

The outputs are saved to the `stage_outputs/` directory relative to the current working directory.

## File Locations

1. **Raw Triples (Extraction Stage)**
   - **Path:** `stage_outputs/1_raw_triples.json`
   - **Contents:** A list of `RawTriple` Pydantic objects. This represents the schema-less topological extractions (Subject, Predicate, Object) identified from raw texts prior to any clustering.

2. **Hardened Clusters (Generalization/Phase 3)**
   - **Path:** `stage_outputs/2_hardened_clusters.json`
   - **Contents:** A list of `DiscoveryCluster` Pydantic objects. These are the finalized clusters that have been mapped via latent space, taxonomic lifting, structural roles, or seeded meta-schemas. 

3. **Discovered Dynamic Schema (Schema Synthesis)**
   - **Path:** `stage_outputs/3_discovered_schema.json`
   - **Contents:** The JSON Schema representation of the final `BaseModel` dynamically generated to capture the generalized graph structure. This can be ingested by any JSON Schema-compatible tool or reconstructed into a strict programmatic model.

4. **Final Distilled Outputs (Validation & Mapping)**
   - **Path:** `stage_outputs/4_final_distilled_outputs.json`
   - **Contents:** A list of the parsed document models strictly validated against the discovered schema. Can be directly loaded as JSON records describing the constrained data.

## Loading in Downstream Processes

To load these outputs into downstream processes or a testing notebook without running the full Agentic pipeline:

```python
import json

# 1. Load Hardened Clusters
with open("stage_outputs/2_hardened_clusters.json", "r") as f:
    clusters_data = json.load(f)
    print("Clusters:", len(clusters_data))

# 2. Re-instantiate the Discovered Schema
# (You may use datamodel-code-generator to compile the JSON schema back to Pydantic)
with open("stage_outputs/3_discovered_schema.json", "r") as f:
    schema_def = json.load(f)
```
