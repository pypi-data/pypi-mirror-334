from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class AbsenceTypeSchema(BaseModel):
    """
    Schema for absence type data from Visma Lon HR.
    """
    
    AbsenceTypeRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Customer ID")
    AbsenceTypeCode: str = Field(..., description="Absence type code")
    Name: str = Field(..., description="Name of absence type")
    AbsenceGroup: Optional[str] = Field(None, description="Absence group")
    ILType: Optional[str] = Field(None, description="IL type")
    StartDate: datetime = Field(..., description="Start date")
    EndDate: datetime = Field(..., description="End date")
    FromDate: Optional[datetime] = Field(None, description="From date")
    ToDate: Optional[datetime] = Field(None, description="To date")
    VersionNumber: str = Field(..., description="Version number")
    CreateTime: datetime = Field(..., description="Creation timestamp")
    UpdateTime: datetime = Field(..., description="Update timestamp")
    
    # Bu alanlar API'dan gelmiyor ancak şemada zorunlu olarak görünüyor
    # Bu nedenle isteğe bağlı yapalım ve alias kullanalım
    AbsenceTypeID: Optional[str] = Field(None, alias="AbsenceTypeCode", description="Absence type ID")
    EmployerID: Optional[str] = Field(None, description="Employer ID")
    ModifyTime: Optional[datetime] = Field(None, alias="UpdateTime", description="Modification timestamp")
    
    @field_validator('StartDate', 'EndDate', 'FromDate', 'ToDate', 'CreateTime', 'UpdateTime', 'ModifyTime', mode='before')
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
