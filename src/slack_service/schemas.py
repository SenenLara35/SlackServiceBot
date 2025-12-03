from pydantic import BaseModel, Field

class SlackMessageRequest(BaseModel):
    text: str = Field(..., description="Mensaje que se enviará a Slack")
    channel: str | None = Field(
        default=None,
        description="ID del canal de Slack. Si no se envía, se usa el canal por defecto."
    )