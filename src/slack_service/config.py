from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SLACK_BOT_TOKEN: str
    SLACK_SIGNING_SECRET: str
    SLACK_CHANNEL_ID: str

    class Config:
        env_file = ".env"
        # Esto indica que las variables se leen del archivo .env
        # además de las variables de entorno del sistema.

settings = Settings()
# Imprimimos para verificar (según el PDF [cite: 288])
print("Canal ID CARGADO:", settings.SLACK_CHANNEL_ID)