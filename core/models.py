from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class SourceQuote(BaseModel):
    quote: str = Field(description="The exact quote from the source text.")
    context: str = Field(description="Brief explanation of the context in which this quote appeared.")

class RawTriple(BaseModel):
    subject: str = Field(description="The source entity node.")
    predicate: str = Field(description="The relationship or action linking Subject to Object.")
    object: str = Field(description="The target entity node or literal value.")

class TripleExtractionResult(BaseModel):
    triples: List[RawTriple] = Field(default_factory=list, description="List of extracted open triples.")

class DiscoveryCluster(BaseModel):
    class_name: str = Field(description="The inferred name for this clustered class (e.g. 'Company', 'Person').")
    nodes: List[str] = Field(description="Entity nodes that belong to this cluster.")
    canonical_predicates: List[str] = Field(description="The canonical structural properties (edges) this class exhibits.")
    negative_constraints: List[str] = Field(description="Fields/predicates that definitely do NOT belong to this class.")

class ExtractedRelationship(BaseModel):
    target_entity: str = Field(description="The name of the entity this feature connects to.")
    relationship_type: str = Field(description="The nature of the connectedness (e.g. 'walks', 'speaks to').")

class AtomicFeature(BaseModel):
    name: str = Field(description="The distinct name of the identified entity, object, event, or relationship.")
    type: str = Field(description="Categorization of the feature (e.g., Person, Organization, Event, Tone).")
    description: str = Field(description="Detailed explanation of the feature.")
    source_grounding: SourceQuote = Field(description="Direct evidence from the text.")
    certainty_score: float = Field(description="Confidence score from 0.0 to 1.0 that this feature actually meant what was extracted.")
    relationships: List[ExtractedRelationship] = Field(default_factory=list, description="0...N explicitly stated node-edge relationships connecting this entity to others.")

class FeatureExtractionResult(BaseModel):
    features: List[AtomicFeature] = Field(default_factory=list, description="Extracted atomic features from the source text.")

class AbstractionCategory(BaseModel):
    hierarchy: List[str] = Field(description="The natural hierarchical chain of abstraction from the broadest category down to the specific sub-type. (e.g., ['Behavior', 'Social Interaction', 'Direct Contact', 'Avoids Eye Contact'])")

class Differentiator(BaseModel):
    name: str = Field(description="The unique distinguishing trait.")
    value: List[str] = Field(description="The specific value(s) of this differentiator (single string or multiple examples) that makes it Unique across similar entities.")

class EntityOntology(BaseModel):
    feature_name: str
    category: AbstractionCategory
    differentiators: List[Differentiator]

class EntityOntologyList(BaseModel):
    ontologies: List[EntityOntology] = Field(description="The categorized grouped ontologies ensuring MECE properties.")

class KnowledgeGraphNode(BaseModel):
    id: str = Field(description="Unique identifier for the node (usually the form/species).")
    type: str = Field(description="The generic category Type (Genus).")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Metadata properties derived from differentiators.")

class KnowledgeGraphEdge(BaseModel):
    source: str = Field(description="Source node ID.")
    target: str = Field(description="Target node ID.")
    relationship: str = Field(description="How the source relates to the target.")

class KnowledgeGraph(BaseModel):
    nodes: List[KnowledgeGraphNode] = Field(default_factory=list)
    edges: List[KnowledgeGraphEdge] = Field(default_factory=list)

class DocumentSource(BaseModel):
    id: str
    text_content: str
