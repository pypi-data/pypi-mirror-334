from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, Field

class AbsenceSchema(BaseModel):
    """Schema for absence data from Visma Lon HR"""
    
    AbsenceCode: str = Field(..., description="Code identifying the type of absence")
    AbsenceName: str = Field(..., description="Name of the absence type")
    AbsenceRID: str = Field(..., description="Resource identifier for the absence")
    ApproveItemStatus: str = Field(..., description="Status of approval for the absence")
    CreateTime: datetime = Field(..., description="Time when the record was created")
    CustomerID: str = Field(..., description="Customer ID associated with this absence")
    Duration: str = Field(..., description="Duration of the absence")
    DurationType: str = Field(..., description="Type of duration measurement")
    EmployeeID: str = Field(..., description="Employee ID for whom the absence is recorded")
    EmployerID: str = Field(..., description="Employer ID associated with this absence")
    EmploymentID: str = Field(..., description="Employment ID associated with this absence")
    EndDate: datetime = Field(..., description="End date of the absence period")
    EndTime: Optional[time] = Field(None, description="End time of the absence on the end date")
    GroupID: Optional[str] = Field(None, description="Group identifier for the absence")
    ProjectID: Optional[str] = Field(None, description="Project identifier if applicable")
    Rate: Optional[str] = Field(None, description="Rate associated with the absence")
    StartDate: datetime = Field(..., description="Start date of the absence period")
    StartTime: Optional[time] = Field(None, description="Start time of the absence on the start date")
    UpdateTime: datetime = Field(..., description="Last update time of the record")
    VersionNumber: str = Field(..., description="Version number of the record")
