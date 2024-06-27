"""
Stats endpoints
"""
from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.services.record import RecordsService
from app.services.database import get_session

router = APIRouter()


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
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD."
        )

    records_service = RecordsService(session)
    stats = records_service.get_customer_stats(id, from_date_obj)
    if not stats:
        raise HTTPException(
            status_code=404,
            detail="No records found for the given customer and date range.",
        )

    return stats
