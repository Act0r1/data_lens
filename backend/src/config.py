from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/datalens"
    secret_key: str = "change-me-in-production"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

    s3_endpoint: str = "https://storage.yandexcloud.net"
    s3_bucket: str = "datalens"
    s3_access_key: str = ""
    s3_secret_key: str = ""
    s3_region: str = "ru-central1"

    yandex_gpt_api_key: str = ""
    yandex_gpt_folder_id: str = ""
    yandex_gpt_model: str = "yandexgpt/latest"

    max_upload_size_mb: int = 100

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
