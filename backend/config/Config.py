from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ssh_host: str
    ssh_port: int = 22
    ssh_user: str
    ssh_pasword: str | None = None

    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_name: str
    db_user: str
    db_password: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="UTF-8")

Settings = Settings()