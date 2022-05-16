import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, Optional

from sqlalchemy import asc, create_engine, func
from sqlalchemy.orm import sessionmaker

from core.repository.events import EventType
from core.repository.models import DeclarativeBase, Event, Record


class Storage:
    def __init__(self, path: Optional[str] = None) -> None:
        self.path = path or ":memory:"
        self.url = None
        self.engine = None
        self.session_factory = None

        if self.path:
            self.load(path=self.path)

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

    def __len__(self):
        session = self.session_factory()

        count = session.query(Record).with_entities(func.count()).scalar()
        return count

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
        self.path = path
        self.url = f"sqlite:///{self.path if self.path == ':memory:' else Path(self.path).resolve()}"
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
        for record in session.query(Record).order_by(asc(Record.id)):
            keys.append(record.key)

        return keys

    def items(self):
        session = self.session_factory()

        items = [(record.key, record.value) for record in session.query(Record)]

        return items

    def clear(self):
        for key in self.keys():
            self.__delitem__(key=key)


class Repository:
    def __init__(self, path: str):
        self.main_storage: Storage = Storage(path=path)
        self.backup_storage: Optional[Storage] = None
        self.is_dirty: bool = False

    def __getitem__(self, key: str) -> Optional[str]:
        value = self.main_storage[key]

        return value

    def __setitem__(self, key: str, value: str) -> None:
        self.is_dirty = True
        self.backup()

        self.main_storage[key] = value

    def __delitem__(self, key: str) -> None:
        self.is_dirty = True
        self.backup()

        del self.main_storage[key]

    def __del__(self):
        if hasattr(self.backup_storage, "file"):
            self.backup_storage.file.close()

    def __len__(self) -> int:
        return len(self.main_storage)

    @property
    def path(self) -> str:
        return self.main_storage.path

    def backup(self) -> None:
        if not self.is_dirty:
            return

        if not self.backup_storage:
            file = NamedTemporaryFile("w+")
            self.backup_storage = Storage(path=file.name)
            self.backup_storage.file = file

        for k, v in self.main_storage.items():
            self.backup_storage[k] = v

    def restore(self) -> None:
        if not self.is_dirty:
            return

        self.is_dirty = False

        self.main_storage.clear()
        for k, v in self.backup_storage.items():
            self.main_storage[k] = v

        self.backup_storage.file.close()
        self.backup_storage = None

    def load(self, path: str) -> None:
        self.main_storage = Storage(path=path)
        self.backup_storage = None
        self.is_dirty = False

    def save(self, path: Optional[str] = None) -> None:
        if not path:
            self.is_dirty = False
            return

        destination = Path(path).resolve()
        source = Path(self.main_storage.path).resolve()

        shutil.copy(source, destination)

        self.main_storage.path = path

    def keys(self):
        return self.main_storage.keys()

    def items(self):
        return self.main_storage.items()

    def commit_success_event(self, key: str) -> None:
        self.main_storage.commit_success_event(key=key)

    def commit_failure_event(self, key: str) -> None:
        self.main_storage.commit_failure_event(key=key)

    def commit_hint_event(self, key: str) -> None:
        self.main_storage.commit_hint_event(key=key)
