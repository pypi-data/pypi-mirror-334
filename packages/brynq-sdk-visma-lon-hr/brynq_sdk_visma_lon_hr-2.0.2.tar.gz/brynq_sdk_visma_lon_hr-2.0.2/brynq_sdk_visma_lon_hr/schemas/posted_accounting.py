from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class PostedAccountingSchema(BaseModel):
    """
    Schema for posted accounting data from Visma Lon HR.
    Represents posted accounting information from the VISMALØN table KOERSELSSELEKTION.
    """
    
    PostedAccountingRID: str = Field(..., description="Unique key for use of OData")
    CustomerID: str = Field(..., description="Customer ID")
    EmployerID: str = Field(..., description="Employer number")
    EmployeeID: str = Field(..., description="Employee number")
    EmploymentID: str = Field(..., description="Employment")
    AccountingSerialNumber1: str = Field(..., description="Accounting serial number")
    AccountingSerialNumber2: Optional[str] = Field(None, description="Secondary accounting number")
    BreakdownNumber: Optional[str] = Field(None, description="Break down number")
    CalculatedSalaryNumber: Optional[str] = Field(None, description="Calculated salary number")
    PayPeriodStart: datetime = Field(..., description="Start date of the payroll period")
    PayPeriodEnd: datetime = Field(..., description="End date of the payroll period")
    PayrollRunNumber: str = Field(..., description="Payroll run number")
    AccountNumber: Optional[str] = Field(None, description="Account number for bookkeeping")
    AccountName: Optional[str] = Field(None, description="Account name for bookkeeping")
    Amount: Optional[str] = Field(None, description="Amount")
    Rate: Optional[str] = Field(None, description="Rate for payout")
    DebitCreditCode: Optional[str] = Field(None, description="D=Debet/K=Credit")
    OrganizationalUnitID: Optional[str] = Field(None, description="Organisation ID")
    UdbetalingsStedNr: Optional[str] = Field(None, description="Subsection number")
    PaymentConditionCode: Optional[str] = Field(None, description="Position category")
    WageGroupNumber: Optional[str] = Field(None, description="Pay group")
    SalaryScale: Optional[str] = Field(None, description="Pay scale")
    SalaryStep: Optional[str] = Field(None, description="Salary step")
    CustomizedInformation1: Optional[str] = Field(None, description="Optional1")
    CustomizedInformation2: Optional[str] = Field(None, description="Optional2")
    CustomizedInformation3: Optional[str] = Field(None, description="Optional3")
    CustomizedInformation4: Optional[str] = Field(None, description="Optional4")
    CustomizedInformation5: Optional[str] = Field(None, description="Optional5")
    CustomizedInformation6: Optional[str] = Field(None, description="Optional6")
    VersionNumber: str = Field(..., description="Used to control the update of data (internal Datahub field)")
    PayTypeCode: Optional[str] = Field(None, description="Wage type number")
    WageConditionNumber: Optional[str] = Field(None, description="Paid in arrear, paid in advance, hourly or forthnightly paid")
    Value: Optional[str] = Field(None, description="Value")
    CreatedByPayroll: Optional[str] = Field(None, description="Created by payroll")
    COA_OrganizationalUnitID: Optional[str] = Field(None, description="Department or input constant from account plan")
    COA_UDBETALINGSSTEDNR: Optional[str] = Field(None, description="Subsection if Finans is marked with a udbetalingskode")
    COA_InputCode: Optional[str] = Field(None, description="Inputvalue if this is chosen to be shown in the account plan")
    COA_EmployeeID: Optional[str] = Field(None, description="Employeenumber if this is chosen to be shown in the account plan")
    ChartOfAccounts: Optional[str] = Field(None, description="Account plan number / name")
    SalaryDistributed: Optional[str] = Field(None, description="If values are distributet between ex. department / pct")
    SettlementMethod: Optional[str] = Field(None, description="Only deduction wage types with reg/bank accountnumber can have the code BC")
    UseCode: Optional[str] = Field(None, description="How the wage type must be shown in connection to output")
    PrintedOnPayslip: Optional[str] = Field(None, description="Wage type show on the payslip")
    PensionYearMark: Optional[str] = Field(None, description="Value = 1 moves the settlement from current year to first bank day in the new year")
    SelectedDate: Optional[datetime] = Field(None, description="Accounting date")
    VismaLoenDepartment: Optional[str] = Field(None, description="Department")
    
    @field_validator('PayPeriodStart', 'PayPeriodEnd', 'SelectedDate', mode='before')
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