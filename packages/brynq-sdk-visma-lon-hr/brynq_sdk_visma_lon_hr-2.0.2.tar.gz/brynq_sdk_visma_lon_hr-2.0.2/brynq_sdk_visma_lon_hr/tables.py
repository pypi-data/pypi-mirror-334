from typing import Union, Optional, List
import pandas as pd
import requests
import xmltodict
from .utils import clean_column_names, handle_duplicate_columns

class Tables:
    """
    Handles table operations for Visma Lon HR API.
    """
    def __init__(self, visma_instance):
        self.visma = visma_instance

    def get(self, 
            table_name: str,
            filter: Optional[str] = None,
            select: Optional[Union[List[str], str]] = None,
            orderby: Optional[Union[List[str], str]] = None,
            top: Optional[int] = None,
            skip: Optional[int] = None,
            skiptoken: Optional[str] = None,
            max_pages: Optional[int] = None) -> pd.DataFrame:
        """
        Get data from a specified table in Visma.
        
        Args:
            table_name (str): Name of the table to query.
            filter (str, optional): OData filter expression. Defaults to None.
            select (Union[List[str], str], optional): Columns to select. Defaults to None.
            orderby (Union[List[str], str], optional): Columns to order by. Defaults to None.
            top (int, optional): Number of records to return. Defaults to None.
            skip (int, optional): Number of records to skip. Defaults to None.
            skiptoken (str, optional): Token for continuing a paged request. Defaults to None.
            max_pages (int, optional): Maximum number of pages to fetch. Defaults to None (all pages).

        Returns:
            pd.DataFrame: DataFrame with table data
        """
        return self.visma.get(
            entity_type=f'{table_name}',
            filter=filter,
            select=select,
            orderby=orderby,
            top=top,
            skip=skip,
            skiptoken=skiptoken,
            max_pages=max_pages
        )
