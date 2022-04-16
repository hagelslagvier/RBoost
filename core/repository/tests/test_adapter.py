import json
from pathlib import Path
from unittest.mock import call, patch

from core.repository import DeclarativeBase
from core.repository.adapter import Adapter
from core.repository.events import EventType
from core.repository.models import Event, Record
from pytest import raises
from sqlalchemy import asc, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import sessionmaker


def test_if_can_create_adapter():
    url = make_url("sqlite:///:memory:")
    engine = create_engine(url=url)

    adapter = Adapter(engine=engine)
    assert adapter.engine is engine

    adapter = Adapter()
    assert isinstance(adapter.engine, Engine)
    assert adapter.engine.url == url


def test_if_can_drop_tables():
    with patch("core.repository.adapter.DeclarativeBase") as mock:
        adapter = Adapter()
        adapter.drop_tables()

        assert mock.mock_calls == [call.metadata.drop_all(bind=adapter.engine)]


def test_if_can_load_content_when_data_file_exists():
    adapter = Adapter()
    adapter.load(path="./fixtures/data.json")

    session_factory = sessionmaker(bind=adapter.engine)
    session = session_factory()

    records = []
    for record in session.query(Record).order_by(asc(Record.id)):
        item = {
            "id": record.id,
            "created_on": str(record.created_on),
            "updated_on": str(record.updated_on),
            "expression": record.expression,
            "meaning": record.meaning,
        }

        records.append(item)

    assert records == [
        {
            "id": 1,
            "created_on": "2022-04-16 12:54:24.671922",
            "expression": "foo_expression",
            "meaning": "foo_meaning",
            "updated_on": "2022-04-16 12:54:24.671928",
        },
        {
            "id": 2,
            "created_on": "2022-04-16 12:54:24.672691",
            "expression": "bar_expression",
            "meaning": "bar_meaning",
            "updated_on": "2022-04-16 12:54:24.672695",
        },
        {
            "id": 3,
            "created_on": "2022-04-16 12:54:24.673138",
            "expression": "baz_expression",
            "meaning": "bar_meaning",
            "updated_on": "2022-04-16 12:54:24.673141",
        },
    ]

    events = []
    for event in session.query(Event).order_by(asc(Event.id)):
        item = {
            "id": event.id,
            "created_on": str(event.created_on),
            "updated_on": str(event.updated_on),
            "event_type": event.event_type.value,
            "record": {
                "id": event.record.id,
                "created_on": str(event.record.created_on),
                "updated_on": str(event.record.updated_on),
                "expression": event.record.expression,
                "meaning": event.record.meaning,
            },
        }

        events.append(item)

    assert events == [
        {
            "id": 1,
            "created_on": "2022-04-16 12:54:24.676669",
            "updated_on": "2022-04-16 12:54:24.676672",
            "event_type": "SUCCESS",
            "record": {
                "id": 1,
                "created_on": "2022-04-16 12:54:24.671922",
                "updated_on": "2022-04-16 12:54:24.671928",
                "expression": "foo_expression",
                "meaning": "foo_meaning",
            },
        },
        {
            "id": 2,
            "created_on": "2022-04-16 12:54:24.677945",
            "updated_on": "2022-04-16 12:54:24.677948",
            "event_type": "SUCCESS",
            "record": {
                "id": 1,
                "created_on": "2022-04-16 12:54:24.671922",
                "updated_on": "2022-04-16 12:54:24.671928",
                "expression": "foo_expression",
                "meaning": "foo_meaning",
            },
        },
        {
            "id": 3,
            "created_on": "2022-04-16 12:54:24.678942",
            "updated_on": "2022-04-16 12:54:24.678945",
            "event_type": "SUCCESS",
            "record": {
                "id": 2,
                "created_on": "2022-04-16 12:54:24.672691",
                "updated_on": "2022-04-16 12:54:24.672695",
                "expression": "bar_expression",
                "meaning": "bar_meaning",
            },
        },
        {
            "id": 4,
            "created_on": "2022-04-16 12:54:24.679934",
            "updated_on": "2022-04-16 12:54:24.679938",
            "event_type": "FAILURE",
            "record": {
                "id": 2,
                "created_on": "2022-04-16 12:54:24.672691",
                "updated_on": "2022-04-16 12:54:24.672695",
                "expression": "bar_expression",
                "meaning": "bar_meaning",
            },
        },
        {
            "id": 5,
            "created_on": "2022-04-16 12:54:24.680927",
            "updated_on": "2022-04-16 12:54:24.680930",
            "event_type": "HINT",
            "record": {
                "id": 2,
                "created_on": "2022-04-16 12:54:24.672691",
                "updated_on": "2022-04-16 12:54:24.672695",
                "expression": "bar_expression",
                "meaning": "bar_meaning",
            },
        },
        {
            "id": 6,
            "created_on": "2022-04-16 12:54:24.681943",
            "updated_on": "2022-04-16 12:54:24.681946",
            "event_type": "HINT",
            "record": {
                "id": 3,
                "created_on": "2022-04-16 12:54:24.673138",
                "updated_on": "2022-04-16 12:54:24.673141",
                "expression": "baz_expression",
                "meaning": "bar_meaning",
            },
        },
        {
            "id": 7,
            "created_on": "2022-04-16 12:54:24.682933",
            "updated_on": "2022-04-16 12:54:24.682936",
            "event_type": "HINT",
            "record": {
                "id": 3,
                "created_on": "2022-04-16 12:54:24.673138",
                "updated_on": "2022-04-16 12:54:24.673141",
                "expression": "baz_expression",
                "meaning": "bar_meaning",
            },
        },
    ]


def test_if_raises_exception_when_data_file_not_exist():
    with raises(FileNotFoundError):
        adapter = Adapter()
        adapter.load(path="./fixtures/nonexistent.json")


def test_if_can_dump_content():
    adapter = Adapter()

    DeclarativeBase.metadata.create_all(bind=adapter.engine)

    session_factory = sessionmaker(bind=adapter.engine)
    session = session_factory()

    records = [
        Record(expression="spam1", meaning="eggs1"),
        Record(expression="spam2", meaning="eggs2"),
    ]

    events = [
        Event(event_type=EventType.SUCCESS, record=records[0]),
        Event(event_type=EventType.HINT, record=records[1]),
    ]

    session.add_all(records + events)
    session.commit()

    file_path = Path(__file__).resolve().parent / "fixtures" / "tmp.json"

    adapter.dump(path=str(file_path))

    with open(str(file_path), "r") as file:
        data = json.load(file)

    assert data == {
        "records": [
            {
                "id": records[0].id,
                "created_on": str(records[0].created_on),
                "updated_on": str(records[0].updated_on),
                "expression": records[0].expression,
                "meaning": records[0].meaning,
            },
            {
                "id": records[1].id,
                "created_on": str(records[1].created_on),
                "updated_on": str(records[1].updated_on),
                "expression": records[1].expression,
                "meaning": records[1].meaning,
            },
        ],
        "events": [
            {
                "id": events[0].id,
                "created_on": str(events[0].created_on),
                "updated_on": str(events[0].updated_on),
                "event_type": events[0].event_type.value,
                "record_id": events[0].record_id,
            },
            {
                "id": events[1].id,
                "created_on": str(events[1].created_on),
                "updated_on": str(events[1].updated_on),
                "event_type": events[1].event_type.value,
                "record_id": events[1].record_id,
            },
        ],
    }

    file_path.unlink()
