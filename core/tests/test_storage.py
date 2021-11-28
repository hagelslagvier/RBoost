from core.repository.storage import Storage


def test_if_can_read_from_storage():
    storage = Storage(path="../tests/test_data/data.json")

    foo_meaning = storage["foo_expression"]
    bar_meaning = storage["bar_expression"]

    assert (foo_meaning, bar_meaning) == ("foo_meaning", "bar_meaning")


def test_if_can_write_to_storage():
    storage = Storage(path="../tests/test_data/data.json")

    storage["baz_expression"] = "baz_meaning"

    baz_meaning = storage["baz_expression"]

    assert baz_meaning == "baz_meaning"
