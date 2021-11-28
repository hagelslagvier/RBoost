from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.repository.models import DeclarativeBase


engine = create_engine("sqlite:///:memory:")

session_factory = sessionmaker(bind=engine)

session = session_factory()


DeclarativeBase.metadata.create_all(engine)
