from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    frontend_origin: str = "http://localhost:3100"
    database_url: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/flytrain"
    )
    # Claude API 키는 서버에만 둔다. 비어 있으면 해설·코치 기능을 끈다.
    anthropic_api_key: str = ""
    # 전처리된 커넥톰 하위 회로가 있는 곳 (connectome/ 스크립트가 만든다)
    connectome_dir: str = "../data/processed"


settings = Settings()
