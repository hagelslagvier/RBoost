from pathlib import Path
from typing import Dict

from sqlalchemy import asc

from core.repository.models import Event, Record
from core.repository.repository import Storage


def _format_event(event: Event) -> Dict:
    return {
        "id": event.id,
        "event_type": event.event_type.name,
        "record_id": event.record_id,
    }


def _format_record(record: Record) -> Dict:
    return {
        "id": record.id,
        "key": record.key,
        "value": record.value,
        "is_checked": record.is_checked,
        "events": [_format_event(event=event) for event in record.events],
    }


def test_if_can_create_storage():
    here = Path(__file__).parent.resolve()
    path = here / "fixtures/new_boost.db"

    Storage(path=str(path))
    try:
        assert Path(path).is_file()

    finally:
        Path(path).unlink(missing_ok=True)


def test_if_can_get_item():
    storage = Storage()

    session = storage.session_factory()
    records = session.query(Record).all()
    assert records == []
    assert storage.keys() == []
    assert storage["foo"] is None

    record = Record(key="foo", value="bar", is_checked=True)
    session.add(record)
    session.commit()

    records = [_format_record(record=record) for record in session.query(Record).all()]
    assert records == [
        {"events": [], "id": 1, "key": "foo", "value": "bar", "is_checked": True}
    ]
    assert storage.keys() == ["foo"]
    assert storage["foo"] == "bar"
    assert storage.is_checked(key="foo") is True


def test_if_can_set_item():
    storage = Storage()

    session = storage.session_factory()
    records = session.query(Record).all()
    assert records == []
    assert storage.keys() == []
    assert storage["foo"] is None

    storage["foo"] = "bar"

    records = [_format_record(record=record) for record in session.query(Record).all()]
    assert records == [
        {"events": [], "id": 1, "key": "foo", "value": "bar", "is_checked": True}
    ]
    assert storage.keys() == ["foo"]
    assert storage["foo"] == "bar"
    assert storage.is_checked(key="foo") is True

    storage.set_unchecked(key="foo")
    assert storage.is_checked(key="foo") is False

    storage.set_checked(key="foo")
    assert storage.is_checked(key="foo") is True


def test_if_can_del_item():
    storage = Storage()
    storage["foo"] = "bar"
    storage["spam"] = "eggs"

    session = storage.session_factory()
    records = [
        _format_record(record=record)
        for record in session.query(Record).order_by(asc(Record.id)).all()
    ]
    assert records == [
        {"id": 1, "key": "foo", "value": "bar", "is_checked": True, "events": []},
        {"id": 2, "key": "spam", "value": "eggs", "is_checked": True, "events": []},
    ]
    assert storage.keys() == ["foo", "spam"]

    del storage["spam"]

    records = [
        _format_record(record=record)
        for record in session.query(Record).order_by(asc(Record.id)).all()
    ]
    assert records == [
        {"id": 1, "key": "foo", "value": "bar", "is_checked": True, "events": []},
    ]
    assert storage.keys() == ["foo"]


def test_if_can_commit_success_event():
    storage = Storage()

    session = storage.session_factory()
    records = session.query(Record).all()
    events = session.query(Event).all()

    assert records == []
    assert events == []

    storage["foo"] = "bar"
    storage.commit_success_event(key="foo")

    records = [
        _format_record(record=record)
        for record in session.query(Record).order_by(asc(Record.id)).all()
    ]
    assert records == [
        {
            "id": 1,
            "key": "foo",
            "value": "bar",
            "is_checked": True,
            "events": [{"id": 1, "event_type": "SUCCESS", "record_id": 1}],
        }
    ]

    events = [
        _format_event(event=event)
        for event in session.query(Event).order_by(asc(Event.id)).all()
    ]
    assert events == [{"id": 1, "event_type": "SUCCESS", "record_id": 1}]


def test_if_can_commit_hint_event():
    storage = Storage()

    session = storage.session_factory()
    records = session.query(Record).all()
    events = session.query(Event).all()

    assert records == []
    assert events == []

    storage["foo"] = "bar"
    storage.commit_hint_event(key="foo")

    records = [
        _format_record(record=record)
        for record in session.query(Record).order_by(asc(Record.id)).all()
    ]
    assert records == [
        {
            "events": [{"event_type": "HINT", "id": 1, "record_id": 1}],
            "id": 1,
            "key": "foo",
            "value": "bar",
            "is_checked": True,
        }
    ]

    events = [
        _format_event(event=event)
        for event in session.query(Event).order_by(asc(Event.id)).all()
    ]
    assert events == [{"event_type": "HINT", "id": 1, "record_id": 1}]


def test_if_can_commit_failure_event():
    storage = Storage()

    session = storage.session_factory()
    records = session.query(Record).all()
    events = session.query(Event).all()

    assert records == []
    assert events == []

    storage["foo"] = "bar"
    storage.commit_failure_event(key="foo")

    records = [
        _format_record(record=record)
        for record in session.query(Record).order_by(asc(Record.id)).all()
    ]
    assert records == [
        {
            "events": [{"event_type": "FAILURE", "id": 1, "record_id": 1}],
            "id": 1,
            "key": "foo",
            "value": "bar",
            "is_checked": True,
        }
    ]

    events = [
        _format_event(event=event)
        for event in session.query(Event).order_by(asc(Event.id)).all()
    ]
    assert events == [{"event_type": "FAILURE", "id": 1, "record_id": 1}]


def test_if_can_return_keys():
    storage = Storage()

    assert storage.keys() == []

    storage["foo"] = "1"
    storage["bar"] = "2"
    storage["baz"] = "3"

    assert storage.keys() == ["foo", "bar", "baz"]


def test_if_can_return_items():
    storage = Storage()

    assert storage.keys() == []

    storage["foo"] = "1"
    storage["bar"] = "2"
    storage["baz"] = "3"

    assert storage.items() == [("foo", "1"), ("bar", "2"), ("baz", "3")]


def test_if_can_clear_items():
    storage = Storage()

    assert storage.keys() == []

    storage["foo"] = "1"
    storage["bar"] = "2"
    storage["baz"] = "3"

    assert storage.items() == [("foo", "1"), ("bar", "2"), ("baz", "3")]

    storage.clear()

    assert storage.keys() == []
    assert storage.items() == []
