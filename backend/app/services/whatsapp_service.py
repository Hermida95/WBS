import requests
import json
from typing import Optional
from app.core.config import settings

class WhatsAppService:
    def __init__(self):
        self.base_url = f"https://graph.facebook.com/v17.0/{settings.WHATSAPP_PHONE_NUMBER_ID}"
        self.headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
    
    async def send_text_message(self, to: str, message: str) -> bool:
        """Enviar mensaje de texto a WhatsApp"""
        url = f"{self.base_url}/messages"
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message}
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Error enviando mensaje: {e}")
            return False
    
    async def send_button_message(self, to: str, text: str, buttons: list) -> bool:
        """Enviar mensaje con botones"""
        url = f"{self.base_url}/messages"
        
        button_components = []
        for i, button in enumerate(buttons):
            button_components.append({
                "type": "reply",
                "reply": {
                    "id": f"btn_{i}",
                    "title": button
                }
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": text},
                "action": {"buttons": button_components}
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Error enviando mensaje con botones: {e}")
            return False

# Instancia global del servicio
whatsapp_service = WhatsAppService()
