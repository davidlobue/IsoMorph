class RefinementPrompts:
    TAXONOMIC_LIFTING_SYSTEM = """
    You are an Ontological Lifting Agent mapping raw discovered classes to a High-Level Top-Level Ontology (such as BFO or DOLCE).
    Your objective is to lift specific, surface-level lexical classes into generalized, cross-domain ancestor classes (Semantic Centroids).
    You will be provided with structural role hints (like Entity, Attribute, or Relational Verb) which should strictly guide your naming convention.
    """

    @staticmethod
    def get_taxonomic_lifting_user(class_data: str, structural_hint: str) -> str:
        return f"""
        Lift the following class definition into a generalized top-level ontology category. 
        Provide the explicit geometric structural role constraint as a context hint. 
        Instead of reasoning, provide the formal 'is-a' Semantic Centroid (Hypernym).
        
        <structural_role_hint>
        {structural_hint}
        </structural_role_hint>
        
        <class_data>
        {class_data}
        </class_data>
        """

    STRUCTURAL_ROLE_SYSTEM = """
    You are a Structural Role Abstraction Agent. You ignore lexical domain semantics entirely and focus strictly on topological function.
    Your objective is to classify a group of nodes based purely on their structural behavior in the graph (e.g., "High Out-Degree Entity", "Terminal Attribute", "Relational Verb Bridge"). 
    """

    @staticmethod
    def get_structural_role_user(class_data: str, metrics: str) -> str:
        return f"""
        Given the following class and its graph topology metrics (in-degree, out-degree, centrality), abstract this class name to represent its systemic structural role. Use the structural type-cast (Entity, Attribute, Relational Verb) as the guiding principle.
        
        <class_data>
        {class_data}
        </class_data>
        <metrics>
        {metrics}
        </metrics>
        """

    SEEDED_META_SCHEMA_SYSTEM = """
    You are a Meta-Schema Assignment Agent.
    Your objective is to map newly discovered classes strictly into one of the user-provided "Golden Schema" foundational buckets.
    You must classify the provided concept as exactly one of the seeded definitions, preventing narrow-scope domain traps.
    """

    @staticmethod
    def get_seeded_meta_schemas_user(class_data: str, seeds: str) -> str:
        return f"""
        Map the following discovered class into ONE of the exact "Golden Schema" categories provided below.
        
        <golden_schema>
        {seeds}
        </golden_schema>
        
        <class_data>
        {class_data}
        </class_data>
        """
