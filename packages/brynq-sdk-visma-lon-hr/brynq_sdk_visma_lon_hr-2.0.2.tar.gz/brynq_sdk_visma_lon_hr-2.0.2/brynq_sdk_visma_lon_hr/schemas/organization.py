from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class OrganizationSchema(BaseModel):
    """
    Schema for organization data from Visma Lon HR.
    Represents organization information from the VISMALØN table ARBEJDSGIVER or Visma HR table Company.
    """
    
    OrganizationRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Customer ID")
    OrganizationID: str = Field(..., description="Organisation")
    StartDate: datetime = Field(..., description="Start date")
    EndDate: Optional[datetime] = Field(None, description="End date")
    FromDate: Optional[datetime] = Field(None, description="From date")
    ToDate: Optional[datetime] = Field(None, description="To date")
    Name: str = Field(..., description="Name")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    ParentOrganizationId: Optional[str] = Field(None, description="Parent Company")
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