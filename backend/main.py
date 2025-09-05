from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.models.whatsapp import WhatsAppWebhook
from app.services.chatbot import chatbot
import json
import sys

# Arreglar encoding UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Crear la instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="Sistema de Agendado de Citas por WhatsApp",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "¡WhatsApp Booking System está funcionando!",
        "app_name": settings.APP_NAME,
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}

# Webhook de verificación de WhatsApp
@app.get("/webhook")
async def verify_webhook(request: Request):
    """Verificar webhook de WhatsApp"""
    query_params = dict(request.query_params)
    
    mode = query_params.get("hub.mode")
    token = query_params.get("hub.verify_token")
    challenge = query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN:
        print("✅ Webhook verificado correctamente")
        return int(challenge)
    else:
        print("❌ Error en verificación de webhook")
        raise HTTPException(status_code=403, detail="Forbidden")

# Webhook para recibir mensajes de WhatsApp
@app.post("/webhook")
async def receive_webhook(webhook: WhatsAppWebhook):
    """Recibir mensajes de WhatsApp"""
    
    try:
        for entry in webhook.entry:
            for change in entry.changes:
                if change.field == "messages":
                    value = change.value
                    
                    # Procesar mensajes entrantes
                    if "messages" in value:
                        for message in value["messages"]:
                            # Extraer información del mensaje
                            phone_number = message.get("from")
                            message_type = message.get("type")
                            
                            if message_type == "text":
                                text_body = message.get("text", {}).get("body", "")
                                
                                print(f"📱 Mensaje recibido de {phone_number}: {text_body}")
                                
                                # Procesar mensaje con el chatbot
                                await chatbot.process_message(phone_number, text_body)
                            
                            elif message_type == "interactive":
                                # Manejar respuestas de botones
                                interactive = message.get("interactive", {})
                                button_reply = interactive.get("button_reply", {})
                                button_text = button_reply.get("title", "")
                                
                                print(f"🔘 Botón presionado por {phone_number}: {button_text}")
                                
                                # Procesar respuesta de botón
                                await chatbot.process_message(phone_number, button_text)
        
        return {"status": "success"}
    
    except Exception as e:
        print(f"❌ Error procesando webhook: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
