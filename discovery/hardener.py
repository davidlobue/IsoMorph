import instructor
from typing import List, Dict, Type
from pydantic import create_model, BaseModel, Field
import re
from core.models import RawTriple, DiscoveryCluster
from core.config import LLMConfig
from core.prompts import Prompts

class HardenerEngine:
    """
    Executes Phase 2 of Discovery natively. 
    Connects to algorithmic modular communities to systematically extract central canonical predicates 
    and explicitly ban hallucinative traits via negative constraints.
    """
    def __init__(self):
        self.model_name = LLMConfig.get_model_name()
        self.async_client = LLMConfig.get_async_client()

    async def canonicalize_cluster(self, community_nodes: List[str], all_triples: List[RawTriple]) -> DiscoveryCluster:
        """
        Extracts all relevant topology edges involving the given subgraph and runs rigorous LLM evaluation to lock native structures.
        """
        # Filter all triples involving ANY node inside this community
        relevant_triples = [
            t for t in all_triples 
            if t.subject in community_nodes or t.object in community_nodes
        ]
        
        edges_json = "\\n".join([f"[{t.subject}] --({t.predicate})--> [{t.object}]" for t in relevant_triples])
        
        # Pydantic JSON enforcement natively handles canonical constraints
        response = await self.async_client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": Prompts.HARDENER_SYSTEM},
                {"role": "user", "content": Prompts.get_hardener_user(edges_json)}
            ],
            response_model=DiscoveryCluster
        )
        return response

    def generate_dynamic_schema(self, clusters: List[DiscoveryCluster]) -> Type[BaseModel]:
        """
        Dynamically generates hard Pydantic models from the canonicalized clusters defining rigid, constraint-based Python classes.
        """
        fields = {}
        for cluster in clusters:
            # We construct a nested schema for each detected class type
            class_fields = {}
            for predicate in cluster.canonical_predicates:
                # Sanitized pydantic string rules
                safe_predicate = re.sub(r'[^a-zA-Z0-9_]', '_', predicate.lower()).lstrip("_")
                if not safe_predicate:
                    safe_predicate = "unknown_property"
                elif safe_predicate[0].isdigit():
                    safe_predicate = "f_" + safe_predicate
                class_fields[safe_predicate] = (str, Field(..., description=f"Canonical property: {predicate}"))
            
            # Map negative constraints strictly onto the schema logic documentation block
            safe_class_name = "".join(x for x in cluster.class_name.title() if x.isalnum())
            if not safe_class_name:
                safe_class_name = "UnknownBlueprintClass"
            elif safe_class_name[0].isdigit():
                safe_class_name = "Class" + safe_class_name
                
            doc_string = f"Discovered Class: {cluster.class_name}.\\nSemantic Centroid / Role: {cluster.hypernym}\\nNEGATIVE CONSTRAINTS:\\n" + "\\n".join(f"- {nc}" for nc in cluster.negative_constraints)
            
            dynamic_model = create_model(f"{safe_class_name}Model", **class_fields)
            dynamic_model.__doc__ = doc_string
            
            field_key = safe_class_name.lower()
            fields[field_key] = (dynamic_model, Field(..., description=f"Dynamically generated schema for {cluster.class_name}"))

        fields['domain_summary'] = (str, Field(..., description="High-level summary of how the source text features were reliably mapped into this blueprint schema."))
        RootSchema = create_model("DiscoveredBlueprint", **fields)
        return RootSchema

    def export_schema_to_file(self, clusters: List[DiscoveryCluster], output_dir: str = "generated_schemas", human_readable: bool = True):
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        lines = [
            "# AUTO-GENERATED PYDANTIC KNOWLEDGE ONTOLOGY",
            "from pydantic import BaseModel, Field",
            "from typing import Optional, List",
            ""
        ]
        
        for cluster in clusters:
            safe_class_name = "".join(x for x in cluster.class_name.title() if x.isalnum())
            if not safe_class_name:
                safe_class_name = "UnknownBlueprintClass"
            elif safe_class_name[0].isdigit():
                safe_class_name = "Class" + safe_class_name
                
            lines.append(f"class {safe_class_name}Model(BaseModel):")
            
            doc_string = f"Discovered Class: {cluster.class_name}.\\n    Semantic Centroid / Role: {cluster.hypernym}\\n    NEGATIVE CONSTRAINTS:\\n" + "\\n".join(f"    - {nc}" for nc in cluster.negative_constraints)
            lines.append(f'    """\\n    {doc_string}\\n    """')
            
            if not cluster.canonical_predicates:
                lines.append("    pass")
            else:
                for predicate in cluster.canonical_predicates:
                    safe_predicate = re.sub(r'[^a-zA-Z0-9_]', '_', predicate.lower()).lstrip("_")
                    if not safe_predicate:
                        safe_predicate = "unknown_property"
                    elif safe_predicate[0].isdigit():
                        safe_predicate = "f_" + safe_predicate
                    lines.append(f'    {safe_predicate}: str = Field(..., description="Canonical property: {predicate}")')
            lines.append("")
            
        lines.append("class DiscoveredBlueprint(BaseModel):")
        lines.append('    domain_summary: str = Field(..., description="High-level summary of how the source text features were reliably mapped into this blueprint schema.")')
        if not clusters:
            lines.append("    pass")
        else:
            for cluster in clusters:
                safe_class_name = "".join(x for x in cluster.class_name.title() if x.isalnum())
                if not safe_class_name:
                    safe_class_name = "UnknownBlueprintClass"
                elif safe_class_name[0].isdigit():
                    safe_class_name = "Class" + safe_class_name
                    
                field_key = safe_class_name.lower()
                lines.append(f'    {field_key}: {safe_class_name}Model = Field(..., description="Dynamically generated schema for {cluster.class_name}")')
                
        with open(os.path.join(output_dir, "models.py"), "w") as f:
            if human_readable:
                f.write("\n".join(lines))
            else:
                f.write("\\n".join(lines))
            
        print(f"[+] Successfully exported rigid Pydantic models to {output_dir}/models.py natively.")
