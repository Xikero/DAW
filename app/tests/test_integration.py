import unittest
from app import create_app, db
from config import TestingConfig
from app.models import User, Incident
from flask import url_for

class TestIntegration(unittest.TestCase):

    def setUp(self):
        """Configura un contexto de aplicación y una base de datos en memoria antes de cada prueba."""
        self.app = create_app(config_class=TestingConfig)  # Asegurarse de usar la configuración de pruebas
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Crear un usuario de prueba
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('Password123!')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Elimina el contexto de aplicación y la base de datos después de cada prueba."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, email, password):
        """Función auxiliar para iniciar sesión en la aplicación."""
        with self.app.test_request_context('/'):
            return self.client.post(url_for('main.login'), data={
                'email': email,
                'password': password
            }, follow_redirects=True)

    def test_register_and_login(self):
        """Prueba un flujo completo de registro y login."""
        with self.app.test_request_context('/'):
            # 1. Registro de un nuevo usuario
            response = self.client.post('/register', data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'NewPassword123!',
                'confirm_password': 'NewPassword123!'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Bienvenid@, newuser!', response.data)
        
            # 2. Iniciar sesión con el nuevo usuario
            response = self.login('newuser@example.com', 'NewPassword123!')
            self.assertEqual(response.status_code, 200)
            # Asegúrate de que el texto esté en bytes y codificado correctamente
            self.assertIn('Sistema de Gestión de Incidencias.'.encode('utf-8'), response.data)
    
    def test_create_and_view_incident(self):
        """Prueba la creación y visualización de una incidencia."""
        with self.app.test_request_context('/'):
            # Iniciar sesión con el usuario de prueba
            self.login('test@example.com', 'Password123!')
        
            # 1. Registrar un incidente
            response = self.client.post('/register_incident', data={
                'project': 'Madrid_T7',
                'description': 'Incidencia de prueba',
                'position': 'Estructuras',
                'responsible': 'Electrico',
                'status': 'Abierto'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incidencias', response.data)
        
            # 2. Verificar que el incidente se registró correctamente en la base de datos
            incident = Incident.query.filter_by(description='Incidencia de prueba').first()
            self.assertIsNotNone(incident)
            self.assertEqual(incident.project, 'Madrid_T7')
        
            # 3. Verificar que el incidente aparece en el dashboard
            response = self.client.get('/dashboard')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incidencia de prueba', response.data)

if __name__ == '__main__':
    unittest.main()
