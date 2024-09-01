# run.py

# Importar la función create_app desde el paquete app
from app import create_app

# Crear una instancia de la aplicación Flask usando la fábrica de aplicaciones
app = create_app()

# Ejecutar la aplicación solo si este script se ejecuta directamente
if __name__ == '__main__':
    # Ejecutar la aplicación en modo de depuración
    app.run(debug=True)
