from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class CustomerSchema(BaseModel):
    """Schema for customer data from Visma Lon HR"""
    
    CustomerRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Customer ID")
    ParentCustomerID: Optional[str] = Field(None, description="Parent customer ID")
    Name: str = Field(..., description="Name of employer")
    AddressLine1: Optional[str] = Field(None, description="Address for employer")
    AddressLine2: Optional[str] = Field(None, description="Supplementary address information")
    PostalCodeDK: Optional[str] = Field(None, description="Postal code for employer")
    PostalDistrictDK: Optional[str] = Field(None, description="City name for employer")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
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
