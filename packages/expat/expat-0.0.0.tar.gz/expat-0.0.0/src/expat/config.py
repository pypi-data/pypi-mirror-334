from pydantic import (
    BaseModel,
    BeforeValidator,
    SecretStr,
    TypeAdapter,
    model_validator,
)
from pydantic_settings import (
    BaseSettings,
    InitSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

import logging
import os
from typing import Annotated, Any, Generic, Literal, Type, TypeVar
from urllib.parse import urlencode


logger = logging.getLogger(__name__)


ExpandableString = Annotated[str, BeforeValidator(lambda s: os.path.expandvars(s))]
LogLevel = Literal["critical", "error", "warning", "info", "debug"]
DBType = Literal["postgres", "mysql"]


class DBConfig(BaseModel): ...


class PostgresConfig(DBConfig):
    host: str
    port: int
    database: str
    user: str
    password: SecretStr
    options: dict[str, str] = {}

    @property
    def connection_string(self) -> str:
        if self.options is not None:
            options_string = f"?{urlencode(self.options)}"
        else:
            options_string = ""

        return (
            f"postgresql://{self.user}:"
            f"{self.password.get_secret_value()}@{self.host}:"
            f"{self.port}/{self.database}{options_string}"
        )


class MySQLConfig(DBConfig):
    host: str
    port: int
    user: str
    password: SecretStr
    options: dict[str, Any] = {}


class LogConfig(BaseModel):
    log_level: LogLevel

    @property
    def python_log_level(self) -> str:
        return self.log_level.upper()


T = TypeVar("T", bound=DBConfig)


class Config(BaseSettings, Generic[T]):
    config_file: ExpandableString | None
    logs: LogConfig
    database_type: DBType
    database: T

    model_config = SettingsConfigDict()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: InitSettingsSource,
        **kwargs,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        toml_file = init_settings.init_kwargs.get("config_file", "expat.toml")

        toml_settings = TomlConfigSettingsSource(settings_cls, toml_file)

        return (init_settings, toml_settings)

    @model_validator(mode="before")
    def set_database_config(cls, data: Any) -> Any:
        db_config = data["database"]

        if isinstance(db_config, dict):
            db_type: DBType = TypeAdapter(DBType).validate_python(db_config.pop("type"))

            match db_type:
                case "postgres":
                    data["database"] = PostgresConfig(**db_config)
                case "mysql":
                    data["database"] = MySQLConfig(**db_config)

            data["database_type"] = db_type

        return data
