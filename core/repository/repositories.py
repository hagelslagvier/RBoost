import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, Optional, Tuple, Union

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
        session.close()

        return value

    def __setitem__(self, key: Union[str, Tuple[str, str]], value: str) -> None:
        session = self.session_factory()

        if isinstance(key, str):
            record = session.query(Record).filter(Record.key == key).one_or_none()
            if record:
                record.value = value
            else:
                record = Record(key=key, value=value)

        elif isinstance(key, tuple):
            old_key, new_key = key
            record = session.query(Record).filter(Record.key == old_key).one_or_none()
            if record:
                record.key = new_key
                record.value = value
            else:
                raise RuntimeError(f"Record with key='{old_key}' not found")

        else:
            raise TypeError(
                f"key must be of type Union[str, Tuple[str, str]], got {tuple(key)}"
            )

        session.add(record)
        session.commit()
        session.close()

    def __delitem__(self, key: str) -> None:
        session = self.session_factory()
        record = session.query(Record).filter(Record.key == key).one()

        session.delete(record)

        session.commit()
        session.close()

    def __len__(self) -> int:
        session = self.session_factory()

        count = session.query(func.count(Record.id)).scalar()

        session.close()

        return count

    def _commit_event(self, key: str, event_type: EventType) -> None:
        session = self.session_factory()

        record = session.query(Record).filter(Record.key == key).one()

        event = Event(event_type=event_type, record=record)
        session.add(event)
        session.commit()
        session.close()

    def commit_success_event(self, key: str) -> None:
        self._commit_event(key=key, event_type=EventType.SUCCESS)

    def commit_failure_event(self, key: str) -> None:
        self._commit_event(key=key, event_type=EventType.FAILURE)

    def commit_hint_event(self, key: str) -> None:
        self._commit_event(key=key, event_type=EventType.HINT)

    def is_checked(self, key: str) -> bool:
        session = self.session_factory()

        record = session.query(Record).filter(Record.key == key).one()

        session.close()

        return record.is_checked

    def set_checked(self, key: str) -> None:
        session = self.session_factory()

        record = session.query(Record).filter(Record.key == key).one()
        record.is_checked = True

        session.add(record)
        session.commit()
        session.close()

    def set_unchecked(self, key: str) -> None:
        session = self.session_factory()

        record = session.query(Record).filter(Record.key == key).one()
        record.is_checked = False

        session.add(record)
        session.commit()
        session.close()

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

        backup_storage = Storage(path=path)
        for key, (value, is_checked) in self.items():
            backup_storage[key] = value
            if is_checked:
                backup_storage.set_checked(key=key)
            else:
                backup_storage.set_unchecked(key=key)

    def keys(self) -> List[str]:
        session = self.session_factory()

        keys = []
        for record in session.query(Record).order_by(
            asc(Record.id)
        ):  # TODO: retrieve id only
            keys.append(record.key)

        session.close()

        return keys

    def items(self) -> List[Tuple[str, Tuple[str, bool]]]:
        session = self.session_factory()

        items = [
            (record.key, (record.value, record.is_checked))
            for record in session.query(Record).order_by(Record.id)
        ]

        session.close()

        return items

    def clear(self) -> None:
        for key in self.keys():
            self.__delitem__(key=key)


class Repository:
    def __init__(self, path: str):
        self.storage: Storage = Storage(path=path)
        self.backup_path = None

    def __getitem__(self, key: str) -> Optional[str]:
        value = self.storage[key]

        return value

    def __setitem__(self, key: str, value: str) -> None:
        if not self.backup_path:
            self.backup()

        self.storage[key] = value

    def __delitem__(self, key: str) -> None:
        if not self.backup_path:
            self.backup()

        del self.storage[key]

    def __len__(self) -> int:
        return len(self.storage)

    @property
    def path(self) -> str:
        return self.storage.path

    def is_checked(self, key: str) -> bool:
        return self.storage.is_checked(key=key)

    def set_checked(self, key: str) -> None:
        self.storage.set_checked(key=key)

    def set_unchecked(self, key: str) -> None:
        self.storage.set_unchecked(key=key)

    def backup(self) -> None:
        backup_file = NamedTemporaryFile("w+")
        backup_path = backup_file.name
        backup_file.close()

        self.backup_path = backup_path
        self.storage.dump(path=self.backup_path)

    def restore(self) -> None:
        if not self.backup_path:
            return

        self.storage.clear()

        backup_storage = Storage(path=self.backup_path)
        for key, (value, is_checked) in backup_storage.items():
            self.storage[key] = value
            if is_checked:
                self.storage.set_checked(key=key)
            else:
                self.storage.set_unchecked(key=key)

        Path(self.backup_path).unlink(missing_ok=True)
        self.backup_path = None

    def load(self, path: str) -> None:
        self.storage = Storage(path=path)
        self.backup_path = None

    def save(self, path: Optional[str] = None) -> None:
        if not path:
            self.backup_path = None
            return

        destination = Path(path).resolve()
        source = Path(self.storage.path).resolve()

        shutil.copy(source, destination)

        self.storage.path = path

    def keys(self) -> List[str]:
        return self.storage.keys()

    def items(self) -> List[Tuple[str, Tuple[str, bool]]]:
        return self.storage.items()

    def commit_success_event(self, key: str) -> None:
        self.storage.commit_success_event(key=key)

    def commit_failure_event(self, key: str) -> None:
        self.storage.commit_failure_event(key=key)

    def commit_hint_event(self, key: str) -> None:
        self.storage.commit_hint_event(key=key)
