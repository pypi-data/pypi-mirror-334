from datetime import datetime
from typing import List
from pydantic import Field
from at_common_schemas.base import BaseSchema
from at_common_schemas.core.calendar import (
    Dividends, Earnings, Splits
)

# Earnings
class CalendarEarningsListRequest(BaseSchema):
    """Request parameters for retrieving earnings calendar data."""
    from_date: datetime = Field(..., description="Start date for retrieving earnings calendar data (inclusive)")
    to_date: datetime = Field(..., description="End date for retrieving earnings calendar data (inclusive)")

class CalendarEarningsListResponse(BaseSchema):
    """Response containing earnings calendar data."""
    items: List[Earnings] = Field(..., description="List of daily earnings announcements within the requested date range")

# Dividend
class CalendarDividendsListRequest(BaseSchema):
    """Request parameters for retrieving dividend calendar data."""
    from_date: datetime = Field(..., description="The start date for the dividend request.")
    to_date: datetime = Field(..., description="The end date for the dividend request.")

class CalendarDividendsListResponse(BaseSchema):
    """Response containing dividend calendar data."""
    items: List[Dividends] = Field(..., description="List of calendar dividends.")

# Split
class CalendarSplitsListRequest(BaseSchema):
    """Request parameters for retrieving stock split calendar data."""
    from_date: datetime = Field(..., description="Start date for retrieving stock split calendar data (inclusive)")
    to_date: datetime = Field(..., description="End date for retrieving stock split calendar data (inclusive)")

class CalendarSplitsListResponse(BaseSchema):
    """Response containing stock split calendar data."""
    items: List[Splits] = Field(..., description="List of daily stock splits within the requested date range")