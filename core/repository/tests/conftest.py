from pathlib import Path

from pytest import fixture

from core.repository.repositories import Storage


@fixture
def db():
    here = Path(__file__).parent.resolve()
    original = here / "fixtures/boost.db"

    repository = Storage(path=str(Path(original).resolve()))

    repository["foo"] = "1"
    repository["bar"] = "2"
