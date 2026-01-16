"""
Pydantic models for medical device information structure.

This module contains all the data models used for organizing and validating
medical device information across different categories and specifications.
"""
from pydantic import BaseModel, Field
from typing import Optional


class DeviceBasicInfo(BaseModel):
    device_name: str = Field(description="Official name of the medical device")
    alternative_names: str = Field(description="Other names or acronyms for this device, comma-separated")
    device_category: str = Field(description="Category (diagnostic imaging, surgical instrument, monitoring device, etc)")
    device_classification: str = Field(description="FDA classification (Class I, II, or III) or equivalent regulatory classification")
    intended_use: str = Field(description="Official intended use as per regulatory clearance")
    medical_specialties: str = Field(description="Primary medical specialties that use this device, comma-separated")


class DevicePurposeAndApplications(BaseModel):
    primary_purpose: str = Field(description="Main clinical purpose of this device")
    diagnostic_applications: str = Field(description="Diseases or conditions this device helps diagnose, comma-separated")
    monitoring_applications: str = Field(description="Conditions this device helps monitor, comma-separated")
    therapeutic_applications: str = Field(description="Therapeutic or surgical applications, comma-separated")
    screening_applications: str = Field(description="Screening or preventive applications")


class PhysicalSpecifications(BaseModel):
    dimensions: str = Field(description="Physical dimensions and size specifications (length x width x height in cm or inches)")
    weight: str = Field(description="Device weight with unit of measurement")
    materials: str = Field(description="Materials used in construction, comma-separated")
    portability: str = Field(description="Whether device is portable, handheld, cart-based, or fixed installation")
    sterilization_capability: str = Field(description="Whether device or components can be sterilized, method required (autoclave, gas, chemical)")
    shelf_life: str = Field(description="Expiration date or shelf life if applicable")


class TechnicalSpecifications(BaseModel):
    operating_principle: str = Field(description="Scientific/physical principle on which device operates")
    technology_type: str = Field(description="Type of technology (ultrasound, radiography, endoscopy, laser, etc)")
    imaging_modality: Optional[str] = Field(description="Imaging modality for diagnostic devices (ultrasound, MRI, CT, X-ray, etc)")
    resolution: str = Field(description="Spatial or temporal resolution capabilities with specific units")
    field_of_view: str = Field(description="Field of view or coverage area for diagnostic/imaging devices")
    frequency_range: Optional[str] = Field(description="Operating frequency range if applicable (MHz for ultrasound, etc)")
    power_specifications: str = Field(description="Power requirements (volts, watts, battery type and duration)")
    data_output: str = Field(description="Types of data or images produced, comma-separated")
    connectivity: str = Field(description="Connectivity options (DICOM, USB, wireless, ethernet, proprietary)")


class SafetyAndRisks(BaseModel):
    safety_features: str = Field(description="Built-in safety mechanisms and protective features, comma-separated")
    common_adverse_events: str = Field(description="Known adverse events or complications, comma-separated")
    serious_risks: str = Field(description="Serious or life-threatening risks, comma-separated")
    contraindications: str = Field(description="Conditions or situations where device should not be used, comma-separated")
    safety_certifications: str = Field(description="Safety certifications (CE mark, FDA approval, UL, ISO standards), comma-separated")
    radiation_exposure: Optional[str] = Field(description="Radiation exposure if applicable (mSv, dose rate, cumulative limits)")
    infection_control: str = Field(description="Infection control considerations and cleaning/disinfection requirements")


class OperationalProcedures(BaseModel):
    setup_requirements: str = Field(description="Pre-use setup and calibration procedures, numbered or comma-separated")
    operation_steps: str = Field(description="Step-by-step operational procedures, numbered")
    time_required: str = Field(description="Typical time required for complete procedure")
    required_personnel: str = Field(description="Number and type of trained personnel required (operator, assistant, specialist)")
    training_requirements: str = Field(description="Minimum training and certification requirements for operators")
    troubleshooting: str = Field(description="Common problems and troubleshooting steps, comma-separated")
    shutdown_procedures: str = Field(description="Proper shutdown and storage procedures")


class MaintenanceAndCalibration(BaseModel):
    maintenance_schedule: str = Field(description="Recommended maintenance frequency (daily, weekly, monthly, annually) with specific tasks")
    calibration_frequency: str = Field(description="How often device must be calibrated with specific timeframes")
    calibration_procedure: str = Field(description="Calibration procedure and tools required")
    common_maintenance_tasks: str = Field(description="Routine maintenance tasks and supplies needed, comma-separated")
    parts_replacement: str = Field(description="Key replaceable components and their typical lifespan")
    service_availability: str = Field(description="Availability of service and technical support")
    spare_parts_common: str = Field(description="Common spare parts and their cost range")


class CleaningAndSterilization(BaseModel):
    disinfection_level_required: str = Field(description="Level of disinfection required (high-level, intermediate, low-level)")
    cleaning_procedure: str = Field(description="Approved cleaning methods and solutions")
    sterilization_methods: str = Field(description="Approved sterilization methods (steam, ethylene oxide, hydrogen peroxide, etc)")
    material_compatibility: str = Field(description="Which components can withstand which sterilization methods")
    compatibility_with_agents: str = Field(description="Chemical compatibility with disinfectants and sterilizing agents")
    drying_storage: str = Field(description="Proper drying and storage conditions")


class PatientPrepAndConsiderations(BaseModel):
    patient_preparation: str = Field(description="Required patient preparation procedures, comma-separated")
    positioning_requirements: str = Field(description="Required patient positioning or movement during procedure")
    special_precautions: str = Field(description="Special precautions for specific patient populations (pediatric, elderly, obese, pregnant)")
    comfort_measures: str = Field(description="Comfort and anxiety-reduction measures")
    anesthesia_requirements: str = Field(description="Whether local, general, or no anesthesia required")
    duration_of_procedure: str = Field(description="Typical procedure duration and patient positioning time")
    post_procedure_recovery: str = Field(description="Post-procedure recovery time and restrictions")


class DataAndResultsHandling(BaseModel):
    data_storage: str = Field(description="How data is stored (electronic, physical, cloud-based)")
    data_security: str = Field(description="Security measures and HIPAA compliance")
    result_formats: str = Field(description="Formats of results or images produced, comma-separated")
    interpretation_software: str = Field(description="Built-in interpretation or analysis software capabilities")
    export_capabilities: str = Field(description="Data export options and formats")
    archival_requirements: str = Field(description="Data retention and archival requirements")
    compatibility_with_systems: str = Field(description="Compatibility with EHR and hospital information systems")


class IndicationsAndContraindications(BaseModel):
    appropriate_indications: str = Field(description="Clinical situations when device use is appropriate, comma-separated")
    relative_contraindications: str = Field(description="Conditions where device may be used with caution, comma-separated")
    absolute_contraindications: str = Field(description="Conditions where device absolutely should not be used, comma-separated")
    special_populations: str = Field(description="Special considerations for children, elderly, pregnant women, renal/hepatic impairment")


class PerformanceCharacteristics(BaseModel):
    sensitivity: str = Field(description="Ability to correctly identify positive cases with percentage")
    specificity: str = Field(description="Ability to correctly identify negative cases with percentage")
    accuracy: str = Field(description="Overall accuracy rate with percentage")
    positive_predictive_value: Optional[str] = Field(description="Probability that positive result is true positive")
    negative_predictive_value: Optional[str] = Field(description="Probability that negative result is true negative")
    inter_rater_reliability: str = Field(description="Consistency between different operators or measurements")
    intra_rater_reliability: str = Field(description="Consistency of measurements by same operator over time")


class ComparisonWithAlternatives(BaseModel):
    alternative_devices: str = Field(description="Alternative devices that serve similar purpose, comma-separated")
    advantages: str = Field(description="Advantages compared to alternatives, comma-separated")
    disadvantages: str = Field(description="Disadvantages compared to alternatives, comma-separated")
    cost_comparison: str = Field(description="Cost comparison with alternative devices")
    when_alternative_preferred: str = Field(description="Clinical scenarios where alternatives are better, comma-separated")


class CostAndReimbursement(BaseModel):
    device_cost_range: str = Field(description="Typical device purchase or lease cost range")
    installation_costs: str = Field(description="Installation, setup, and infrastructure costs")
    maintenance_costs_annual: str = Field(description="Annual maintenance and support costs")
    procedure_cost_to_patient: str = Field(description="Typical patient cost or facility fee")
    insurance_coverage: str = Field(description="Typical insurance coverage and reimbursement rates")
    cpt_codes: Optional[str] = Field(description="Relevant CPT codes for billing and reimbursement")
    financial_assistance: str = Field(description="Availability of financial assistance or payment plans")


class RegulatoryAndCertification(BaseModel):
    fda_clearance: str = Field(description="FDA clearance status, 510(k) number, or breakthrough status")
    ce_marking: str = Field(description="CE marking status and applicable European directives")
    iso_standards: str = Field(description="Applicable ISO standards and certifications, comma-separated")
    clinical_evidence: str = Field(description="Level of clinical evidence supporting device effectiveness")
    recalls_or_alerts: str = Field(description="Any FDA recalls or safety alerts on record")
    post_market_surveillance: str = Field(description="Post-market surveillance requirements or data collection")


class ManufacturerAndSupport(BaseModel):
    manufacturer_name: str = Field(description="Device manufacturer name")
    manufacturer_contact: str = Field(description="Manufacturer contact information (phone, website, support email)")
    support_availability: str = Field(description="24/7, business hours, regional support availability")
    training_resources: str = Field(description="Available training resources (courses, certifications, manuals)")
    user_manuals_available: str = Field(description="Availability and languages of user documentation")


class SpecialConsiderations(BaseModel):
    pediatric_use: str = Field(description="Specific considerations and adaptations for pediatric use")
    geriatric_use: str = Field(description="Specific considerations for elderly patients")
    pregnancy_safety: str = Field(description="Safety considerations for pregnant women (especially for imaging/radiation devices)")
    allergic_reactions: str = Field(description="Potential allergic reactions to device materials or contrast agents if used")
    renal_hepatic_considerations: str = Field(description="Considerations for patients with renal or hepatic impairment")


class TrendsDevelopments(BaseModel):
    recent_improvements: str = Field(description="Recent technological improvements in this device category")
    emerging_technologies: str = Field(description="Emerging technologies that may replace this device")
    future_versions: str = Field(description="Known future versions or developments")
    artificial_intelligence: str = Field(description="AI/ML capabilities for analysis and interpretation")


class MedicalDeviceInfo(BaseModel):
    # Basic Information
    basic_info: DeviceBasicInfo

    # Purpose and Applications
    purpose_and_applications: DevicePurposeAndApplications

    # Physical and Technical Specifications
    physical_specifications: PhysicalSpecifications
    technical_specifications: TechnicalSpecifications

    # Safety and Risk Management
    safety_and_risks: SafetyAndRisks

    # Operation and Use
    operational_procedures: OperationalProcedures
    maintenance_and_calibration: MaintenanceAndCalibration
    cleaning_and_sterilization: CleaningAndSterilization

    # Patient-Related Information
    patient_prep_and_considerations: PatientPrepAndConsiderations
    indications_and_contraindications: IndicationsAndContraindications
    special_considerations: SpecialConsiderations

    # Data and Results
    data_and_results_handling: DataAndResultsHandling

    # Performance
    performance_characteristics: PerformanceCharacteristics

    # Comparison and Alternatives
    comparison_with_alternatives: ComparisonWithAlternatives

    # Practical Information
    cost_and_reimbursement: CostAndReimbursement

    # Regulatory and Compliance
    regulatory_and_certification: RegulatoryAndCertification
    manufacturer_and_support: ManufacturerAndSupport

    # Additional Information
    trends_developments: TrendsDevelopments

    # Educational Content
    plain_language_explanation: str = Field(description="Simple explanation of how device works for patients")
    key_takeaways: str = Field(description="3-5 most important points about this device, comma-separated")
    common_misconceptions: str = Field(description="Common myths or misunderstandings about this device, comma-separated")
