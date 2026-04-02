import logging

from lite.config import ModelConfig
from .med_speciality_roles_agents import SpecialityAgent, ComplianceAgent, OutputAgent
from .med_speciality_roles_models import ModelOutput, MedicalSpecialityRolesModel

logger = logging.getLogger(__name__)


class MedSpecialityRoles:
    """
    A class for determining the roles and responsibilities of a medical specialist.
    Using a 3-tier multi-agent approach.
    """

    def __init__(self, config: ModelConfig):
        self.config = config
        self.speciality_agent = SpecialityAgent(config)
        self.compliance_agent = ComplianceAgent(config)
        self.output_agent = OutputAgent(config)

    def generate_text(self, speciality: str, structured: bool = False) -> ModelOutput:
        """
        Generates comprehensive specialist roles info using a 3-tier agent system.
        """
        if not speciality or not speciality.strip():
            raise ValueError("Speciality name cannot be empty")

        logger.info(f"Starting 3-tier specialist roles generation for: {speciality}")

        try:
            # 1. Run Specialist agent
            logger.debug("Running Specialist agent...")
            spec_res = self.speciality_agent.run(speciality, structured)
            
            if structured:
                spec_content = spec_res.data.model_dump_json(indent=2)
                roles_info = spec_res.data
            else:
                spec_content = spec_res.markdown
                roles_info = None

            # 2. Compliance Audit Stage (JSON/Audit)
            logger.debug("Running ComplianceAgent audit...")
            compliance_res = self.compliance_agent.run(
                speciality, spec_content, structured
            )
            
            comp_content = (
                compliance_res.data.model_dump_json(indent=2)
                if structured and compliance_res.data
                else str(compliance_res.markdown)
            )

            # 3. Final Synthesis Stage (Markdown/Refinement)
            logger.debug("Running OutputAgent final synthesis...")
            final_markdown = self.output_agent.run(
                speciality, spec_content, comp_content
            )

            # Aggregate data
            aggregated_data = None
            if structured:
                aggregated_data = MedicalSpecialityRolesModel(
                    speciality_name=speciality,
                    roles_info=roles_info,
                    compliance_review=compliance_res.data
                )

            return ModelOutput(markdown=final_markdown, data=aggregated_data)

        except Exception as e:
            logger.error(f"✗ 3-tier generation failed: {e}")
            raise
