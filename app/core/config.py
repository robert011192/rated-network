from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    The settings used in the application.
    """
    PROJECT_NAME: str = "Rated Log Parser"
    # DB
    DATABASE: str = "/app/app/processor/api_requests.db"

    def sql_alchemy_uri(self) -> str:
        """URI to database"""
        return f"sqlite:///{self.DATABASE}"

    class Config:
        """Pydantic config"""

        env_file = ".env"


settings = Settings()
