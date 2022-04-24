from pathlib import Path
from core.repository.storage import Storage

import uuid


def test_if_can_create_storage():
    here = Path(__file__).parent.resolve()
    path = here / "fixtures/new_boost.db"

    Storage(path=str(path))
    try:
        assert Path(path).is_file()

    finally:
        Path(path).unlink(missing_ok=True)


def test_if_can_get_item():
    here = Path(__file__).parent.resolve()
    path = here / "fixtures/boost.db"

    storage = Storage(path=str(path))

    assert storage["foo"] == "bar"


def test_if_can_set_item():
    here = Path(__file__).parent.resolve()
    file_name = str(uuid.uuid4())
    path = here / f"fixtures/{file_name}.db"

    storage = Storage(path=str(path))
    storage["spam"] = "eggs"

    try:
        assert storage["spam"] == "eggs"

    finally:
        Path(path).unlink(missing_ok=True)


def test_if_can_del_item():
    here = Path(__file__).parent.resolve()
    file_name = str(uuid.uuid4())
    path = here / f"fixtures/{file_name}.db"

    storage = Storage(path=str(path))
    storage["spam"] = "eggs"

    try:
        assert "spam" in storage.keys()

        del storage["spam"]

        assert "spam" not in storage.keys()

    finally:
        Path(path).unlink(missing_ok=True)


def test_if_can_commit_success_event():
    
