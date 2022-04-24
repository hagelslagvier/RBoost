import shutil
from pathlib import Path

from core.repository.storage import Repository


def test_if_doesnt_make_backup_on_getitem():
    here = Path(__file__).parent.resolve()
    original = here / "fixtures/boost.db"

    repository = Repository(path=str(Path(original).resolve()))

    assert repository.is_dirty is False
    assert repository.backup_storage is None

    assert repository["foo"] == "1"
    assert repository["bar"] == "2"
    assert repository.is_dirty is False
    assert repository.backup_storage is None


def test_if_can_backup_and_restore_on_setitem():
    here = Path(__file__).parent.resolve()
    original = here / "fixtures/boost.db"
    copied = here / "fixtures/copied.db"

    shutil.copy(original, copied)

    repository = Repository(path=str(Path(copied).resolve()))

    assert repository["foo"] == "1"
    assert repository["bar"] == "2"
    assert repository.is_dirty is False
    assert repository.backup_storage is None
    assert repository.main_storage.keys() == ["foo", "bar"]
    assert repository.main_storage.items() == [("foo", "1"), ("bar", "2")]

    repository["baz"] = "3"

    assert repository["baz"] == "3"
    assert repository.is_dirty is True
    assert repository.backup_storage is not None
    assert repository.backup_storage.keys() == ["foo", "bar"]
    assert repository.backup_storage.items() == [("foo", "1"), ("bar", "2")]
    assert repository.main_storage.keys() == ["foo", "bar", "baz"]
    assert repository.main_storage.items() == [("foo", "1"), ("bar", "2"), ("baz", "3")]

    repository.restore()

    assert repository.is_dirty is False
    assert repository.backup_storage is None
    assert repository.main_storage.keys() == ["foo", "bar"]
    assert repository.main_storage.items() == [("foo", "1"), ("bar", "2")]

    copied.unlink(missing_ok=True)


def test_if_can_backup_and_restore_on_delitem():
    here = Path(__file__).parent.resolve()
    original = here / "fixtures/boost.db"
    copied = here / "fixtures/copied.db"

    shutil.copy(original, copied)

    repository = Repository(path=str(Path(copied).resolve()))

    assert repository["foo"] == "1"
    assert repository["bar"] == "2"
    assert repository.is_dirty is False
    assert repository.backup_storage is None
    assert repository.main_storage.keys() == ["foo", "bar"]
    assert repository.main_storage.items() == [("foo", "1"), ("bar", "2")]

    del repository["bar"]

    assert repository.is_dirty is True
    assert repository.backup_storage is not None
    assert repository.backup_storage.keys() == ["foo", "bar"]
    assert repository.backup_storage.items() == [("foo", "1"), ("bar", "2")]
    assert repository.main_storage.keys() == ["foo"]
    assert repository.main_storage.items() == [("foo", "1")]

    repository.restore()

    assert repository.is_dirty is False
    assert repository.backup_storage is None
    assert repository.main_storage.keys() == ["foo", "bar"]
    assert repository.main_storage.items() == [("foo", "1"), ("bar", "2")]

    copied.unlink(missing_ok=True)
