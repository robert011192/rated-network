"""Database service, to be injected in different other services"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.sql_alchemy_uri())
SessionLocal = sessionmaker(bind=engine, future=True)


async def get_session():
    """Dependency injection for a database session"""
    with SessionLocal() as session:
        yield session
        session.commit()
