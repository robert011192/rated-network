from sqlalchemy import Column, Integer, DateTime, String, Float

from app.db.base_class import Base


class Records(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    customer_id = Column(String, index=True)
    request_path = Column(String)
    status_code = Column(Integer)
    duration = Column(Float)
