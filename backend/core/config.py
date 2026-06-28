from pydantic_settings import BaseSettings, SettingsConfigDict
from pprint import pprint
print("works")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str

    MAIL_FROM: str

    MAIL_SERVER: str
    MAIL_PORT: str = '587'

    MAIL_STARTTLS: str = 'True'
    MAIL_SSL_TLS: str = 'False'

    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

settings = Settings()
pprint(settings.model_dump())
