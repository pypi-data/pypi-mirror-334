from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class TaxCardSchema(BaseModel):
    """
    Schema for tax card data from Visma Lon HR.
    Represents tax card information from the VISMALØN table SKATTEKORT.
    """
    
    TaxCardRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Customer ID")
    EmployerID: str = Field(..., description="Employer number")
    EmployeeID: str = Field(..., description="Employee number")
    TaxCardType: str = Field(..., description="Type of tax card ex. hovedkort (main) or bikort (secondary)")
    StartDate: datetime = Field(..., description="Valid from")
    EndDate: Optional[datetime] = Field(None, description="Valid to")
    TaxFreeAmount: Optional[str] = Field(None, description="Tax free amount")
    IncomeTaxRate: Optional[str] = Field(None, description="Tax rate")
    DeductionPrDay: Optional[str] = Field(None, description="Daily deduction")
    DeductionPrWeek: Optional[str] = Field(None, description="Weekly deduction")
    DeductionPr14Day: Optional[str] = Field(None, description="Bi weekly deduction")
    DeductionPrMonth: Optional[str] = Field(None, description="Monthly deduction")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    AdditionalIncomeTaxRate: Optional[str] = Field(None, description="Extra additional tax rate")
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