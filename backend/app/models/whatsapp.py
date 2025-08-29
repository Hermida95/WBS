from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Modelos para recibir mensajes de WhatsApp
class WhatsAppContact(BaseModel):
    profile: Optional[Dict[str, Any]] = None
    wa_id: str

class WhatsAppText(BaseModel):
    body: str

class WhatsAppMessage(BaseModel):
    from_: str = Field(alias='from')
    id: str
    timestamp: str
    text: Optional[WhatsAppText] = None
    type: str

class WhatsAppChange(BaseModel):
    field: str
    value: Dict[str, Any]

class WhatsAppEntry(BaseModel):
    id: str
    changes: List[WhatsAppChange]

class WhatsAppWebhook(BaseModel):
    object: str
    entry: List[WhatsAppEntry]

# Modelos para enviar mensajes
class WhatsAppTextMessage(BaseModel):
    messaging_product: str = "whatsapp"
    to: str
    type: str = "text"
    text: Dict[str, str]

class WhatsAppButtonMessage(BaseModel):
    messaging_product: str = "whatsapp"
    to: str
    type: str = "interactive"
    interactive: Dict[str, Any]
