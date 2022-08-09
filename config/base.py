from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str
    SERVER_PORT: int
    SERVER_IP: str


    class Config:
        env_file = '.env'
