from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class CourseCalendarSchema(BaseModel):
    """
    Schema for course calendar data from Visma Lon HR.
    Represents course calendar information from the Visma HR table CourseCalendar.
    """
    
    CourseCalendarRID: str = Field(..., description="Unique key for use of OData")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    CustomerID: str = Field(..., description="Organisation")
    CourseID: str = Field(..., description="Key to the specific course")
    StartDate: datetime = Field(..., description="Start date")
    CourseCalendarID: str = Field(..., description="Course calendar")
    EndDate: Optional[datetime] = Field(None, description="End date")
    MaxParticipants: Optional[str] = Field(None, description="Max number of participants")
    Note: Optional[str] = Field(None, description="Note")
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