import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pytest
from unittest.mock import patch, MagicMock
from medical.med_history.patient_medical_history import PatientMedicalHistoryGenerator
from medical.med_history.patient_medical_history_prompts import MedicalHistoryInput
from lite.config import ModelConfig
from medical.med_history.patient_medical_history_models import (
    PatientMedicalHistoryModel, ModelOutput, PastMedicalHistoryQuestionsModel,
    FamilyHistoryQuestionsModel, DrugInformationQuestionsModel,
    VaccinationQuestionsModel, LifestyleAndSocialQuestionsModel,
    QuestionRequirement, PastConditionQuestionModel, FollowUpQuestionModel
)

@pytest.fixture
def mock_lite_client():
    with patch('medical.med_history.patient_medical_history.LiteClient') as mock:
        yield mock

def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = PatientMedicalHistoryGenerator(config)
    assert generator.model_config == config

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = PatientMedicalHistoryGenerator(config)
    user_input = MedicalHistoryInput(exam="Cardiac", age=45, gender="Male")
    
    mock_output = ModelOutput(markdown="History questions", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = generator.generate_text(user_input)
    assert result.markdown == "History questions"
    assert generator.user_input == user_input

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = PatientMedicalHistoryGenerator(config)
    user_input = MedicalHistoryInput(exam="Cardiac", age=45, gender="Male")
    
    # Minimal mock data for structured output
    mock_data = PatientMedicalHistoryModel(
        purpose="physical_exam",
        exam="Cardiac",
        age=45,
        gender="Male",
        past_medical_history=PastMedicalHistoryQuestionsModel(
            condition_questions=[
                PastConditionQuestionModel(
                    question="History of high blood pressure?",
                    clinical_relevance="Risk factor",
                    requirement=QuestionRequirement.MANDATORY,
                    expected_answer_type="yes/no",
                    condition_category="Cardiac",
                    follow_up_questions=[FollowUpQuestionModel(question="Since when?", clinical_reason="Duration matters", investigation_focus="Severity")]
                )
            ],
            hospitalization_questions=[],
            surgery_questions=[]
        ),
        family_history=FamilyHistoryQuestionsModel(maternal_history_questions=[], paternal_history_questions=[], genetic_risk_questions=[]),
        drug_information=DrugInformationQuestionsModel(medication_questions=[], allergy_questions=[], adverse_reaction_questions=[]),
        vaccination=VaccinationQuestionsModel(vaccination_status_questions=[], vaccine_specific_questions=[], booster_questions=[]),
        lifestyle_and_social=LifestyleAndSocialQuestionsModel(lifestyle_questions=[], personal_social_questions=[])
    )
    
    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    result = generator.generate_text(user_input, structured=True)
    assert result.data.exam == "Cardiac"

@patch('medical.med_history.patient_medical_history.save_model_response')
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = PatientMedicalHistoryGenerator(config)
    user_input = MedicalHistoryInput(exam="Cardiac", age=45, gender="Male")
    mock_output = ModelOutput(markdown="Questions")
    mock_lite_client.return_value.generate_text.return_value = mock_output
    
    generator.generate_text(user_input)
    generator.save(mock_output, Path("/tmp"))
    
    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("cardiac_medical_history")
