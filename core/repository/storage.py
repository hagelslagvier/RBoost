from typing import Optional, List

from core.repository import session, engine
from core.repository.adapter import Adapter
from core.repository.models import Record, Event, EventType


class Storage:
    def __init__(self, path: str):
        self.path = path

        self.adapter = Adapter(engine=engine)
        self.adapter.drop_tables()
        self.adapter.load(path=self.path)

    def __getitem__(self, key: str) -> Optional[str]:
        record = session.query(Record) \
            .filter(Record.expression == key) \
            .one_or_none()

        value = record.meaning if record else None

        return value

    def __setitem__(self, key: str, value: str) -> None:
        record = Record(expression=key, meaning=value)
        session.add(record)
        session.commit()

    def __delitem__(self, key: str) -> None:
        record = session.query(Record) \
            .filter(Record.expression == key) \
            .one()

        session.delete(record)
        session.commit()

    def _commit_event(self, expression: str, event_type: EventType):
        record = session.query(Record)\
            .filter(Record.expression == expression)\
            .one()

        event = Event(event_type=event_type, record=record)
        session.add(event)
        session.commit()

    def commit_success_event(self, expression):
        self._commit_event(expression=expression, event_type=EventType.SUCCESS)

    def commit_failure_event(self, expression):
        self._commit_event(expression=expression, event_type=EventType.FAILURE)

    def commit_hint_event(self, expression):
        self._commit_event(expression=expression, event_type=EventType.HINT)

    def all_expressions(self) -> List[str]:
        expressions = []
        for expression in session.query(Record.expression).all():
            expressions.append(expression)

        return expressions



if __name__ == "__main__":
    # et = EventType(type_name="success")
    # session.add(et)
    # session.commit()
    # print(et)
    #
    # et = EventType(type_name="failure")
    # session.add(et)
    # session.commit()
    # print(et)
    #
    # et = EventType(type_name="hint")
    # session.add(et)
    # session.commit()
    # print(et)

    # record = Record(expression="aaa3", meaning="bbb2")
    # session.add(record)
    # session.commit()
    # print(record)
    #
    shelf = Storage(path="../payload/data.json")

    shelf["foo_expression"] = "foo_meaning"
    shelf["bar_expression"] = "bar_meaning"


    shelf.commit_success_event(expression="foo_expression")
    shelf.commit_success_event(expression="foo_expression")

    shelf.commit_success_event(expression="bar_expression")
    shelf.commit_failure_event(expression="bar_expression")
    shelf.commit_hint_event(expression="bar_expression")

    # r = shelf["foo2"]
    # print(r)
    # r = shelf["foo3"]
    # print(r)

    # shelf["qux6"] = "qux2"
    # r = shelf["qux6"]
    # print(r)

    # shelf.commit_event(expression="foo", event_type=EventType.HINT)
    # shelf.commit_event(expression="foo", event_type=EventType.HINT)
    # shelf.commit_event(expression="foo", event_type=EventType.HINT)
    # shelf.commit_event(expression="foo", event_type=EventType.HINT)
    # shelf.commit_event(expression="foo", event_type=EventType.HINT)
    # shelf.commit_event(key="qux6", event_name="success")
    # shelf.commit_event(key="qux6", event_name="success")
    # shelf.commit_event(key="qux6", event_name="success")
    #
    #
    # shelf["zzz"] = "zzzz1"
    # shelf["yyy"] = "yyyy1"
    shelf.adapter.dump(path=shelf.path)



