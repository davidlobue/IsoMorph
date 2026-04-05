class RefinementPrompts:
    TAXONOMIC_LIFTING_SYSTEM = """
    You are an Ontological Lifting Agent mapping raw discovered classes to a High-Level Top-Level Ontology (such as BFO or DOLCE).
    Your objective is to lift specific, surface-level lexical classes (like "Water Density" or "Neutron Star") into generalized, cross-domain ancestor classes (like "Physical Property", "Celestial Object", or "Process").
    """

    @staticmethod
    def get_taxonomic_lifting_user(class_data: str) -> str:
        return f"""
        Lift the following class definition into a generalized top-level ontology category. Provide the new class name and optionally abstract its predicates.
        
        <class_data>
        {class_data}
        </class_data>
        """

    STRUCTURAL_ROLE_SYSTEM = """
    You are a Structural Role Abstraction Agent. You ignore lexical domain semantics entirely and focus strictly on topological function.
    Your objective is to rename and classify a group of nodes based purely on their structural behavior in the graph (e.g., "High-Centrality Hub", "Dependent Component", "Terminal Attribute", "Bridge Node"). 
    """

    @staticmethod
    def get_structural_role_user(class_data: str, metrics: str) -> str:
        return f"""
        Given the following class and its graph topology metrics (centrality, degree spread), abstract this class name to represent its systemic structural role instead of its literal text meaning.
        
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
