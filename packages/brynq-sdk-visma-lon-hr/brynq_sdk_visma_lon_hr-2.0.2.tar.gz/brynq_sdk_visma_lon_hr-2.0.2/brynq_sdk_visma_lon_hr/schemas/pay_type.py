from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class PayTypeSchema(BaseModel):
    """
    Schema for pay type data from Visma Lon HR.
    Represents wage type information from the VISMALØN table LOENART.
    """
    
    PayTypeRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Customer ID")
    StartDate: datetime = Field(..., description="Start date")
    EndDate: Optional[datetime] = Field(None, description="End date")
    Name: str = Field(..., description="Name of Wage type")
    BenefitDeduction: Optional[str] = Field(None, description="Benefit deduction")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    PayTypeCode: str = Field(..., description="Number of Wage type")
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