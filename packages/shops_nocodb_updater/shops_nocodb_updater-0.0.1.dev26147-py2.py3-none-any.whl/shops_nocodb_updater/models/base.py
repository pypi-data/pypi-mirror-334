from typing import Optional, List, Dict, Any

from pydantic import BaseModel

ID_FIELD = "Id"


class NocodbModel(BaseModel):
    """
    Base model for NocoDB tables. 
    Inherit from this class to define your NocoDB table models.
    """
    __tableid__: str  # The NocoDB table ID
    __skip_update_attributes__: Optional[List[str]] = None  # Keys to skip during data comparison

    class Config:
        # Allow extra fields
        extra = "allow"


class PaginationResponseModel(BaseModel):
    """
    Model representing pagination information from NocoDB.
    """
    total_rows: int
    page: int
    page_size: int
    is_first_page: bool
    is_last_page: bool


def get_pagination_info(page_info: dict) -> PaginationResponseModel:
    """
    Convert NocoDB pagination info to a PaginationResponseModel.
    
    Args:
        page_info: The pagination info dictionary from NocoDB
        
    Returns:
        PaginationResponseModel with the parsed information
    """
    return PaginationResponseModel(
        total_rows=page_info["totalRows"],
        page=page_info["page"],
        page_size=page_info["pageSize"],
        is_first_page=page_info["isFirstPage"],
        is_last_page=page_info["isLastPage"],
    ) 