"""
medical_device_models.py - Data Models for Medical Device Identification

This module contains Pydantic models used for identifying if a medical device
is well-known in the healthcare field and providing basic information about it.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class MedicalDeviceIdentificationModel(BaseModel):
    """Structured information about a medical device's recognition."""
    device_name: str = Field(description="The name of the medical device being identified")
    is_well_known: bool = Field(description="Whether the device is widely recognized in healthcare")
    device_category: str = Field(description="The category of device (e.g., implantable, diagnostic, surgical, wearable)")
    primary_function: str = Field(description="What the device is primarily used for")
    clinical_significance: str = Field(description="Explanation of its importance in patient care or medical procedures")


class MedicalDeviceIdentifierModel(BaseModel):
    """
    Comprehensive medical device identification result.
    """
    identification: Optional[MedicalDeviceIdentificationModel] = Field(
        default=None,
        description="Detailed identification information"
    )
    summary: str = Field(description="A concise summary of the device's status in healthcare")
    data_available: bool = Field(description="Whether information about this device was found")


class ModelOutput(BaseModel):
    data: Optional[MedicalDeviceIdentifierModel] = None
    markdown: Optional[str] = None
