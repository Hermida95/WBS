# WBS - WhatsApp Booking SaaS

Sistema SaaS de gestión de citas vía WhatsApp para profesionales y pequeñas empresas.

## 🚀 Características

- **Multi-tenant**: Un sistema, múltiples clientes
- **WhatsApp Integration**: Recibe y gestiona citas por WhatsApp
- **Google Calendar**: Sincronización automática
- **Stripe Payments**: Sistema de suscripciones
- **Dashboard**: Panel de control para cada negocio
- **API REST**: FastAPI + SQLAlchemy
- **Escalable**: PostgreSQL + Redis + Celery

## 🏗️ Arquitectura

```
WBS/
├── backend/          # FastAPI + PostgreSQL
├── frontend/         # Dashboard (React/Vue)
├── landing/          # Landing page para ventas
├── docs/            # Documentación
└── infrastructure/  # Docker, configs
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Alembic
- **Database**: PostgreSQL + Redis
- **Auth**: JWT multi-tenant
- **Payments**: Stripe
- **Integrations**: WhatsApp Business API, Google Calendar
- **Deploy**: Railway/Heroku
- **Monitoring**: Sentry

## 🔧 Setup para Desarrollo

```bash
# Clonar proyecto
git clone https://github.com/tu-usuario/wbs.git
cd wbs

# Setup backend
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar base de datos
createdb wbs_dev
alembic upgrade head

# Ejecutar
uvicorn app.main:app --reload
```

## 📦 Variables de Entorno

Copia `.env.example` a `.env` y configura:

- `DATABASE_URL`: PostgreSQL connection
- `WHATSAPP_ACCESS_TOKEN`: WhatsApp Business token
- `STRIPE_SECRET_KEY`: Stripe payments
- `GOOGLE_CLIENT_ID`: Google Calendar API

## 🚀 Deployment

```bash
# Deploy a Railway
railway login
railway link
railway up
```

## 📊 Modelo de Negocio

- **Básico**: €29/mes - 100 citas/mes
- **Pro**: €59/mes - 500 citas/mes  
- **Enterprise**: €99/mes - Ilimitado

## 🎯 Target Market

Profesionales locales que reciben citas:
- Clínicas dentales
- Consultas médicas
- Salones de belleza
- Despachos de abogados
- Centros de fisioterapia

## 📈 Roadmap

- [x] MVP Backend API
- [x] WhatsApp Integration
- [ ] Dashboard Frontend
- [ ] Stripe Integration
- [ ] Google Calendar Sync
- [ ] Landing Page
- [ ] Deploy Production

## 📄 License

Proprietary - Todos los derechos reservados