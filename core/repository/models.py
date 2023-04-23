from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

from core.repository.events import EventType

DeclarativeBase = declarative_base()


class BaseModel(DeclarativeBase):
    __abstract__ = True

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Event(BaseModel):
    __tablename__ = "events"

    id = Column(Integer(), primary_key=True)

    event_type = Column(Enum(EventType))
    record_id = Column(Integer(), ForeignKey("records.id"))
    record = relationship("Record", backref=backref("events", order_by=record_id))

    def __repr__(self):
        return f"Event(id={self.id}, event_type={self.event_type.name}, record_id={self.record_id})"


class Record(BaseModel):
    __tablename__ = "records"

    id = Column(Integer(), primary_key=True)

    key = Column(String(length=256), unique=True, nullable=False)
    value = Column(Text(length=1024), nullable=False)
    is_checked = Column(Boolean, default=True)

    def __repr__(self):
        return f"Record(id={self.id}, key={self.key}, value={self.value}, is_checked={self.is_checked})"
