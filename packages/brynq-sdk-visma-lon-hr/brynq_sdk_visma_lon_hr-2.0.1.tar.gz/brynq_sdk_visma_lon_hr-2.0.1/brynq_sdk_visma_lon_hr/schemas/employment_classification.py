from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class EmploymentClassificationSchema(BaseModel):
    """
    Schema for employment classification data from Visma Lon HR.
    Represents employment classification information from the VISMALØN table ANSOPLYSNING.
    """
    
    EmploymentClassificationRID: str = Field(..., description="Unique key for use of OData")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    CustomerID: str = Field(..., description="Customer ID")
    EmployerID: str = Field(..., description="Employer number")
    EmployeeID: str = Field(..., description="Employee number")
    EmploymentID: str = Field(..., description="Employment")
    StartDate: datetime = Field(..., description="Start date")
    EndDate: Optional[datetime] = Field(None, description="End date")
    ContentTypeCode: str = Field(..., description="Ex. 100, 200, 350, 400, 600, 610, 620, 700, 800 etc.")
    ClassificationCode: str = Field(..., description="Ex. 6 digit Disco-08 code for IP_type 350")
    Value: Optional[str] = Field(None, description="For IP_Type 600, 610, og 620 the normtime, holidays or holiday supplement is shown")
    CreateTime: datetime = Field(..., description="Timestamp for creating the registration")
    UpdateTime: datetime = Field(..., description="Timestamp for latest update of the registration")
    
    @field_validator('StartDate', 'EndDate', 'CreateTime', 'UpdateTime', mode='before')
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