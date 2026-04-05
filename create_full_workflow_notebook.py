import nbformat as nbf

nb = nbf.v4.new_notebook()

text_intro = """\
# Full Pipeline Step-by-Step Workflow
This notebook breaks down the `Orchestrator` to test the Distillation, Designer, and Validation loops explicitly.
It also demonstrates how downstream processes can load and utilize the new `stage_outputs` JSON structures independent of full model re-runs.
"""

code_imports = """\
import sys
import os
import asyncio
import json

# Allow imports from local directory if running inside the ontology folder
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from dotenv import load_dotenv
load_dotenv()

from core.models import DocumentSource
from pipeline.orchestrator import Orchestrator
"""

text_docs = """\
## 1. Define Test Context
Initialize the raw clinical documents that will act as the empirical context.
"""

code_docs = """\
doc1 = DocumentSource(
    id="doc_001",
    text_content=\"\"\"
    Patient Assessment - Oct 4, 2023:
    Jordan exhibited highly repetitive physical motions, specifically hand-flapping, 
    when the classroom environment became too loud. He did not engage in verbal communication for 45 minutes.
    \"\"\"
)

doc2 = DocumentSource(
    id="doc_002",
    text_content=\"\"\"
    In-home Observation - Oct 5, 2023:
    During dinner, Jordan successfully maintained eye contact with his sibling when asking for water.
    However, when transitioned to bedtime, severe physical agitation and distress was observed.
    \"\"\"
)

docs = [doc1, doc2]
"""

text_orchestrator = """\
## 2. Initialize the Orchestrator with Tracking Enabled
We configure the `Orchestrator` with our generalization metrics enabled, utilizing `save_stage_outputs=True` to persist checkpoints tracking intermediate vectors.
"""

code_orchestrator = """\
orchestrator = Orchestrator(
    max_concurrency=4,
    hallucination_filter=True,
    ontology_depth=None,
    strict_typing=True,
    verbose=True,
    generalize_latent_space=True,
    generalize_structural_roles=True,
    generalize_taxonomic_lifting=True,
    generalize_seeded_schemas=True,
    save_stage_outputs=True
)
"""

text_phase1 = """\
## 3. Phase 1: Discovery & Abstraction
Instead of running `run_pipeline`, we manually invoke `run_discovery` to extract raw topologies, cluster them, and synthesize a programmatic output schema.
Because `save_stage_outputs` is enabled, this will export `1_raw_triples.json`, `2_hardened_clusters.json`, and `3_discovered_schema.json`.
"""

code_phase1 = """\
# NOTE: This runs the extraction natively over the LLM. 
# If you are doing downstream testing, you can skip this and simply load "stage_outputs/3_discovered_schema.json"
discovered_schema = await orchestrator.run_discovery(docs)

print(f"\\nSuccessfully Dynamically Instantiated BaseModel: {discovered_schema.__name__}")
"""

text_inspect = """\
## 4. Validating Downstream Capabilities
Let's simulate a downstream process testing our logic by loading the exported `2_hardened_clusters.json` file.
"""

code_inspect = """\
# We can load these datasets computationally without querying the LLM again.
try:
    with open("stage_outputs/2_hardened_clusters.json", "r") as f:
        hardened_clusters = json.load(f)
        print(f"Loaded {len(hardened_clusters)} Structural Abstractions natively from Local Disk for isolated testing:")
        print(json.dumps(hardened_clusters[0], indent=2))
except Exception as e:
    print(f"Failed to load isolated stage output: {e}")
"""

text_phase2 = """\
## 5. Phase 2: Information Distillation (Constrained Extraction)
Now we force the original unstructured context into the constraints of the dynamic schema via validation loop.
This will save its exact final models to `4_final_distilled_outputs.json`.
"""

code_phase2 = """\
# Extract empirical features against the dynamically discovered schema
constrained_outputs = []
sem = asyncio.Semaphore(orchestrator.max_concurrency)
tasks = [orchestrator._safe_extract_features(doc, discovered_schema, sem) for doc in docs]
constrained_outputs = await asyncio.gather(*tasks)

print("\\nSuccess! Context maps to Generalized Topologies natively.")
"""

text_final = """\
## 6. Inspect Final Dataset
Alternatively, you can skip full runtime computation and build entire frontend charts directly utilizing `stage_outputs/4_final_distilled_outputs.json`
"""

code_final = """\
for i, item in enumerate(constrained_outputs):
    print(f"--- Processed Document ID: {docs[i].id} ---")
    print(item.model_dump_json(indent=2))
    print("\\n")
"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text_intro),
    nbf.v4.new_code_cell(code_imports),
    nbf.v4.new_markdown_cell(text_docs),
    nbf.v4.new_code_cell(code_docs),
    nbf.v4.new_markdown_cell(text_orchestrator),
    nbf.v4.new_code_cell(code_orchestrator),
    nbf.v4.new_markdown_cell(text_phase1),
    nbf.v4.new_code_cell(code_phase1),
    nbf.v4.new_markdown_cell(text_inspect),
    nbf.v4.new_code_cell(code_inspect),
    nbf.v4.new_markdown_cell(text_phase2),
    nbf.v4.new_code_cell(code_phase2),
    nbf.v4.new_markdown_cell(text_final),
    nbf.v4.new_code_cell(code_final)
]

with open('full_workflow.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Created full_workflow.ipynb successfully.")
