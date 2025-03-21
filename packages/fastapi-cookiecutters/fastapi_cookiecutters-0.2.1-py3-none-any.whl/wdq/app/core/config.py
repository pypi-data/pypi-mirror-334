from pydantic_settings import BaseSettings, SettingsConfigDict


pg_user = os.getenv("POSTGRES_USER", "user")
pg_password = os.getenv("POSTGRES_PASSWORD", "password")
pg_host = os.getenv("POSTGRES_HOST", "localhost")
pg_database = os.getenv("POSTGRES_DB", "my_fastapi_project")


class Settings(BaseSettings):
    APP_NAME: str = "my_fastapi_project"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str =  f"postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}/{pg_database}"
    
    
    REDIS_URL: str = "redis://localhost:6379/0"
    

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()