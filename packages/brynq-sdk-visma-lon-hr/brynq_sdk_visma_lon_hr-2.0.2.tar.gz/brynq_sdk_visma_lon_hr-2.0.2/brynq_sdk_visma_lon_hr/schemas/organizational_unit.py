from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class OrganizationalUnitSchema(BaseModel):
    """
    Schema for organizational unit data from Visma Lon HR.
    Represents organizational unit information from Visma Løn or Visma HR.
    """
    
    OrganizationalUnitRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Customer ID")
    EmployerID: str = Field(..., description="Employer number")
    OrganizationID: str = Field(..., description="Organisation ID")
    StartDate: datetime = Field(..., description="Start date")
    EndDate: Optional[datetime] = Field(None, description="End date")
    Name: str = Field(..., description="Name of organisational unit")
    AddressLine1: Optional[str] = Field(None, description="Address line 1")
    AddressLine2: Optional[str] = Field(None, description="Address line 2")
    PostalCode: Optional[str] = Field(None, description="Postal code")
    PostalDistrict: Optional[str] = Field(None, description="City name")
    CountryCode: Optional[str] = Field(None, description="Country code for tax registration")
    Country: Optional[str] = Field(None, description="Country name")
    ResponsibleEmployeeId: Optional[str] = Field(None, description="Department manager")
    OrganizationalUnitID: str = Field(..., description="Department ID")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    ParentOrganizationalUnitID: Optional[str] = Field(None, description="Identification of parent organisation unit (if any)")
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