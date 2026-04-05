import sys
import os
# Allow imports from local directory if running inside the ontology folder
if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

from core.models import DocumentSource
from pipeline.orchestrator import Orchestrator


doc1 = DocumentSource(
    id="doc_001",
    text_content="""
    Patient Assessment - Oct 4, 2023:
    Jordan exhibited highly repetitive physical motions, specifically hand-flapping, 
    when the classroom environment became too loud. He did not engage in verbal communication for 45 minutes.
    """
)

doc2 = DocumentSource(
    id="doc_002",
    text_content="""
    In-home Observation - Oct 5, 2023:
    During dinner, Jordan successfully maintained eye contact with his sibling when asking for water.
    However, when transitioned to bedtime, severe physical agitation and distress was observed.
    """
)

docs = [doc1, doc2]


import os
from dotenv import load_dotenv
load_dotenv()

from pipeline.orchestrator import Orchestrator

orchestrator = Orchestrator(
    max_concurrency=4,
    hallucination_filter=True,
    ontology_depth=None,
    strict_typing=True,
    verbose=True,
    generalize_latent_space=True,
    generalize_structural_roles=True,
    generalize_taxonomic_lifting=True,
    generalize_seeded_schemas=True
)

import asyncio

async def main():
    try:
        final_schemas = await orchestrator.run_pipeline(docs)
        return final_schemas[0] if final_schemas else None
    except Exception as e:
        print(f"Pipeline Error: {e}")
        print("Is your LLM connection running locally, or did you export LLM_BASE_URL?")
        return None

final_schema = asyncio.run(main())


if final_schema:
    print("Final Dynamic Schema JSON Definition:\n")
    import json
    print(json.dumps(final_schema.model_json_schema(), indent=2))

