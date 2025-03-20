from typing import Optional, Union, List
import pandas as pd
import xmltodict
from .utils import parse_xml_to_df
from .schemas.salary import SalarySchema

class Salary:
    """
    Handles salary operations for Visma Lon HR API.
    """

    def __init__(self, visma_instance):
        """
        Initialize the Salary class.

        Args:
            visma_instance: The Visma class instance.
        """
        self.visma = visma_instance

    def get(self, 
            filter: Optional[str] = None,
            select: Optional[Union[List[str], str]] = None,
            orderby: Optional[Union[List[str], str]] = None,
            top: Optional[int] = None,
            skip: Optional[int] = None,
            skiptoken: Optional[str] = None,
            max_pages: Optional[int] = None) -> pd.DataFrame:
        """
        Get salary data from Visma.
        
        Args:
            filter (str, optional): OData filter expression. Defaults to None.
            select (Union[List[str], str], optional): Columns to select. Defaults to None.
            orderby (Union[List[str], str], optional): Columns to order by. Defaults to None.
            top (int, optional): Number of records to return. Defaults to None.
            skip (int, optional): Number of records to skip. Defaults to None.
            skiptoken (str, optional): Token for continuing a paged request. Defaults to None.
            max_pages (int, optional): Maximum number of pages to fetch. Defaults to None (all pages).

        Returns:
            pd.DataFrame: DataFrame with salary data
        """
        from .schemas import SalarySchema
        return self.visma.get(
            entity_type="CalculatedSalary",
            filter=filter,
            select=select,
            orderby=orderby,
            top=top,
            skip=skip,
            skiptoken=skiptoken,
            max_pages=max_pages,
            schema=SalarySchema
        )
