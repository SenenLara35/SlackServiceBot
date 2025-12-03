from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import os

from .schemas import SlackMessageRequest
from .slack_client import send_message_to_slack

app = FastAPI(title="Servicio FastAPI Slack", version="1.0.0")

# --- 1. PRIMERO DEFINIMOS LA API (Para que tenga prioridad) ---

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/send-slack-message")
def send_slack_message(payload: SlackMessageRequest):
    result = send_message_to_slack(text=payload.text, channel=payload.channel)

    if not result["ok"]:
        raise HTTPException(status_code=500, detail=result["error"])

    return {
        "status": "sent",
        "channel": result["channel"],
        "ts": result["ts"]
    }

# --- 2. LUEGO MONTAMOS LA WEB (Como último recurso) ---
# Si la petición no coincide con la API de arriba, servirá el HTML.
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=static_path, html=True), name="static")