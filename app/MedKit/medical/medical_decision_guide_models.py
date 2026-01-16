"""Pydantic models for medical decision guides.

Defines the schema for decision trees used in medical symptom assessment.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class DecisionNode(BaseModel):
    """Single decision point in the symptom assessment tree."""
    node_id: str = Field(description="Unique identifier for this decision node")
    question: str = Field(description="Question to ask the patient")
    yes_node_id: str = Field(description="Node ID to go to if answer is yes")
    no_node_id: str = Field(description="Node ID to go to if answer is no")
    uncertain_node_id: Optional[str] = Field(default=None, description="Node ID to go to if answer is uncertain (optional - if present, creates third branch)")


class Outcome(BaseModel):
    """Terminal node of a decision tree - assessment outcome."""
    outcome_id: str = Field(description="Unique identifier for this outcome")
    severity_level: str = Field(description="Assessed severity (mild, moderate, severe, emergency)")
    urgency: str = Field(description="Care urgency (self-care, urgent-care, emergency, specialist)")
    recommendation: str = Field(description="Clinical recommendation and next steps")
    possible_diagnoses: str = Field(description="Possible diagnoses to consider, comma-separated")
    home_care_advice: str = Field(description="Home management strategies if appropriate")
    warning_signs: str = Field(description="Red flags requiring immediate attention, comma-separated")


class MedicalDecisionGuide(BaseModel):
    """
    Medical decision tree for symptom assessment.

    Structured decision tree with yes/no questions leading to outcomes
    and recommendations for different age groups.
    """
    guide_name: str = Field(description="Name of the decision guide")
    primary_symptom: str = Field(description="Main symptom this guide addresses")
    secondary_symptoms: str = Field(description="Associated symptoms covered, comma-separated")
    age_groups_covered: str = Field(description="Age ranges addressed, comma-separated")
    scope: str = Field(description="What conditions this guide covers and what it doesn't")

    start_node_id: str = Field(description="ID of the first question/decision node")
    decision_nodes: List[DecisionNode] = Field(description="All decision nodes in order")
    outcomes: List[Outcome] = Field(description="All terminal outcomes")

    warning_signs: str = Field(description="Red flags requiring immediate attention, comma-separated")
    emergency_indicators: str = Field(description="Signs of medical emergency, comma-separated")
