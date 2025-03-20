from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class VismaLoenWorkCalendarSchema(BaseModel):
    """
    Schema for work calendar data from Visma Lon HR.
    Represents work calendar information from the VISMALØN table ARBEJDSTIDSKALENDER.
    """
    
    VismaLoenWorkCalendarRID: str = Field(..., description="Unique key for use of OData")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    CustomerID: str = Field(..., description="Customer ID")
    EmployerID: str = Field(..., description="Employer number")
    EmployeeID: str = Field(..., description="Employee number")
    EmploymentID: str = Field(..., description="Employment")
    StartDate: datetime = Field(..., description="Start date")
    EndDate: Optional[datetime] = Field(None, description="End date")
    ICAL: Optional[str] = Field(None, description="Calendar in the format ICAL")
    WorkingHoursType: Optional[str] = Field(None, description="Working hour type")
    IgnoreHolidays: Optional[str] = Field(None, description="Ignore holidays")
    IncludeSaturdays: Optional[str] = Field(None, description="Include Saturdays")
    IncludeSundays: Optional[str] = Field(None, description="Include Sundays")
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