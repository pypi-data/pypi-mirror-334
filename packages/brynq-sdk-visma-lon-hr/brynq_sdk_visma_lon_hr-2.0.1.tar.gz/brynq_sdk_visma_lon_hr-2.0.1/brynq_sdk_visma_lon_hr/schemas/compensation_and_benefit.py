from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class CompensationAndBenefitSchema(BaseModel):
    """
    Schema for compensation and benefit data from Visma Lon HR.
    Represents wage types that will be a part of a future payroll from ANSLOENOPLYSNING and ANSLOENOPLPARAM tables.
    """
    
    CompensationAndBenefitRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Customer ID")
    EmployerID: str = Field(..., description="Employer number")
    EmployeeID: str = Field(..., description="Employee number")
    EmploymentID: str = Field(..., description="Employment ID")
    StartDate: datetime = Field(..., description="Start date")
    EndDate: datetime = Field(..., description="End date")
    PayTypeCode: str = Field(..., description="Wage type number")
    CompensationAndBenefitName: Optional[str] = Field(None, description="Text that describes the wage type")
    PayTypeType: Optional[str] = Field(None, description="Type of wage type")
    Frequency: Optional[str] = Field(None, description="Frequency")
    UseAfter: Optional[str] = Field(None, description="To be paid out after a specific date")
    Units: Optional[str] = Field(None, description="Units, number of units to be paid out")
    Rate: Optional[str] = Field(None, description="The rate to calculate the payout")
    Amount: Optional[str] = Field(None, description="The amount to pay out")
    PensionOwnPercent: Optional[str] = Field(None, description="Pension own percentage")
    DoNotReduce: Optional[str] = Field(None, description="If the amount on the wage type is to be reduced if the employee is on paid leave")
    PensionCompanyAmount: Optional[str] = Field(None, description="Pension company amount")
    PensionCompanyPercent: Optional[str] = Field(None, description="Pension company percent")
    PensionBasis: Optional[str] = Field(None, description="Basis to calculate the pension")
    Balance: Optional[str] = Field(None, description="Balance")
    Year: Optional[str] = Field(None, description="Year")
    InputValue: Optional[str] = Field(None, description="Input value")
    RegistrationNumber: Optional[str] = Field(None, description="Registration number")
    AccountNumber: Optional[str] = Field(None, description="Account number")
    SettlingType: Optional[str] = Field(None, description="Transaction code for pension company")
    ApproveItemStatus: Optional[str] = Field(None, description="Status for approval")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    Historik: Optional[datetime] = Field(None, description="Timestamp for creating the registration")
    Used: Optional[str] = Field(None, description="Used")
    SettlementMethod: Optional[str] = Field(None, description="Method of settlement")
    SettlementType: Optional[str] = Field(None, description="Number for settlement type")
    DisapprovalComment: Optional[str] = Field(None, description="Comment for rejection")
    ChangeReasonCode: Optional[str] = Field(None, description="Code for change reason")
    Comment: Optional[str] = Field(None, description="Comment")
    
    @field_validator('StartDate', 'EndDate', 'Historik', mode='before')
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