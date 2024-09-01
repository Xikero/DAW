import os

class Config:
    # Clave secreta utilizada por Flask para la gestión de sesiones y la protección contra CSRF
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # URI de la base de datos SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    
    # Carpeta de cargas para almacenar archivos subidos por los usuarios
    UPLOAD_FOLDER = 'uploads'
    
    # Tamaño máximo permitido para las cargas de archivos (16 MB en este caso)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max 16 MB upload size

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Asegurarse de usar la base de datos en memoria
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost.localdomain'  # Agregar esto
