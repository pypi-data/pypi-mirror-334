from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class EmployerSchema(BaseModel):
    """
    Schema for employer data from Visma Lon HR.
    Represents employer information from the VISMALØN table ARBEJDSGIVER.
    """
    
    EmployerRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Customer ID")
    EmployerID: str = Field(..., description="Employer number")
    StartDate: datetime = Field(..., description="Employer start date")
    EndDate: Optional[datetime] = Field(None, description="End date for closing down the employer")
    FromDate: Optional[datetime] = Field(None, description="Active start date")
    ToDate: Optional[datetime] = Field(None, description="Active end date")
    CVRNumber: Optional[str] = Field(None, description="CVR number")
    Name: str = Field(..., description="Name of employer")
    AddressLine1: Optional[str] = Field(None, description="Employer address")
    AddressLine2: Optional[str] = Field(None, description="Supplementary address information")
    PostalCodeDK: Optional[str] = Field(None, description="Employer postal code")
    PostalDistrictDK: Optional[str] = Field(None, description="Employer city name")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    CreateTime: datetime = Field(..., description="Timestamp for creating the registration")
    UpdateTime: datetime = Field(..., description="Timestamp for latest update of the registration")
    
    @field_validator('StartDate', 'EndDate', 'FromDate', 'ToDate', 'CreateTime', 'UpdateTime', mode='before')
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
