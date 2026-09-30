import os
from pydantic_settings import BaseSettings,SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR,".env")

class Settings(BaseSettings):
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str 
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int

    model_config = SettingsConfigDict(env_file=ENV_PATH)


settings = Settings()