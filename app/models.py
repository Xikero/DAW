from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Clase de modelo para los usuarios
class User(db.Model, UserMixin):
    # Definición de las columnas de la tabla 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Método para establecer la contraseña del usuario
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Método para verificar la contraseña del usuario
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Clase de modelo para los incidentes
class Incident(db.Model):
    # Definición de las columnas de la tabla 'incident'
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(100))
    description = db.Column(db.String(200))
    position = db.Column(db.String(100))
    responsible = db.Column(db.String(100))
    status = db.Column(db.String(50))
    created_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Método para convertir el objeto en un diccionario
    def to_dict(self):
        return {
            'id': self.id,
            'project': self.project,
            'description': self.description,
            'position': self.position,
            'responsible': self.responsible,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at
        }
