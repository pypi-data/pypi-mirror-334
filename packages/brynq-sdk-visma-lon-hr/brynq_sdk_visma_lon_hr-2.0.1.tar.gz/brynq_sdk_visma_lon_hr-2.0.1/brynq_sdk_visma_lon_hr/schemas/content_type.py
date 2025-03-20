from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class ContentTypeSchema(BaseModel):
    """
    Schema for content type data from Visma Lon HR.
    Represents content type information from the VISMALØN table INDHOLDSTYPE.
    """
    
    ContentTypeRID: str = Field(..., description="Unique key for use of OData")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    CustomerID: str = Field(..., description="Customer ID")
    ContentTypeCode: str = Field(..., description="Ex. 100, 200, 350, 400, 600, 610, 620, 700, 800 etc.")
    StartDate: datetime = Field(..., description="Start date")
    EndDate: Optional[datetime] = Field(None, description="End date")
    FromDate: Optional[datetime] = Field(None, description="Period From date")
    ToDate: Optional[datetime] = Field(None, description="Period To date")
    ContentTypeName: str = Field(..., description="Description of personal information")
    Reciever: Optional[str] = Field(None, description="Receiver of statistics ex. DA, DS, FA")
    CreateTime: datetime = Field(..., description="Timestamp for creating the registration")
    UpdateTime: datetime = Field(..., description="Timestamp for latest update of the registration")
    
    @field_validator('StartDate', 'EndDate', 'FromDate', 'ToDate', 'CreateTime', 'UpdateTime', mode='before')
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