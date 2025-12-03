from fastapi import FastAPI, HTTPException
from .schemas import SlackMessageRequest
from .slack_client import send_message_to_slack

app = FastAPI(
    title="Servicio FastAPI Slack",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    """Endpoint para monitoreo."""
    return {"status": "ok"}

@app.post("/send-slack-message")
def send_slack_message(payload: SlackMessageRequest):
    # Se pasa la información validada al cliente de Slack
    result = send_message_to_slack(text=payload.text, channel=payload.channel)

    # Si Slack responde "ok": False, se lanza un error HTTP 500
    if not result["ok"]:
        raise HTTPException(status_code=500, detail=result["error"])

    return {
        "status": "sent",
        "channel": result["channel"],
        "ts": result["ts"]
    }