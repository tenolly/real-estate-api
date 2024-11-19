from pydantic_settings import BaseSettings


class Config(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_TEST_DB: str

    class Config:
        env_file = ".env"
