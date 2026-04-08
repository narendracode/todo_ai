from typing import Type, Any, Dict, List

from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

import logging

logger = logging.getLogger(__name__)


class GetBookingsToolInput(BaseModel):
    mobile_number: str = Field(description="Mobile number of the user")


class GetBookingsTool(BaseTool):
    name: str = "get_bookings"
    description: str = "Get bookings from the database via API"
    args_schema: Type[BaseModel] = GetBookingsToolInput

    """Call the actual API to get the booking data
    """

    def _run(self, **kwargs) -> Dict[str, Any]:
        """Synchronous API call."""
        args = GetBookingsToolInput.model_validate(kwargs)
        return f"According to your phone number {args.mobile_number}, I found two bookings. Booking ID: 123456, Jumbo on 5th May 2026 and booking ID: 789012 Taj Mahal on 10th June 2026"

    async def _arun(self, **kwargs) -> Dict[str, Any]:
        """Asynchronous API call."""
        args = GetBookingsToolInput.model_validate(kwargs)
        return f"According to your phone number {args.mobile_number}, I found two bookings. Booking ID: 123456, Jumbo on 5th May 2026 and booking ID: 789012 Taj Mahal on 10th June 2026"
    