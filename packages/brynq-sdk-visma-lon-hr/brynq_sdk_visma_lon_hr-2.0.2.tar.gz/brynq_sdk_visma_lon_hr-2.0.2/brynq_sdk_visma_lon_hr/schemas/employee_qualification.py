from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class EmployeeQualificationSchema(BaseModel):
    """
    Schema for employee qualification data from Visma Lon HR.
    Represents course and education information for employees from the Visma HR table EmployeeQualification.
    """
    
    EmployeeQualificationRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Organisation")
    EmployerID: str = Field(..., description="Employer number")
    EmployeeID: str = Field(..., description="Employee number")
    CourseID: str = Field(..., description="Course ID")
    CourseCalendarID: Optional[str] = Field(None, description="Calendar for course")
    CourseStateCode: Optional[str] = Field(None, description="Status")
    Text: Optional[str] = Field(None, description="Name of course")
    CourseStartDate: Optional[datetime] = Field(None, description="Course start date")
    CoursePrice: Optional[str] = Field(None, description="Price")
    Duration: Optional[str] = Field(None, description="Duration")
    DurationIsDefaultValue: Optional[str] = Field(None, description="Absence text")
    DurationTypeCode: Optional[str] = Field(None, description="Units for duration")
    Grade: Optional[str] = Field(None, description="Grade/Level")
    DeadlineDate: Optional[datetime] = Field(None, description="Obsolescence/expiration date")
    Description: Optional[str] = Field(None, description="Remark")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    CreateTime: datetime = Field(..., description="Timestamp for creating the registration")
    UpdateTime: datetime = Field(..., description="Timestamp for latest update of the registration")
    
    @field_validator('CourseStartDate', 'DeadlineDate', 'CreateTime', 'UpdateTime', mode='before')
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