"""
Stats endpoints
"""
import logging

from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from fastapi.responses import JSONResponse
from fastapi import status

from app.services.record import RecordsService
from app.services.database import get_session

router = APIRouter()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@router.get("/customers/{id}/stats", response_model=List[dict])
def get_customer_stats(
    id: str,
    from_: str = Query(..., alias="from"),
    session: Session = Depends(get_session),
):
    """
    Get daily statistics for a specific customer starting from the given date.

    Args:
        id (str): Customer ID.
        from_ (str): Start date in YYYY-MM-DD format (alias for `from` query parameter).
        session (Session): Database session.

    Returns:
        List[dict]: List of daily statistics.
    """
    try:
        from_date_obj = datetime.strptime(from_, "%Y-%m-%d")
        records_service = RecordsService(session)

        # Check if the customer exists
        if not records_service.customer_exists(id):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Customer not found."},
            )

        stats = records_service.get_customer_stats(id, from_date_obj)
        if not stats:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "message": "No records found for the given customer and date range."
                },
            )
        return stats

    except ValueError:
        logger.error(f"Invalid date format received: {from_}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Invalid date format. Use YYYY-MM-DD."},
        )
    except Exception as e:
        logger.error(f"An error occurred while retrieving customer stats: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )
