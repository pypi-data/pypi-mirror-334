from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class ProcessedAbsenceSchema(BaseModel):
    """
    Schema for processed absence data from Visma Lon HR.
    Represents processed absence information from the VISMALØN table FRAVAERSPOSTERING.
    """
    
    ProcessedAbsenceRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Customer ID")
    EmployerID: str = Field(..., description="Employer number")
    EmployeeID: str = Field(..., description="Employee number")
    EmploymentID: str = Field(..., description="Employment")
    StartDate: datetime = Field(..., description="Start date")
    EndDate: Optional[datetime] = Field(None, description="End date")
    AbsenceCode: str = Field(..., description="Absence code")
    ProcessedAbsenceName: str = Field(..., description="Name of absence")
    Rate: Optional[str] = Field(None, description="Rate that the absence is paid out by")
    Duration: Optional[str] = Field(None, description="Length of absence period either in days or hours depending on the type of absence")
    DurationType: Optional[str] = Field(None, description="Hours or days")
    UsedDate: Optional[datetime] = Field(None, description="Date of payroll processed")
    ProjectID: Optional[str] = Field(None, description="Project number")
    UsedPayrollNumber: Optional[str] = Field(None, description="Payroll number")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    GroupID: Optional[str] = Field(None, description="ID that refers to a possible registration in the table ProcessedAbsence")
    StartTime: Optional[str] = Field(None, description="Start time for the absence")
    EndTime: Optional[str] = Field(None, description="End time for the absence")
    CreateTime: datetime = Field(..., description="Timestamp for creating the registration")
    UpdateTime: datetime = Field(..., description="Timestamp for latest update of the registration")
    
    @field_validator('StartDate', 'EndDate', 'UsedDate', 'CreateTime', 'UpdateTime', mode='before')
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