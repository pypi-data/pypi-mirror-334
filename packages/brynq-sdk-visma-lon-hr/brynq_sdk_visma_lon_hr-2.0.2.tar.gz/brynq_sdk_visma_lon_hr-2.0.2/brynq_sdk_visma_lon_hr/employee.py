from typing import Optional, List, Union
import pandas as pd
from .schemas.employee import EmployeeSchema

class Employee:
    """
    Handles table operations for Visma Lon HR API.
    """

    def __init__(self, visma_instance):
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
        Fetch data from Employee table in Visma Lon HR with pagination and filtering support.

        Args:
            filter (str, optional): OData filter expression. Defaults to None.
            select (Union[List[str], str], optional): Columns to select. Can be a comma-separated string or list of strings. Defaults to None.
            orderby (Union[List[str], str], optional): Columns to order by. Can be a comma-separated string or list of strings. Defaults to None.
            top (int, optional): Number of records to return. Defaults to None.
            skip (int, optional): Number of records to skip. Defaults to None.
            skiptoken (str, optional): Token for continuing a paged request. Defaults to None.
            max_pages (int, optional): Maximum number of pages to fetch. Defaults to None (fetch all pages).

        Returns:
            pd.DataFrame: A DataFrame containing all fetched employee data.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
            ValueError: If the response cannot be parsed or converted to DataFrame.
        """
        return self.visma.get(
            entity_type="Employee", 
            filter=filter,
            select=select,
            orderby=orderby,
            top=top,
            skip=skip,
            skiptoken=skiptoken,
            max_pages=max_pages, 
            schema=EmployeeSchema
        )
