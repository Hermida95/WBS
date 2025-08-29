from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    # Configuración de la aplicación
    APP_NAME: str = "WhatsApp Booking System"
    DEBUG: bool = True
    ENVIRONMENT: Optional[str] = "development"
    
    # Configuración de base de datos
    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str] = None
    
    # Configuración de seguridad
    SECRET_KEY: str = "your-secret-key-here"
    JWT_SECRET_KEY: Optional[str] = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de Redis
    REDIS_URL: Optional[str] = None
    
    # Configuración de WhatsApp Business API
    WHATSAPP_ACCESS_TOKEN: Optional[str] = None
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = None
    WHATSAPP_WEBHOOK_VERIFY_TOKEN: Optional[str] = None
    WHATSAPP_WEBHOOK_SECRET: Optional[str] = None
    
    # Configuración de Google
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    
    # Configuración de Stripe
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    
    # Configuración de SendGrid
    SENDGRID_API_KEY: Optional[str] = None
    FROM_EMAIL: Optional[str] = None
    
    # Configuración de Sentry
    SENTRY_DSN: Optional[str] = None
    
    # Configuración de CORS y Frontend
    CORS_ORIGINS: Optional[str] = None
    FRONTEND_URL: Optional[str] = "http://localhost:3000"
    
    # Configuración de zona horaria y límites
    DEFAULT_TIMEZONE: Optional[str] = "Europe/Madrid"
    MAX_APPOINTMENTS_PER_DAY: Optional[int] = 50
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instancia global de configuración
settings = Settings()
