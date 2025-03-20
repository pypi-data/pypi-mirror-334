from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class EmployeeSchema(BaseModel):
    """Schema for employee data from Visma Lon HR"""
    
    EmployeeRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Customer ID")
    EmployerID: str = Field(..., description="Employer number")
    EmployeeID: str = Field(..., description="Employee number")
    FirstName: Optional[str] = Field(None, description="First name of employee")
    LastName: Optional[str] = Field(None, description="Last name of employee")
    AddressLine1: Optional[str] = Field(None, description="Employee address")
    AddressLine2: Optional[str] = Field(None, description="Supplementary address information for employee")
    PostalCodeDK: Optional[str] = Field(None, description="Employee postal code")
    PostalDistrictDK: Optional[str] = Field(None, description="Employee city name")
    PrivatePhoneNumber1: Optional[str] = Field(None, description="Private phone number")
    PrivatePhoneNumber2: Optional[str] = Field(None, description="Alternative private phone number")
    CompanyPhoneNumber1: Optional[str] = Field(None, description="Direct company phone number")
    CompanyPhoneNumber2: Optional[str] = Field(None, description="Mobile company phone number")
    CompanyEmail: Optional[str] = Field(None, description="Employee work e-mail address")
    PrivateEmail: Optional[str] = Field(None, description="Employee private e-mail address")
    Initials: Optional[str] = Field(None, description="Initials")
    SocialSecurityNumber: Optional[str] = Field(None, description="CPR-number")
    PostalCodeInt: Optional[str] = Field(None, description="Employee foreign postal code")
    PostalDistrictInt: Optional[str] = Field(None, description="Employee foreign city name")
    CountryCode: Optional[str] = Field(None, description="Country code for tax registration")
    Country: Optional[str] = Field(None, description="Country name")
    FirstHiredDate: Optional[datetime] = Field(None, description="Date of first employment")
    Seniority: Optional[str] = Field(None, description="Number of years, months and days employed (Format YYMMDD)")
    Eboks: Optional[str] = Field(None, description="Defines whether the employee receives the payslip in eBoks")
    RegistrationNumber: Optional[str] = Field(None, description="Employee bank registration number")
    AccountNumber: Optional[str] = Field(None, description="Employee bank account number")
    Email2: Optional[str] = Field(None, description="Email (Private)")
    BirthDate: Optional[datetime] = Field(None, description="Date of birth")
    Gender: Optional[str] = Field(None, description="Gender")
    StateCountryCode: Optional[str] = Field(None, description="Citizenship")
    BirthCountryCode: Optional[str] = Field(None, description="Country of birth")
    DefaultCalendarCode: Optional[str] = Field(None, description="Default Calendar code")
    Comment: Optional[str] = Field(None, description="Comment")
    CallingName: Optional[str] = Field(None, description="Nickname")
    SocialSecurityNumberAbroad: Optional[str] = Field(None, description="Foreign CPR-Number")
    VerificationDate: Optional[datetime] = Field(None, description="Date for validation of Registration/account number")
    NemAccount: Optional[str] = Field(None, description="Code for NemKonto")
    SalarySeniorityFrom: Optional[datetime] = Field(None, description="Salary seniority date")
    SalaryComputed: Optional[str] = Field(None, description="Part of payroll")
    SocialSecurityNumberValidated: Optional[str] = Field(None, description="CPR number validation")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    CreateTime: datetime = Field(..., description="Timestamp for creating the registration")
    UpdateTime: datetime = Field(..., description="Timestamp for latest update of the registration")
    
    @field_validator('FirstHiredDate', 'BirthDate', 'VerificationDate', 'SalarySeniorityFrom', 'CreateTime', 'UpdateTime', mode='before')
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
