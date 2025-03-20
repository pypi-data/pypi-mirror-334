from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class PhoneNumberSchema(BaseModel):
    """
    Schema for phone number data from Visma Lon HR.
    Represents phone number information from the VISMALØN table TELEFON.
    """
    
    PhoneNumberRID: str = Field(..., description="Unique key for use of OData")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    CustomerID: str = Field(..., description="Customer ID")
    EmployerID: str = Field(..., description="Employer number")
    EmployeeID: str = Field(..., description="Employee number")
    EmploymentID: str = Field(..., description="Employment")
    PhoneNumber1: Optional[str] = Field(None, description="Phone number")
    ExtentionNumber: Optional[str] = Field(None, description="Extension number")
    Comment: Optional[str] = Field(None, description="Text")
    CreateTime: datetime = Field(..., description="Timestamp for creating the registration")
    UpdateTime: datetime = Field(..., description="Timestamp for latest update of the registration")
    
    @field_validator('CreateTime', 'UpdateTime', mode='before')
    @classmethod
    def parse_datetime(cls, v: Optional[str]) -> Optional[datetime]:
        """Parse datetime fields from string"""
        if not v:
            return None
        try:
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return None
    
    class Config:
        from_attributes = True
        populate_by_name = True 