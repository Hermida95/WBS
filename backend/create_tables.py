from app.models.database import Base
from app.database import engine

# Crear todas las tablas
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente")
