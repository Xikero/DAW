from app import create_app, db
from app.models import Incident

# Crear una instancia de la aplicación Flask
app = create_app()

# Ejecutar dentro del contexto de la aplicación
with app.app_context():
    # Verificar si la tabla 'incident' existe en la base de datos
    if not db.engine.has_table('incident'):
        # Crear todas las tablas definidas en los modelos
        db.create_all()
        print("Table 'incident' created successfully.")
    else:
        print("Table 'incident' already exists.")
