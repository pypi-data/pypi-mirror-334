from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class EmploymentSchema(BaseModel):
    """
    Schema for employment data from Visma Lon HR.
    Represents employment information from the VISMALØN table ANSFORHOLD.
    """
    
    EmploymentRID: str = Field(..., description="Unique key for use of OData")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    CustomerID: str = Field(..., description="Customer ID")
    EmployerID: str = Field(..., description="Employer number")
    EmployeeID: str = Field(..., description="Employee number")
    EmploymentID: str = Field(..., description="Employment")
    StartDate: datetime = Field(..., description="Start date in Visma Løn")
    EndDate: Optional[datetime] = Field(None, description="Change or termination of Employment")
    FromDate: Optional[datetime] = Field(None, description="From date")
    ToDate: Optional[datetime] = Field(None, description="To date")
    OrganizationalUnitID: Optional[str] = Field(None, description="Department ID")
    OrganizationalUnitName: Optional[str] = Field(None, description="Department name")
    PlaceOfWorkNumber: Optional[str] = Field(None, description="P-nummer if it deviates from the p-number registered on the employer")
    EmploymentDesignation: Optional[str] = Field(None, description="Title")
    PaymentConditionCode: Optional[str] = Field(None, description="Position category")
    WageConditionNumber: Optional[str] = Field(None, description="Prepaid, paid in arrears, hourly- or forthnightly paid")
    WorkingHourNumerator: Optional[str] = Field(None, description="Number of employee working hours per month")
    WorkingHourDenominator: Optional[str] = Field(None, description="Number of full time working hours per month or per forthnightly period")
    VacationWeek: Optional[str] = Field(None, description="Vacation week")
    SalaryScale: Optional[str] = Field(None, description="Pay scale")
    SalaryStep: Optional[str] = Field(None, description="Salary step")
    UdbetalingsStedNR: Optional[str] = Field(None, description="Subsection")
    WageGroupNumber: Optional[str] = Field(None, description="Pay group")
    DateOfEmployment: Optional[datetime] = Field(None, description="Hire date")
    TerminationDate: Optional[datetime] = Field(None, description="Termination date")
    CustomizedInformation1: Optional[str] = Field(None, description="Optional1")
    CustomizedInformation2: Optional[str] = Field(None, description="Optional2")
    CustomizedInformation3: Optional[str] = Field(None, description="Optional3")
    CustomizedInformation4: Optional[str] = Field(None, description="Optional4")
    CustomizedInformation5: Optional[str] = Field(None, description="Optional5")
    CustomizedInformation6: Optional[str] = Field(None, description="Optional6")
    AutoMovement: Optional[str] = Field(None, description="Auto movement")
    MovementCode1: Optional[str] = Field(None, description="Name of table for movement in relation to use of Pay scale/salary step")
    MovementCode2: Optional[str] = Field(None, description="Name of table for movement in relation to use of Pay scale/salary step")
    MovementCode3: Optional[str] = Field(None, description="Name of table for movement in relation to use of Pay scale/salary step")
    LastMovementDate1: Optional[datetime] = Field(None, description="Date of last movement in relation to use of Pay scale/salary step")
    LastMovementDate2: Optional[datetime] = Field(None, description="Date of last movement in relation to use of Pay scale/salary step")
    LastMovementDate3: Optional[datetime] = Field(None, description="Date of last movement in relation to use of Pay scale/salary step")
    NextMovementDate1: Optional[datetime] = Field(None, description="Date of next movement in relation to use of Pay scale/salary step")
    NextMovementDate2: Optional[datetime] = Field(None, description="Date of next movement in relation to use of Pay scale/salary step")
    NextMovementDate3: Optional[datetime] = Field(None, description="Date of next movement in relation to use of Pay scale/salary step")
    AutoMovementCode1: Optional[str] = Field(None, description="Must the movement in relation to use of Pay scale/salary step be automatic? Ja (yes) or Nej (no)")
    AutoMovementCode2: Optional[str] = Field(None, description="Must the movement in relation to use of Pay scale/salary step be automatic? Ja (yes) or Nej (no)")
    AutoMovementCode3: Optional[str] = Field(None, description="Must the movement in relation to use of Pay scale/salary step be automatic? Ja (yes) or Nej (no)")
    JobFunctionNumber: Optional[str] = Field(None, description="Job function number")
    JobFunctionName: Optional[str] = Field(None, description="Name of job function number")
    Occupation: Optional[str] = Field(None, description="Position")
    InternalOccupationCode: Optional[str] = Field(None, description="Internal position code")
    OccupationTypeCode: Optional[str] = Field(None, description="Position type code")
    ChangeReasonCode: Optional[str] = Field(None, description="Code for change reason")
    InternalTitleCode: Optional[str] = Field(None, description="Internal title code")
    WorkPlanCode: Optional[str] = Field(None, description="Work plan code")
    SkillRequirementCode: Optional[str] = Field(None, description="Education requirement code")
    ExtraNoticePersonMonth: Optional[str] = Field(None, description="Extra termination notice employee")
    ExtraNoticeCompanyMonth: Optional[str] = Field(None, description="Extra termination notice company")
    Comment: Optional[str] = Field(None, description="Comment")
    PayrollRunNumber: Optional[str] = Field(None, description="Payroll run number")
    Seniority2: Optional[str] = Field(None, description="Seniority date 2")
    Anniversary2: Optional[str] = Field(None, description="Anniversary date 2")
    ResignationCode: Optional[str] = Field(None, description="Termination reason code")
    EmploymentTypeCode: Optional[str] = Field(None, description="Employment type code")
    VismaLoenDepartment: Optional[str] = Field(None, description="Cost center")
    CreateTime: datetime = Field(..., description="Timestamp for creating the registration")
    UpdateTime: datetime = Field(..., description="Timestamp for latest update of the registration")
    
    @field_validator('StartDate', 'EndDate', 'FromDate', 'ToDate', 
                    'DateOfEmployment', 'TerminationDate',
                    'LastMovementDate1', 'LastMovementDate2', 'LastMovementDate3',
                    'NextMovementDate1', 'NextMovementDate2', 'NextMovementDate3',
                    'CreateTime', 'UpdateTime', mode='before')
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