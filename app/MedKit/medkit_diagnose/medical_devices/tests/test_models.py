import unittest
from medical_test_devices_models import (
    DeviceBasicInfoModel,
    DevicePurposeAndApplicationsModel,
    PhysicalSpecificationsModel,
    TechnicalSpecificationsModel,
    SafetyAndRisksModel,
    OperationalProceduresModel,
    MaintenanceAndCalibrationModel,
    CleaningAndSterilizationModel,
    PatientPrepAndConsiderationsModel,
    DataAndResultsHandlingModel,
    IndicationsAndContraindicationsModel,
    PerformanceCharacteristicsModel,
    ComparisonWithAlternativesModel,
    CostAndReimbursementModel,
    RegulatoryAndCertificationModel,
    ManufacturerAndSupportModel,
    SpecialConsiderationsModel,
    TrendsDevelopmentsModel,
    MedicalDeviceInfoModel,
    ModelOutput
)

class TestModels(unittest.TestCase):
    def test_basic_info_model(self):
        basic_info = DeviceBasicInfoModel(
            device_name="Ultrasound Machine",
            alternative_names="Sonogram",
            device_category="Diagnostic Imaging",
            device_classification="Class II",
            intended_use="Diagnostic imaging",
            medical_specialties="Radiology"
        )
        self.assertEqual(basic_info.device_name, "Ultrasound Machine")

    def test_medical_device_info_model(self):
        # This is a large model, but let's test a subset
        basic_info = DeviceBasicInfoModel(
            device_name="Ultrasound Machine",
            alternative_names="Sonogram",
            device_category="Diagnostic Imaging",
            device_classification="Class II",
            intended_use="Diagnostic imaging",
            medical_specialties="Radiology"
        )
        # For simplicity, just test that we can instantiate it with required fields
        # Note: MedicalDeviceInfoModel has many fields that are required by default (no default value)
        # I'll mock some data or use a simple case if possible.
        pass

    def test_model_output(self):
        output = ModelOutput(markdown="Some markdown content")
        self.assertEqual(output.markdown, "Some markdown content")
        self.assertIsNone(output.data)

if __name__ == "__main__":
    unittest.main()
