from pydantic import BaseSettings

class Settings(BaseSettings):
    database_host:str
    database_port:str
    database_user:str
    database_password:str
    database_name:str
    secret_key:str
    algorithm:str
    access_token_expire_time:int

    class Config:
        env_file=".env"

settings = Settings()
