from app import create_app, db
from sqlalchemy import text

# Crear una aplicación y contexto de aplicación
app = create_app()
with app.app_context():
    # Conexión a la base de datos
    connection = db.engine.connect()

    # Consultar las columnas de la tabla 'user'
    user_columns_query = text("PRAGMA table_info(user);")
    result_user = connection.execute(user_columns_query)
    user_columns = [row[1] for row in result_user]  # Usar índices en lugar de nombres
    print("Columns in 'user' table:", user_columns)

    # Consultar las columnas de la tabla 'incident'
    incident_columns_query = text("PRAGMA table_info(incident);")
    result_incident = connection.execute(incident_columns_query)
    incident_columns = [row[1] for row in result_incident]  # Usar índices en lugar de nombres
    print("Columns in 'incident' table:", incident_columns)

    # Cerrar la conexión
    connection.close()
