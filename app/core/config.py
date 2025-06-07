from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str 

    smtp_username: str
    app_password: str


    class Config:
        env_file = ".env"

settings = Settings()

