# AUTO-GENERATED PYDANTIC KNOWLEDGE ONTOLOGY
from pydantic import BaseModel, Field
from typing import Optional, List

class ActionModel(BaseModel):
    """\n    Discovered Class: Action.\n    NEGATIVE CONSTRAINTS:\n    - NEVER - (Not a TemporalEvent: HasLocation)\n    - NEVER - (Not a TemporalEvent: HasPhysicalAddress)\n    """
    dateofevaluation____datetime: str = Field(..., description="Canonical property: DateOfEvaluation -> DateTime")
    dateofreport____datetime: str = Field(..., description="Canonical property: DateOfReport -> DateTime")

class AgentModel(BaseModel):
    """\n    Discovered Class: Agent.\n    NEGATIVE CONSTRAINTS:\n    - <PERSON> --(is_dead)-->\n    - <PERSON> --(has_positive_thinking)-->\n    """
    name: str = Field(..., description="Canonical property: Name")
    date_of_birth: str = Field(..., description="Canonical property: Date of Birth")
    grade: str = Field(..., description="Canonical property: Grade")
    clinician: str = Field(..., description="Canonical property: Clinician")
    referral_reason: str = Field(..., description="Canonical property: Referral Reason")
    cooperative_status: str = Field(..., description="Canonical property: Cooperative Status")
    eye_contact: str = Field(..., description="Canonical property: Eye Contact")
    seat_behavior: str = Field(..., description="Canonical property: Seat Behavior")
    task_avoidance: str = Field(..., description="Canonical property: Task Avoidance")
    thinking_style: str = Field(..., description="Canonical property: Thinking Style")
    inattention__parental_concerns_: str = Field(..., description="Canonical property: Inattention (Parental Concerns)")
    emotional_reactivity__score_: str = Field(..., description="Canonical property: Emotional Reactivity (Score)")
    executive_functioning: str = Field(..., description="Canonical property: Executive Functioning")
    adhd_diagnosis: str = Field(..., description="Canonical property: ADHD Diagnosis")
    anxiety_disorder_diagnosis: str = Field(..., description="Canonical property: Anxiety Disorder Diagnosis")
    has_problem_at_home: str = Field(..., description="Canonical property: has_problem_at_home")
    has_issue_at_school: str = Field(..., description="Canonical property: has_issue_at_school")
    has_impulse_control_problem_at_school: str = Field(..., description="Canonical property: has_impulse_control_problem_at_school")
    has_executive_function_dysfunction_at_school: str = Field(..., description="Canonical property: has_executive_function_dysfunction_at_school")
    struggles_with: str = Field(..., description="Canonical property: struggles_with")
    meets_criteria_for: str = Field(..., description="Canonical property: meets_criteria_for")
    also_has: str = Field(..., description="Canonical property: also_has")

class ObjectModel(BaseModel):
    """\n    Discovered Class: Object.\n    NEGATIVE CONSTRAINTS:\n    - NEVER possess 'Score' --> 'Below Average range' as it is a 'Low Average range' cluster.\n    - NEVER have other than ['Working Memory', 'Processing Speed'] in the SubtestName, given their mutual exclusivity and cluster singularity.\n    """
    subtestname: str = Field(..., description="Canonical property: SubtestName")
    cognitivedomain: str = Field(..., description="Canonical property: CognitiveDomain")
    scoringproperty: str = Field(..., description="Canonical property: ScoringProperty")

class ContextModel(BaseModel):
    """\n    Discovered Class: Context.\n    NEGATIVE CONSTRAINTS:\n    - A clinical evaluation report should NEVER have a 'date_of_evaluation' that is later than its 'date_of_report'.\n    - This means, for each instance of <CLINICAL_EVALUATION_REPORT>\n    - the 'date_of_evaluation' cannot be after the 'date_of_report'.\n    """
    date_of_evaluation__with_type_date_: str = Field(..., description="Canonical property: date_of_evaluation (with type Date)")
    date_of_report__with_type_date_: str = Field(..., description="Canonical property: date_of_report (with type Date)")

class DiscoveredBlueprint(BaseModel):
    reasoning: str = Field(..., description="Step-by-step reasoning explaining how the source text features were reliably mapped into this blueprint schema.")
    action: ActionModel = Field(..., description="Dynamically generated schema for Action")
    agent: AgentModel = Field(..., description="Dynamically generated schema for Agent")
    object: ObjectModel = Field(..., description="Dynamically generated schema for Object")
    context: ContextModel = Field(..., description="Dynamically generated schema for Context")