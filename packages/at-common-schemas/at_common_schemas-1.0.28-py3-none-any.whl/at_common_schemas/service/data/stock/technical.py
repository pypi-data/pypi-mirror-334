from datetime import datetime
from typing import List
from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.core.technical import TechnicalPattern, TechnicalIndicator

class TechnicalIndicatorListRequest(BaseSchema):
    symbols: List[str] = Field(..., description="List of stock symbols")
    date_from: datetime = Field(..., description="Start date for the request")
    date_to: datetime = Field(..., description="End date for the request")

class TechnicalIndicatorListResponse(BaseSchema):
    items: List[TechnicalIndicator] = Field(..., description="List of technical indicators")

class TechnicalPatternListRequest(BaseSchema):
    symbols: List[str] = Field(..., description="List of stock symbols")
    date_from: datetime = Field(..., description="Start date for the request")
    date_to: datetime = Field(..., description="End date for the request")

class TechnicalPatternListResponse(BaseSchema):
    items: List[TechnicalPattern] = Field(..., description="List of technical patterns")