import json
from pathlib import Path
from typing import Dict

from pandas import DataFrame, read_sql_table
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

from core.repository import DeclarativeBase


class Adapter:
    def __init__(self, engine: Engine = None) -> None:
        self.engine = engine or create_engine("sqlite:///:memory:")

    def create_tables(self) -> None:
        DeclarativeBase.metadata.create_all(bind=self.engine)

    def drop_tables(self) -> None:
        DeclarativeBase.metadata.drop_all(bind=self.engine)

    def load(self, path: str) -> bool:
        self.drop_tables()
        self.create_tables()

        if not Path(path).exists():
            return False

        with open(path, "r") as file:
            data = json.load(file)

        self.content = data

        return True

    def dump(self, path: str) -> None:
        with open(path, "w+") as file:
            json.dump(self.content, file, indent=4, default=str)

    @property
    def content(self) -> Dict:
        data = {}
        for table in (table.name for table in DeclarativeBase.metadata.sorted_tables):
            payload = read_sql_table(
                table_name=table,
                con=self.engine,
            ).to_dict(orient="records")
            if payload:
                payload = json.dumps(payload, default=str)  #
                payload = json.loads(payload)  #

                data.update({table: payload})

        return data

    @content.setter
    def content(self, data: Dict) -> None:
        self.drop_tables()
        self.create_tables()

        for table, payload in data.items():
            if not payload:
                continue

            DataFrame(payload).to_sql(
                name=table, con=self.engine, index=False, if_exists="append"
            )
