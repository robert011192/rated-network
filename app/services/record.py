"""
Records service, containing different methods to handle the records from within the database
"""
import logging
import statistics
from datetime import datetime

from fastapi import Depends
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql import case

from app.models.record import Records
from app.services.database import get_session

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RecordsService:
    """Record service"""

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_customer_stats(self, customer_id: str, from_date: datetime):
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

        results = query.all()
        stats = []
        for row in results:
            durations = list(map(float, row.durations.split(",")))
            median_latency = statistics.median(durations)
            p99_latency = statistics.quantiles(durations, n=100)[98]
            uptime = (row.successful_requests / row.total_requests) * 100
            stats.append(
                {
                    "date": row.date,
                    "successful_requests": row.successful_requests,
                    "failed_requests": row.failed_requests,
                    "uptime": uptime,
                    "average_latency": row.average_latency,
                    "median_latency": median_latency,
                    "p99_latency": p99_latency,
                }
            )
        return stats
