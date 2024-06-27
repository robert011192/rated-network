from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    The settings used in the application.
    """
    # DB
    DATABASE: str = "api_requests.db"

    def sql_alchemy_uri(self) -> str:
        """URI to database"""
        return f"sqlite:///{self.DATABASE}"

    class Config:
        """Pydantic config"""

        env_file = ".env"


settings = Settings()
