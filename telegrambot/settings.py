from pydantic import BaseModel
import os



class BotSettings(BaseModel):
    backend_url: str = os.getenv("backend_url")
    token: str = os.getenv("token")

settings = BotSettings()