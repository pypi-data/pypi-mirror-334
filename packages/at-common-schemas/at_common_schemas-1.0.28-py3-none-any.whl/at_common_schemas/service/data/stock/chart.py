from datetime import datetime
from typing import List
from at_common_schemas.base import BaseSchema
from pydantic import Field
from at_common_schemas.core.chart import ChartEOD, ChartIntraday, ChartInterval

class ChartEODListRequest(BaseSchema):
    symbol: str = Field(..., description="Stock symbol")
    date_from: datetime = Field(..., description="Start date for the request")
    date_to: datetime = Field(..., description="End date for the request")

class ChartEODListResponse(BaseSchema):
    items: List[ChartEOD] = Field(..., description="List of daily candlestick data")

class ChartIntradayListRequest(BaseSchema):
    symbol: str = Field(..., description="Stock symbol")
    time_from: datetime = Field(..., description="Start time for the request")
    time_to: datetime = Field(..., description="End time for the request")
    interval: ChartInterval = Field(..., description="Time interval for the request")

class ChartIntradayListResponse(BaseSchema):
    items: List[ChartIntraday] = Field(..., description="List of intraday candlestick data")