from datetime import datetime
from typing import Union, Optional
from pydantic import BaseModel, Field

class SalarySchema(BaseModel):
    """Schema for salary data from Visma Lon HR"""
    
    AccountNumber: Optional[str] = Field(None, description="Account number associated with the salary")
    Amount: str = Field(..., description="Salary amount")
    CalculatedSalaryName: str = Field(..., description="Name of the calculated salary")
    CalculatedSalaryNumber: str = Field(..., description="Number identifying the calculated salary")
    CalculatedSalaryRID: str = Field(..., description="Resource identifier for the calculated salary")
    CustomerID: str = Field(..., description="Customer ID associated with this salary")
    EmployeeID: str = Field(..., description="Employee ID for whom the salary is recorded")
    EmployerID: str = Field(..., description="Employer ID associated with this salary")
    EmploymentID: str = Field(..., description="Employment ID associated with this salary")
    MadeByAdjustment: str = Field(..., description="Indicator if the salary was made by adjustment")
    OriginalPayrollRunNumber: str = Field(..., description="Original payroll run number")
    OriginalPayrollSelectionNumber: str = Field(..., description="Original payroll selection number")
    PayPeriodEnd: datetime = Field(..., description="End date of the pay period")
    PayPeriodStart: datetime = Field(..., description="Start date of the pay period")
    PayTypeCode: str = Field(..., description="Code for the type of pay")
    PayrollRunNumber: str = Field(..., description="Payroll run number")
    PayrollSelectionNumber: str = Field(..., description="Payroll selection number")
    RegistrationNumber: str = Field(..., description="Registration number")
    TransactionType: str = Field(..., description="Type of transaction")
    Value1: Optional[Union[str, float]] = Field(None, description="First value associated with the salary")
    Value2: Optional[Union[str, float]] = Field(None, description="Second value associated with the salary")
    Value3: Optional[Union[str, float]] = Field(None, description="Third value associated with the salary")
    Value4: Optional[Union[str, float]] = Field(None, description="Fourth value associated with the salary")
    Value5: Optional[Union[str, float]] = Field(None, description="Fifth value associated with the salary")
    Value6: Optional[Union[str, float]] = Field(None, description="Sixth value associated with the salary")
    VersionNumber: str = Field(..., description="Version number of the record")