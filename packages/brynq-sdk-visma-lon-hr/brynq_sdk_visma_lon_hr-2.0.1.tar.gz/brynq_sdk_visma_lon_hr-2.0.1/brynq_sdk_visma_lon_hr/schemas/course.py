from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class CourseSchema(BaseModel):
    """
    Schema for course data from Visma Lon HR.
    Represents course information from the Visma HR table Course.
    """
    
    CourseRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Organisation")
    CourseId: str = Field(..., alias="CourseID", description="Course ID")
    CourseName: str = Field(..., description="Name of course")
    StartDate: datetime = Field(..., description="Valid from")
    EndDate: datetime = Field(..., description="Valid to")
    CourseTypeCode: Optional[str] = Field(None, description="Type of course")
    Instructor: Optional[str] = Field(None, description="Instructor")
    PhoneNumber: Optional[str] = Field(None, description="Phone number")
    CoursePrice: Optional[str] = Field(None, description="Price")
    Duration: Optional[str] = Field(None, description="Duration")
    DurationType: Optional[str] = Field(None, description="Hours or days")
    Description: Optional[str] = Field(None, description="Description")
    CourseSupplierID: Optional[str] = Field(None, description="Supplier number")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
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