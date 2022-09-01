from typing import List
import sqlalchemy as sa
from aiogram.utils.executor import Executor
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import DateTime, Column
from data import config

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db.func.now())
    updated_at = Column(DateTime(True),
                        default=db.func.now(),
                        onupdate=db.func.now(),
                        server_default=db.func.now())


async def on_startup():

    import socket
    h_name = socket.gethostname()
    IP_addres = socket.gethostbyname(h_name)
    print("Host Name is:" + h_name)
    print("Computer IP Address is:" + IP_addres)
    print("Установка связи с PostgreSQL")
    await db.set_bind(config.POSTGRES_URL)
    print("Готов1")
    await db.gino.drop_all()
    db.gino: GinoSchemaVisitor
    print("Готов2")
    await db.gino.create_all()


def setup(executor: Executor):
    executor.on_startup(on_startup)
