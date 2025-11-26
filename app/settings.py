from pydantic import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://api.aipipe.ai/v1"
    MODEL_NAME: str = "gpt-4o-mini"
    VALID_SECRETS: str = "change-me"
    MAX_EXECUTION_SECONDS: int = 180
    MAX_PAYLOAD_BYTES: int = 1_000_000
    PLAYWRIGHT_HEADLESS: bool = True
    ALLOW_FOLLOW_CHAIN: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
