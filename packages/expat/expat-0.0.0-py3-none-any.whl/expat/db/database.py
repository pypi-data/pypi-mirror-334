from expat.config import Config, DBConfig
from expat.db.drivers import Driver, MySQLDriver, PostgresDriver

from pydantic import BaseModel

from typing import Self, Type


class Database(BaseModel):
    config: DBConfig
    driver_class: Type[Driver]

    @classmethod
    def from_config(cls: Type[Self], config: Config) -> Self:
        match config.database_type:
            case "postgres":
                return cls(config=config.database, driver_class=PostgresDriver)
            case "mysql":
                return cls(config=config.database, driver_class=MySQLDriver)

    def initialize(self):
        with self.driver_class(self.config) as driver:
            driver.create_expat_tables()

    def destroy(self):
        with self.driver_class(self.config) as driver:
            driver.destroy_expat_tables()
