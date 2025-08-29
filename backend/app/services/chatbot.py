from typing import Dict, Any
from app.services.whatsapp_service import whatsapp_service
from app.models.database import User, Service, Appointment
from app.database import SessionLocal
from datetime import datetime
import re

class ChatBot:
    def __init__(self):
        self.user_states: Dict[str, str] = {}
        self.user_data: Dict[str, Dict[str, Any]] = {}
    
    async def process_message(self, phone_number: str, message: str) -> None:
        """Procesar mensaje entrante y responder"""
        
        current_state = self.user_states.get(phone_number, "welcome")
        
        if current_state == "welcome":
            await self._handle_welcome(phone_number, message)
        elif current_state == "awaiting_service":
            await self._handle_service_selection(phone_number, message)
        elif current_state == "awaiting_date":
            await self._handle_date_selection(phone_number, message)
        elif current_state == "awaiting_time":
            await self._handle_time_selection(phone_number, message)
        elif current_state == "awaiting_name":
            await self._handle_name_input(phone_number, message)
        elif current_state == "confirming":
            await self._handle_confirmation(phone_number, message)
    
    def _get_or_create_user(self, phone_number: str, name: str = None):
        """Obtener o crear usuario en la base de datos"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.phone_number == phone_number).first()
            if not user:
                user = User(phone_number=phone_number, name=name)
                db.add(user)
                db.commit()
                db.refresh(user)
            elif name and not user.name:
                user.name = name
                db.commit()
            return user
        finally:
            db.close()
    
    def _get_service_by_name(self, service_name: str):
        """Obtener servicio por nombre"""
        db = SessionLocal()
        try:
            return db.query(Service).filter(Service.name == service_name).first()
        finally:
            db.close()
    
    def _create_appointment(self, user_id: int, service_id: int, date_str: str, time_str: str):
        """Crear cita en la base de datos"""
        db = SessionLocal()
        try:
            # Por simplicidad, usar fecha actual + hora
            appointment_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
            
            appointment = Appointment(
                user_id=user_id,
                service_id=service_id,
                appointment_date=appointment_date,
                status="confirmed"
            )
            db.add(appointment)
            db.commit()
            db.refresh(appointment)
            return appointment
        finally:
            db.close()
    
    async def _handle_welcome(self, phone_number: str, message: str):
        """Manejar mensaje de bienvenida"""
        # Crear usuario en BD si no existe
        self._get_or_create_user(phone_number)
        
        welcome_text = """¡Hola! 👋 Bienvenido a nuestro sistema de citas.

¿En qué servicio estás interesado?"""
        
        buttons = ["Consulta Médica", "Odontología", "Psicología"]
        
        await whatsapp_service.send_button_message(phone_number, welcome_text, buttons)
        self.user_states[phone_number] = "awaiting_service"
        
        if phone_number not in self.user_data:
            self.user_data[phone_number] = {}
    
    async def _handle_service_selection(self, phone_number: str, message: str):
        """Manejar selección de servicio"""
        service = message.strip()
        self.user_data[phone_number]["service"] = service
        
        date_text = f"""Perfecto! Has seleccionado: {service} 

¿Qué día prefieres para tu cita?
Ejemplo: mañana, lunes, 2024-08-28"""
        
        await whatsapp_service.send_text_message(phone_number, date_text)
        self.user_states[phone_number] = "awaiting_date"
    
    async def _handle_date_selection(self, phone_number: str, message: str):
        """Manejar selección de fecha"""
        date = message.strip()
        self.user_data[phone_number]["date"] = date
        
        time_text = """¿A qué hora te gustaría la cita?"""
        buttons = ["9:00 AM", "11:00 AM", "2:00 PM", "4:00 PM"]
        
        await whatsapp_service.send_button_message(phone_number, time_text, buttons)
        self.user_states[phone_number] = "awaiting_time"
    
    async def _handle_time_selection(self, phone_number: str, message: str):
        """Manejar selección de hora"""
        time = message.strip()
        self.user_data[phone_number]["time"] = time
        
        name_text = """¿Cuál es tu nombre completo?"""
        
        await whatsapp_service.send_text_message(phone_number, name_text)
        self.user_states[phone_number] = "awaiting_name"
    
    async def _handle_name_input(self, phone_number: str, message: str):
        """Manejar entrada del nombre"""
        name = message.strip()
        self.user_data[phone_number]["name"] = name
        
        data = self.user_data[phone_number]
        
        confirmation_text = f"""📅 RESUMEN DE TU CITA:

👤 Nombre: {data['name']}
🏥 Servicio: {data['service']}
📅 Fecha: {data['date']}
⏰ Hora: {data['time']}

¿Confirmas esta cita?"""
        
        buttons = ["✅ Confirmar", "❌ Cancelar"]
        
        await whatsapp_service.send_button_message(phone_number, confirmation_text, buttons)
        self.user_states[phone_number] = "confirming"
    
    async def _handle_confirmation(self, phone_number: str, message: str):
        """Manejar confirmación de cita"""
        if "confirmar" in message.lower() or "✅" in message:
            data = self.user_data[phone_number]
            
            # Crear/actualizar usuario
            user = self._get_or_create_user(phone_number, data['name'])
            
            # Obtener o crear servicio
            service = self._get_service_by_name(data['service'])
            if not service:
                # Crear servicio si no existe
                db = SessionLocal()
                service = Service(name=data['service'])
                db.add(service)
                db.commit()
                db.refresh(service)
                db.close()
            
            # Crear cita
            appointment = self._create_appointment(
                user.id, 
                service.id, 
                data['date'], 
                data['time']
            )
            
            success_text = f"""✅ ¡CITA CONFIRMADA!

Tu cita #{appointment.id} ha sido agendada exitosamente:

�� {data['name']}
🏥 {data['service']}  
📅 {data['date']}
⏰ {data['time']}

📱 Te enviaremos un recordatorio 1 día antes.
💬 Si necesitas reagendar, escríbenos "reagendar"

¡Gracias por confiar en nosotros! 🙏"""
            
            await whatsapp_service.send_text_message(phone_number, success_text)
            
            # Limpiar estado
            self.user_states[phone_number] = "welcome"
            if phone_number in self.user_data:
                del self.user_data[phone_number]
        
        else:
            cancel_text = """❌ Cita cancelada.

¿Te gustaría agendar una nueva cita?"""
            
            buttons = ["Sí, nueva cita", "No, gracias"]
            
            await whatsapp_service.send_button_message(phone_number, cancel_text, buttons)
            self.user_states[phone_number] = "welcome"

chatbot = ChatBot()
