import argparse
import logging
import sys
from pathlib import Path
from tqdm import tqdm

# Add the current directory to sys.path to support relative imports in this module
sys.path.append(str(Path(__file__).parent))

from lite.config import ModelConfig
from lite.logging_config import configure_logging

# Import generators
from anatomy.medical_anatomy import MedicalAnatomyGenerator
from disease_info.disease_info import DiseaseInfoGenerator
from herbal_info.herbal_info import HerbalInfoGenerator
from med_advise.primary_health_care import PrimaryHealthCareProvider
from med_decision_guide.medical_decision_guide import MedicalDecisionGuideGenerator
from med_facts_checker.medical_facts_checker import MedicalFactsChecker
from med_faqs.medical_faq import MedicalFAQGenerator
from med_implant.medical_implant import MedicalImplantGenerator
from med_myths_checker.medical_myth_checker import MedicalMythsChecker
from med_physical_exams_questions.medical_physical_exams_questions import ExamQuestionGenerator as PhysicalExamGenerator
from med_procedure_info.medical_procedure_info import MedicalProcedureInfoGenerator
from med_procedure_info.eval_medical_procedure_output import MedicalProcedureEvaluator
from med_quiz.medical_quiz import MedicalQuizGenerator
from med_refer.med_refer import MedReferral
from med_speciality_roles.med_speciality_roles import MedSpecialityRoles
from med_topic.medical_topic import MedicalTopicGenerator
from organ_diseases.organ_disease_info import DiseaseInfoGenerator as OrganDiseaseGenerator
from surgical_info.surgical_info import SurgeryInfoGenerator 
from surgical_pose_info.surgical_pose_info import SurgicalPoseInfoGenerator
from surgical_tool_info.surgical_tool_info import SurgicalToolInfoGenerator
from surgical_tray.surgical_tray_info import SurgicalTrayGenerator
from synthetic_case_report.synthetic_case_report import SyntheticCaseReportGenerator
from med_history.patient_medical_history import PatientMedicalHistoryGenerator
from med_history.patient_medical_history_prompts import MedicalHistoryInput
from med_ethics.med_ethics import MedEthicalQA
from med_flashcard.medical_flashcard import MedicalLabelExtractor, MedicalTermExplainer

logger = logging.getLogger(__name__)

def handle_batch_input(input_val: str, desc: str):
    input_path = Path(input_val)
    if input_path.is_file():
        with open(input_path, 'r', encoding='utf-8') as f:
            items = [line.strip() for line in f if line.strip()]
        logger.debug(f"Read {len(items)} items from file: {input_path}")
        return items
    return [input_val]

def main():
    parser = argparse.ArgumentParser(description="MedKit Unified CLI - Access all medical AI tools.")
    
    # Global arguments
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument("-d", "--output-dir", default="outputs", help="Output directory.")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Verbosity level.")
    parser.add_argument("-s", "--structured", action="store_true", help="Use structured output.")

    subparsers = parser.add_subparsers(dest="command", required=True, help="Medical tool subcommands")

    # Anatomy
    anatomy_p = subparsers.add_parser("anatomy", help="Generate anatomical info")
    anatomy_p.add_argument("body_part", help="Body part or file path")

    # Disease Info
    disease_p = subparsers.add_parser("disease", help="Generate disease info")
    disease_p.add_argument("disease", help="Disease name or file path")

    # Herbal Info
    herbal_p = subparsers.add_parser("herbal", help="Generate herbal info")
    herbal_p.add_argument("herb", help="Herb name or file path")

    # PHC Advise
    advise_p = subparsers.add_parser("advise", help="Primary Health Care advice")
    advise_p.add_argument("query", help="Health concern or file path")

    # Decision Guide
    decision_p = subparsers.add_parser("decision", help="Medical decision guide")
    decision_p.add_argument("symptom", help="Symptom name or file path")

    # Facts Checker
    facts_p = subparsers.add_parser("facts", help="Check medical facts")
    facts_p.add_argument("statement", help="Statement or file path")

    # FAQs
    faq_p = subparsers.add_parser("faq", help="Generate medical FAQs")
    faq_p.add_argument("topic", help="Medical topic or file path")

    # Implant
    implant_p = subparsers.add_parser("implant", help="Medical implant info")
    implant_p.add_argument("implant", help="Implant name or file path")

    # Myth Checker
    myth_p = subparsers.add_parser("myth", help="Check medical myths")
    myth_p.add_argument("input", help="Medical myth or file path")

    # Procedure Info
    proc_p = subparsers.add_parser("procedure", help="Medical procedure info")
    proc_p.add_argument("procedure", help="Procedure name or file path")

    # Eval Procedure
    eval_proc_p = subparsers.add_parser("eval-procedure", help="Evaluate procedure documentation")
    eval_proc_p.add_argument("file", help="File path to evaluate or file containing paths")

    # Quiz
    quiz_p = subparsers.add_parser("quiz", help="Generate medical quiz")
    quiz_p.add_argument("topic", help="Topic or file path")
    quiz_p.add_argument("--difficulty", default="Intermediate")
    quiz_p.add_argument("--num-questions", type=int, default=5)
    quiz_p.add_argument("--num-options", type=int, default=4)

    # Refer
    refer_p = subparsers.add_parser("refer", help="Recommend specialists")
    refer_p.add_argument("question", help="Symptoms or file path")

    # Roles
    roles_p = subparsers.add_parser("roles", help="Speciality roles and responsibilities")
    roles_p.add_argument("speciality", help="Speciality or file path")

    # Topic
    topic_p = subparsers.add_parser("topic", help="General medical topic info")
    topic_p.add_argument("topic", help="Topic or file path")

    # Organ
    organ_p = subparsers.add_parser("organ", help="Organ-specific disease info")
    organ_p.add_argument("organ", help="Organ name or file path")

    # Surgery
    surgery_p = subparsers.add_parser("surgery", help="Surgical procedure info")
    surgery_p.add_argument("surgery", help="Surgery name or file path")

    # Pose
    pose_p = subparsers.add_parser("pose", help="Surgical positioning info")
    pose_p.add_argument("pose", nargs="?", help="Position name or file path")
    pose_p.add_argument("-l", "--list", action="store_true")

    # Tool
    tool_p = subparsers.add_parser("tool", help="Surgical tool info")
    tool_p.add_argument("tool", help="Tool name or file path")

    # Tray
    tray_p = subparsers.add_parser("tray", help="Surgical tray setup info")
    tray_p.add_argument("surgery", help="Surgery name or file path")

    # Case Report
    case_p = subparsers.add_parser("case", help="Synthetic case report generator")
    case_p.add_argument("condition", help="Condition name or file path")

    # Ethics
    ethics_p = subparsers.add_parser("ethics", help="Medical ethics analysis")
    ethics_p.add_argument("question", help="Ethics question or file path")

    # Flashcard
    flashcard_p = subparsers.add_parser("flashcard", help="Explain medical labels from an image")
    flashcard_p.add_argument("image", help="Path to medical image or label")

    # Medical History
    history_p = subparsers.add_parser("history", help="Patient medical history questions")
    history_p.add_argument("-e", "--exam", required=True)
    history_p.add_argument("-a", "--age", type=int, required=True)
    history_p.add_argument("-g", "--gender", required=True)
    history_p.add_argument("-p", "--purpose", default="physical_exam")

    args = parser.parse_args()

    # Logging config
    configure_logging(log_file="medkit_unified.log", verbosity=args.verbosity, enable_console=True)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    model_config = ModelConfig(model=args.model, temperature=0.2)

    try:
        if args.command == "anatomy":
            gen = MedicalAnatomyGenerator(model_config)
            for item in tqdm(handle_batch_input(args.body_part, "anatomy"), desc="Anatomy"):
                res = gen.generate_text(body_part=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "disease":
            gen = DiseaseInfoGenerator(model_config)
            for item in tqdm(handle_batch_input(args.disease, "disease"), desc="Disease"):
                res = gen.generate_text(disease=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "herbal":
            gen = HerbalInfoGenerator(model_config)
            for item in tqdm(handle_batch_input(args.herb, "herbal"), desc="Herbal"):
                res = gen.generate_text(herb=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "advise":
            gen = PrimaryHealthCareProvider(model_config)
            for item in tqdm(handle_batch_input(args.query, "advise"), desc="Advise"):
                res = gen.generate_text(query=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "decision":
            gen = MedicalDecisionGuideGenerator(model_config)
            for item in tqdm(handle_batch_input(args.symptom, "decision"), desc="Decision"):
                res = gen.generate_text(symptom=item, structured=args.structured)
                if res:
                    path = output_dir / f"{item.lower().replace(' ', '_')}_decision.json"
                    gen.save(res, path)

        elif args.command == "facts":
            gen = MedicalFactsChecker(model_config)
            from lite.utils import save_model_response
            for item in tqdm(handle_batch_input(args.statement, "facts"), desc="Facts"):
                res = gen.generate_text(statement=item, structured=args.structured)
                if res:
                    fname = "".join([c if c.isalnum() else "_" for c in item.lower()])[:50]
                    save_model_response(res, output_dir / f"{fname}.json")

        elif args.command == "faq":
            gen = MedicalFAQGenerator(model_config)
            for item in tqdm(handle_batch_input(args.topic, "faq"), desc="FAQ"):
                res = gen.generate_text(topic=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "implant":
            gen = MedicalImplantGenerator(model_config)
            for item in tqdm(handle_batch_input(args.implant, "implant"), desc="Implant"):
                res = gen.generate_text(implant=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "myth":
            gen = MedicalMythsChecker(model_config)
            for item in tqdm(handle_batch_input(args.input, "myth"), desc="Myth"):
                res = gen.generate_text(myth=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "procedure":
            gen = MedicalProcedureInfoGenerator(model_config)
            for item in tqdm(handle_batch_input(args.procedure, "procedure"), desc="Procedure"):
                res = gen.generate_text(procedure=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "eval-procedure":
            gen = MedicalProcedureEvaluator(model_config)
            for item in tqdm(handle_batch_input(args.file, "eval-procedure"), desc="Eval Proc"):
                res = gen.generate_text(file_path=item)
                if res: gen.save(res, output_dir)

        elif args.command == "quiz":
            gen = MedicalQuizGenerator(model_config)
            for item in tqdm(handle_batch_input(args.topic, "quiz"), desc="Quiz"):
                res = gen.generate_text(topic=item, difficulty=args.difficulty, num_questions=args.num_questions, num_options=args.num_options, structured=True)
                if res: gen.save(res, output_dir)

        elif args.command == "refer":
            gen = MedReferral(model_config)
            for item in tqdm(handle_batch_input(args.question, "refer"), desc="Refer"):
                res = gen.generate_text(item)
                if res:
                    fname = "".join([c if c.isalnum() else "_" for c in item.lower()])[:50]
                    with open(output_dir / f"{fname}.md", 'w') as f: f.write(res)

        elif args.command == "roles":
            gen = MedSpecialityRoles(model_config)
            for item in tqdm(handle_batch_input(args.speciality, "roles"), desc="Roles"):
                res = gen.generate_text(item)
                if res:
                    fname = "".join([c if c.isalnum() else "_" for c in item.lower()])[:50]
                    with open(output_dir / f"{fname}.md", 'w') as f: f.write(res)

        elif args.command == "topic":
            gen = MedicalTopicGenerator(model_config)
            for item in tqdm(handle_batch_input(args.topic, "topic"), desc="Topic"):
                res = gen.generate_text(topic=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "organ":
            gen = OrganDiseaseGenerator(model_config)
            for item in tqdm(handle_batch_input(args.organ, "organ"), desc="Organ"):
                res = gen.generate_text(organ=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "surgery":
            gen = SurgeryInfoGenerator(model_config)
            for item in tqdm(handle_batch_input(args.surgery, "surgery"), desc="Surgery"):
                res = gen.generate_text(surgery=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "pose":
            if args.list:
                from surgical_pose_info.surgical_pose_info import COMMON_SURGICAL_POSITIONS
                for p in COMMON_SURGICAL_POSITIONS: print(f"- {p}")
            elif args.pose:
                gen = SurgicalPoseInfoGenerator(model_config)
                for item in tqdm(handle_batch_input(args.pose, "pose"), desc="Pose"):
                    res = gen.generate_text(pose=item, structured=args.structured)
                    if res: gen.save(res, output_dir)

        elif args.command == "tool":
            gen = SurgicalToolInfoGenerator(model_config)
            for item in tqdm(handle_batch_input(args.tool, "tool"), desc="Tool"):
                res = gen.generate_text(tool=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "tray":
            gen = SurgicalTrayGenerator(model_config)
            for item in tqdm(handle_batch_input(args.surgery, "tray"), desc="Tray"):
                res = gen.generate_text(surgery=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "case":
            gen = SyntheticCaseReportGenerator(model_config)
            for item in tqdm(handle_batch_input(args.condition, "case"), desc="Case"):
                res = gen.generate_text(condition=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "ethics":
            gen = MedEthicalQA(model_config)
            for item in tqdm(handle_batch_input(args.question, "ethics"), desc="Ethics"):
                res = gen.generate_text(question=item, structured=args.structured)
                if res: gen.save(res, output_dir)

        elif args.command == "flashcard":
            extractor = MedicalLabelExtractor(model_config)
            explainer = MedicalTermExplainer(model_config)
            
            input_path = Path(args.image)
            is_image = input_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']
            
            if is_image:
                terms = extractor.extract_terms(str(input_path))
                if not terms:
                    print(f"No medical terms found in {args.image}")
                else:
                    for term in tqdm(terms, desc="Explaining Labels"):
                        res = explainer.explain_label(term, structured=args.structured)
                        if res: explainer.save(res, output_dir, term=term)
            else:
                # Treat as a direct term
                res = explainer.explain_label(args.image, structured=args.structured)
                if res: explainer.save(res, output_dir, term=args.image)

        elif args.command == "history":
            gen = PatientMedicalHistoryGenerator(model_config)
            input_data = MedicalHistoryInput(exam=args.exam, age=args.age, gender=args.gender, purpose=args.purpose)
            res = gen.generate_text(input_data, structured=args.structured)
            if res: gen.save(res, output_dir)

    except Exception as e:
        logger.error(f"Error in command {args.command}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
