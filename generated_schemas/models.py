# AUTO-GENERATED PYDANTIC KNOWLEDGE ONTOLOGY
from pydantic import BaseModel, Field
from typing import Optional, List

class AgentModel(BaseModel):
    """\n    Discovered Class: Agent.\n    NEGATIVE CONSTRAINTS:\n    - SHOULD NOT have an age less than 0 or greater than 18.\n    - MAY NOT be referred by a system that is not defined as an [ORGANIZATION] or [PERSON].\n    - MUST be present with at least one of the assessments like (has done assessment)\n    """
    has_name_: str = Field(..., description="Canonical property: (has name)")
    was_born_on_: str = Field(..., description="Canonical property: (was born on)")
    is_chronologically_: str = Field(..., description="Canonical property: (is chronologically)")
    is_aged_: str = Field(..., description="Canonical property: (is aged)")
    is_in_grade_: str = Field(..., description="Canonical property: (is in grade)")
    has_gender_: str = Field(..., description="Canonical property: (has gender)")
    has_a_developmental_history_with_: str = Field(..., description="Canonical property: (has a developmental history with)")
    received_the_following_diagnoses_: str = Field(..., description="Canonical property: (received the following diagnoses)")
    attends_: str = Field(..., description="Canonical property: (attends)")
    has_: str = Field(..., description="Canonical property: (has)")
    negative_constraints_for_schema_hardening_agent_to_prevent_hallucinations: str = Field(..., description="Canonical property: negative_constraints_for_schema_hardening_agent_to_prevent_hallucinations")
    never_possesses__18_years_old_if__is_in_grade__has_a_value_greater_than_or_equal_to__6th_grade___: str = Field(..., description="Canonical property: NEVER possesses <18 years old if 'is in grade' has a value greater than or equal to '6th Grade'. ")
    never_possesses_a__name__attribute_if___was_born_on___and___has_name___are_missing_: str = Field(..., description="Canonical property: NEVER possesses a 'name' attribute if '(was born on)' and '(has name)' are missing.")
    never_exhibits_: str = Field(..., description="Canonical property: NEVER exhibits ")
    has_: str = Field(..., description="Canonical property: (has)")
    a_minimum_of_four_to_five_verbal_prompts: str = Field(..., description="Canonical property: a minimum of four to five verbal prompts")
    without_prompting_if___had_issues_in___is_not_present_: str = Field(..., description="Canonical property:  without prompting if '(had issues in)' is not present ")
    never_has_superior_range_performance_if______struggles_to_output_the_work_at_the_same_pace_as_their_peers__missing_: str = Field(..., description="Canonical property: NEVER has Superior range performance if ',' (struggles to output the work at the same pace as their peers' missing.")
    never_meets_criteria_for__diagnosis__if___patient_____meets_the_diagnostic_criteria_for______diagnosis___is_not_explicitly_defined_: str = Field(..., description="Canonical property: NEVER meets criteria for <Diagnosis> if '<PATIENT> --(meets the diagnostic criteria for)--> <Diagnosis>' is not explicitly defined.")
    never_has__escape_behaviors__during_home_work_sessions__without_having__has_behavioral_issues_in_class_room_: str = Field(..., description="Canonical property: NEVER has 'escape behaviors' during home work sessions, without having (has behavioral issues in class room)")
    never_possesses_a__: str = Field(..., description="Canonical property: NEVER possesses a '")
    freqntly_blurt_out_answers_before_the_teacher____with_having___has_attention_deficits_in_classroom___: str = Field(..., description="Canonical property: (freqntly blurt out answers before the teacher',' with having '(has attention deficits in classroom)' ")

class ActionModel(BaseModel):
    """\n    Discovered Class: Action.\n    NEGATIVE CONSTRAINTS:\n    - NEVER possess a title with profanity.\n    - NEVER contain hate speech directed towards any involved parties.\n    - NEVER provide recommendations that are contradictory or misleading.\n    - NEVER target an age group under 5 years old (as the context is school performance and family functioning).\n    """
    title: str = Field(..., description="Canonical property: title")
    purpose: str = Field(..., description="Canonical property: purpose")
    content: str = Field(..., description="Canonical property: content")
    target_audience: str = Field(..., description="Canonical property: target_audience")
    recommendations: str = Field(..., description="Canonical property: recommendations")
    involved_parties: str = Field(..., description="Canonical property: involved_parties")

class ObjectModel(BaseModel):
    """\n    Discovered Class: Object.\n    NEGATIVE CONSTRAINTS:\n    - NEVER possesses: consistent_stellar_attention_span\n    - NEVER possesses: minimal_daydreaming_during_classes\n    - NEVER possesses: emotional_balance_during_task_transitions\n    """
    included_symptom__persistent_difficulties_with_sustained_attention: str = Field(..., description="Canonical property: included_symptom: persistent_difficulties_with_sustained_attention")
    included_symptom__frequent_daydreaming_in_class: str = Field(..., description="Canonical property: included_symptom: frequent_daydreaming_in_class")
    included_symptom__significant_emotional_reactivity_when_transitioning_between_tasks: str = Field(..., description="Canonical property: included_symptom: significant_emotional_reactivity_when_transitioning_between_tasks")

class MechanismModel(BaseModel):
    """\n    Discovered Class: Mechanism.\n    NEGATIVE CONSTRAINTS:\n    - is_not_intervention\n    """
    used_in_child_assessment: str = Field(..., description="Canonical property: used_in_child_assessment")

class ActionModel(BaseModel):
    """\n    Discovered Class: Action.\n    NEGATIVE CONSTRAINTS:\n    - DOES NOT recommend FOR medication_or_fine_repayment Plan types\n    - cannot_recommend_non_educational_services\n    - So, it's explicitly defined that these entities cannot have any attributes or relations related to medication recommendation or non-education services like financial repayment.\n    """
    recommended_for_plan__individualizededucationprogram_504plan_enum: str = Field(..., description="Canonical property: recommended_for_plan: IndividualizedEducationProgram|504Plan Enum")
    so___504plan__and__individualizededucationprogram__are_possible_values_for_a__plans__attribute_: str = Field(..., description="Canonical property: So, `504Plan` and `IndividualizedEducationProgram` are possible values for a `plans` attribute.")

class DiscoveredBlueprint(BaseModel):
    reasoning: str = Field(..., description="Step-by-step reasoning explaining how the source text features were reliably mapped into this blueprint schema.")
    agent: AgentModel = Field(..., description="Dynamically generated schema for Agent")
    action: ActionModel = Field(..., description="Dynamically generated schema for Action")
    object: ObjectModel = Field(..., description="Dynamically generated schema for Object")
    mechanism: MechanismModel = Field(..., description="Dynamically generated schema for Mechanism")
    action: ActionModel = Field(..., description="Dynamically generated schema for Action")