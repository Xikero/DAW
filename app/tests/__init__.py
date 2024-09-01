# tests/__init__.py

# Aquí podrías importar cosas comunes o configurar parámetros globales para tus pruebas.
import os
import sys

# Asegurarte de que el directorio raíz del proyecto esté en el sys.path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
