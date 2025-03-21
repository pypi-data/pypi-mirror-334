from expat.config import MySQLConfig
from expat.db.drivers.driver import Driver

from pymysql import Connection, connect

from types import TracebackType
from typing import Self, Type, final


@final
class MySQLDriver(Driver):
    config: MySQLConfig
    connection: Connection

    def __enter__(self) -> Self:
        self.connection = connect(
            host=self.config.host,
            user=self.config.user,
            password=self.config.password.get_secret_value(),
            port=self.config.port,
            **self.config.options,
        )
        return self

    def __exit__(
        self,
        exception_type: Type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exception is not None:
            self.connection.rollback()

        else:
            self.connection.commit()

        self.connection.close()

    def create_expat_tables(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                    CREATE SCHEMA expat;
                """
            )

    def destroy_expat_tables(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                    DROP SCHEMA expat;
                """
            )
