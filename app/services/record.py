"""
Records service, containing different methods to handle the records from within the database
"""
import logging
import statistics
from datetime import datetime
from typing import List, Dict

from fastapi import Depends
from sqlalchemy import func, and_, exists
from sqlalchemy.orm import Session
from sqlalchemy.sql import case

from app.models.record import Records
from app.services.database import get_session

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class UserException(Exception):
    """User service related Exceptions"""


class UserNotFoundException(UserException):
    """User not found exception"""

    def __init__(self, message="User not found."):
        super().__init__(message)


class RecordsService:
    """Service class for handling records related to customers."""

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def customer_exists(self, customer_id: str) -> bool:
        """Checks if a customer with the given ID exists in the database."""
        return self.session.query(
            exists().where(Records.customer_id == customer_id)
        ).scalar()

    def get_customer_stats(self, customer_id: str, from_date: datetime) -> List[Dict]:
        """
        Retrieves customer statistics from the records starting from a given date.

        Args:
            customer_id (str): The ID of the customer to retrieve stats for.
            from_date (datetime): The starting date from which to retrieve the records.

        Returns:
            List[Dict]: A list of dictionaries containing stats per date.
        """
        results = self._perform_query(customer_id, from_date)
        return self._process_results(results)

    def _perform_query(self, customer_id: str, from_date: datetime) -> List:
        """
        Performs the SQL query to fetch records data.

        Args:
            customer_id (str): The customer's ID.
            from_date (datetime): The starting date from which records are considered.

        Returns:
            List: Raw query results containing records data.
        """
        query = (
            self.session.query(
                func.date(Records.timestamp).label("date"),
                func.count().label("total_requests"),
                func.sum(case((Records.status_code == 200, 1), else_=0)).label(
                    "successful_requests"
                ),
                func.sum(case((Records.status_code != 200, 1), else_=0)).label(
                    "failed_requests"
                ),
                func.avg(Records.duration).label("average_latency"),
                func.group_concat(Records.duration).label("durations"),
            )
            .filter(
                and_(Records.customer_id == customer_id, Records.timestamp >= from_date)
            )
            .group_by(func.date(Records.timestamp))
            .order_by(func.date(Records.timestamp))
        )
        return query.all()

    def _process_results(self, results: List) -> List[Dict]:
        """
        Processes the query results into formatted statistics.

        Args:
            results (List): List of raw results from the SQL query.

        Returns:
            List[Dict]: Processed and formatted statistics for each record.
        """
        stats = []
        for row in results:
            durations = list(map(float, row.durations.split(",")))
            stats.append(
                {
                    "date": row.date,
                    "successful_requests": row.successful_requests,
                    "failed_requests": row.failed_requests,
                    "uptime": self._calculate_uptime(
                        row.successful_requests, row.total_requests
                    ),
                    "average_latency": row.average_latency,
                    "median_latency": statistics.median(durations),
                    "p99_latency": statistics.quantiles(durations, n=100)[98],
                }
            )
        return stats

    @staticmethod
    def _calculate_uptime(successful_requests: int, total_requests: int) -> float:
        """
        Calculates the uptime percentage.

        Args:
            successful_requests (int): Number of successful requests.
            total_requests (int): Total number of requests.

        Returns:
            float: Uptime percentage.
        """
        return (successful_requests / total_requests) * 100 if total_requests > 0 else 0
