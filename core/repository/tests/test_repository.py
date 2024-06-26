import shutil
from pathlib import Path

from core.repository.repositories import Repository, Storage


def test_if_doesnt_make_backup_on_getitem(db):
    here = Path(__file__).parent.resolve()
    original = here / "fixtures/boost.db"

    repository = Repository(path=str(Path(original).resolve()))

    assert repository.backup_path is None

    assert repository["foo"] == "1"
    assert repository["bar"] == "2"
    assert repository.backup_path is None


def test_if_can_backup_and_restore_on_setitem():
    here = Path(__file__).parent.resolve()
    original = here / "fixtures/boost.db"
    copied = here / "fixtures/copied.db"

    shutil.copy(original, copied)

    repository = Repository(path=str(Path(copied).resolve()))

    assert repository["foo"] == "1"
    assert repository["bar"] == "2"
    assert repository.backup_path is None
    assert repository.storage.keys() == ["foo", "bar"]
    assert repository.storage.items() == [("foo", ("1", True)), ("bar", ("2", True))]

    repository["baz"] = "3"

    assert repository["baz"] == "3"
    assert repository.backup_path is not None

    backup_storage = Storage(path=repository.backup_path)

    assert backup_storage.keys() == ["foo", "bar"]
    assert backup_storage.items() == [("foo", ("1", True)), ("bar", ("2", True))]
    assert repository.storage.keys() == ["foo", "bar", "baz"]
    assert repository.storage.items() == [
        ("foo", ("1", True)),
        ("bar", ("2", True)),
        ("baz", ("3", True)),
    ]

    repository.restore()

    assert repository.backup_path is None
    assert repository.storage.keys() == ["foo", "bar"]
    assert repository.storage.items() == [("foo", ("1", True)), ("bar", ("2", True))]

    copied.unlink(missing_ok=True)


def test_if_can_backup_and_restore_on_delitem():
    here = Path(__file__).parent.resolve()
    original = here / "fixtures/boost.db"
    copied = here / "fixtures/copied.db"

    shutil.copy(original, copied)

    repository = Repository(path=str(Path(copied).resolve()))

    assert repository["foo"] == "1"
    assert repository["bar"] == "2"
    assert repository.backup_path is None
    assert repository.storage.keys() == ["foo", "bar"]
    assert repository.storage.items() == [("foo", ("1", True)), ("bar", ("2", True))]

    del repository["bar"]

    assert repository.backup_path is not None

    backup_storage = Storage(path=repository.backup_path)

    assert backup_storage.keys() == ["foo", "bar"]
    assert backup_storage.items() == [("foo", ("1", True)), ("bar", ("2", True))]
    assert repository.storage.keys() == ["foo"]
    assert repository.storage.items() == [("foo", ("1", True))]

    repository.restore()

    assert repository.backup_path is None
    assert repository.storage.keys() == ["foo", "bar"]
    assert repository.storage.items() == [("foo", ("1", True)), ("bar", ("2", True))]

    copied.unlink(missing_ok=True)
