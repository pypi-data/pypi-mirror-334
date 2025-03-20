from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class PayrollSchema(BaseModel):
    """
    Schema for payroll data from Visma Lon HR.
    Represents payroll information from the VISMALØN table KOERSELSSELEKTION.
    """
    
    PayrollRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Customer ID")
    PayrollRunNumber: str = Field(..., description="Payroll run number")
    SelectionNumber: str = Field(..., description="Selection number")
    PayPeriodStart: datetime = Field(..., description="Payroll period start")
    PayPeriodEnd: datetime = Field(..., description="Payroll period end")
    Name: str = Field(..., description="Payroll name")
    AccountingDate: Optional[datetime] = Field(None, description="Accounting date")
    AvailabilityDate: Optional[datetime] = Field(None, description="Availability date")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    PayrollUsedDate: Optional[datetime] = Field(None, description="Payroll used date")
    CreateTime: datetime = Field(..., description="Timestamp for creating the registration")
    UpdateTime: datetime = Field(..., description="Timestamp for latest update of the registration")
    
    @field_validator('PayPeriodStart', 'PayPeriodEnd', 'AccountingDate', 'AvailabilityDate', 
                    'PayrollUsedDate', 'CreateTime', 'UpdateTime', mode='before')
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