import json

from sqlalchemy.engine.base import Engine
from pandas import DataFrame, read_sql_table


from core.repository import DeclarativeBase


class Adapter:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def drop_tables(self) -> None:
        DeclarativeBase.metadata.drop_all(bind=self.engine)

    def load(self, path: str) -> None:
        DeclarativeBase.metadata.create_all(bind=self.engine)

        try:
            with open(path, "r") as file:
                content = json.load(file)
        except FileNotFoundError:
            return

        for table, payload in content.items():
            if not payload:
                continue

            DataFrame(payload).to_sql(name=table, con=self.engine, index=False, if_exists="append")

    def dump(self, path: str) -> None:
        content = {}
        for table in (table.name for table in DeclarativeBase.metadata.sorted_tables):
            payload = read_sql_table(table_name=table, con=self.engine).to_dict(orient="records")
            if payload:
                content.update({table: payload})

        with open(path, "w") as file:
            json.dump(content, file, indent=4, default=str)
