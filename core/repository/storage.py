from pathlib import Path
from typing import List, Optional

from core.repository.events import EventType
from core.repository.models import DeclarativeBase, Event, Record
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Storage:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.url = None
        self.engine = None
        self.session_factory = None
        self.is_dirty = False

        self.load(path=str(self.path.resolve()))

    def __getitem__(self, key: str) -> Optional[str]:
        session = self.session_factory()

        record = session.query(Record).filter(Record.key == key).one_or_none()

        value = record.value if record else None

        return value

    def __setitem__(self, key: str, value: str) -> None:
        session = self.session_factory()

        record = session.query(Record).filter(Record.key == key).one_or_none()
        if record:
            record.value = value
        else:
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

    def load(self, path: str) -> None:
        self.path = Path(path)
        self.url = f"sqlite:///{self.path.resolve()}"
        self.engine = create_engine(url=self.url)
        self.session_factory = sessionmaker(bind=self.engine)

        DeclarativeBase.metadata.create_all(bind=self.engine)

    def dump(self, path: str) -> None:
        url = f"sqlite:///{Path(path).resolve()}"
        engine = create_engine(url=url)

        DeclarativeBase.metadata.create_all(bind=engine)

        storage = Storage(path=path)

        for key, value in self.items():
            storage[key] = value

    def keys(self) -> List[str]:
        session = self.session_factory()

        keys = []
        for record in session.query(Record):
            keys.append(record.key)

        return keys

    def items(self):
        session = self.session_factory()

        items = [(record.key, record.value) for record in session.query(Record)]

        return items

    def clear(self):
        for key in self.keys():
            self.__delitem__(key=key)
