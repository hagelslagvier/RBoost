from typing import List, Optional

from core.repository.events import EventType
from core.repository.models import DeclarativeBase, Event, Record
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Storage:
    def __init__(self, url: str) -> None:
        self.engine = create_engine(url)
        self.session_factory = sessionmaker(bind=self.engine)

        DeclarativeBase.metadata.create_all(bind=self.engine)

    def __getitem__(self, key: str) -> Optional[str]:
        session = self.session_factory()

        record = session.query(Record).filter(Record.key == key).one_or_none()

        value = record.value if record else None

        return value

    def __setitem__(self, key: str, value: str) -> None:
        session = self.session_factory()

        record = Record(key=key, value=value)
        session.add(record)
        session.commit()

    def __delitem__(self, key: str) -> None:
        session = self.session_factory()

        record = session.query(Record).filter(Record.key == key).one()

        session.delete(record)
        session.commit()

    def _commit_event(self, key: str, event_type: EventType):
        session = self.session_factory()

        record = session.query(Record).filter(Record.key == key).one()

        event = Event(event_type=event_type, record=record)
        session.add(event)
        session.commit()

    def commit_success_event(self, key):
        self._commit_event(key=key, event_type=EventType.SUCCESS)

    def commit_failure_event(self, key):
        self._commit_event(key=key, event_type=EventType.FAILURE)

    def commit_hint_event(self, key):
        self._commit_event(key=key, event_type=EventType.HINT)

    def all_keys(self) -> List[str]:
        session = self.session_factory()

        keys = []
        for key in session.query(Record.key):
            keys.append(key)

        return keys
