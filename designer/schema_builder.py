from pydantic import create_model, BaseModel, Field
from typing import Type, Any, Dict
from core.models import KnowledgeGraph

class SchemaBuilder:
    def __init__(self, strict_typing: bool = True):
        self.strict_typing = strict_typing

    def synthesize_schema(self, knowledge_graph: KnowledgeGraph, schema_name: str = "UniversalBlueprint") -> Type[BaseModel]:
        """
        Dynamically constructs a Pydantic BaseModel from the derived Knowledge Graph layout.
        This schema represents the "Essential Form" of the area, geared for Zero False Positives.
        """
        fields: Dict[str, Any] = {}
        
        # In a robust implementation, the graph properties map directly to required Pydantic fields.
        for node in knowledge_graph.nodes:
            # We skip generic categories (like IS_A target nodes) if they don't have properties
            # Instead we look at the node id (species) and use its properties to define fields.
            
            # Example heuristic: If the node has properties, we build a nested Pydantic model for it.
            if node.properties:
                nested_fields = {}
                for prop_name, prop_val in node.properties.items():
                    # Simplified typing assumption: all traits are string or inferable
                    # If strict_typing is True, we enforce strict python constraints here.
                    field_type = type(prop_val) if prop_val is not None else str
                    nested_fields[prop_name] = (field_type, Field(..., description=f"Extracted trait: {prop_name}"))
                
                # Sanitize node id to make it a valid class name
                safe_node_id = "".join(x for x in node.id.title() if x.isalnum())
                dynamic_nested_model = create_model(f"{safe_node_id}Model", **nested_fields)
                
                # Add this nested model to our root fields
                field_key = node.id.replace(" ", "_").lower()
                fields[field_key] = (dynamic_nested_model, Field(..., description=f"Form for {node.id} ({node.type})"))

        # Finally, create the root schema
        BlueprintSchema = create_model(schema_name, **fields)
        return BlueprintSchema

if __name__ == "__main__":
    # Test Synthesis
    from core.models import KnowledgeGraphNode
    kg = KnowledgeGraph(
        nodes=[
            KnowledgeGraphNode(id="Buyer Entity", type="Actor", properties={"is_corporate": True, "jurisdiction": "USA"}),
            KnowledgeGraphNode(id="Purchase Event", type="Event", properties={"amount": 0.0, "currency": "USD"})
        ]
    )
    
    builder = SchemaBuilder()
    SynthesizedModel = builder.synthesize_schema(kg)
    print("Schema Synthesized:", SynthesizedModel.model_json_schema())
