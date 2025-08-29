from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Crear la instancia de FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="Sistema de Agendado de Citas por WhatsApp",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
