from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class CourseSupplierSchema(BaseModel):
    """
    Schema for course supplier data from Visma Lon HR.
    Represents course supplier information from the Visma HR table CourseSupplier.
    """
    
    CourseSupplierRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Organisation")
    CourseSupplierID: str = Field(..., description="Supplier number")
    CourseSupplierName: str = Field(..., description="Supplier name")
    Adress: Optional[str] = Field(None, description="Address")
    Contact: Optional[str] = Field(None, description="Contact person")
    AddressWeb: Optional[str] = Field(None, description="Website address")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    CreateTime: datetime = Field(..., description="Timestamp for creating the registration")
    UpdateTime: datetime = Field(..., description="Timestamp for latest update of the registration")
    
    @field_validator('CreateTime', 'UpdateTime', mode='before')
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