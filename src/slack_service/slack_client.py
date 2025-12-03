from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from .config import settings

# Crea un cliente autenticado usando tu bot token
client = WebClient(token=settings.SLACK_BOT_TOKEN)

def send_message_to_slack(text: str, channel: str | None = None) -> dict:
    """
    Envía un mensaje a Slack y devuelve la respuesta de la API.
    """
    # Si channel es None, se usa el canal por defecto del .env
    if channel is None:
        channel = settings.SLACK_CHANNEL_ID

    try:
        # Esto hace una llamada real al endpoint de Slack
        response = client.chat_postMessage(
            channel=channel,
            text=text
        )
        return {"ok": True, "ts": response["ts"], "channel": response["channel"]}
    except SlackApiError as e:
        # Esto lo puedes loguear y devolver info útil
        error_msg = str(e)
        return {"ok": False, "error": error_msg}