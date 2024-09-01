from app import create_app, db
import unittest
from app.models import User, Incident
from flask import url_for
from config import TestingConfig

class TestRoutes(unittest.TestCase):

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

    def login(self):
        """Función auxiliar para iniciar sesión en la aplicación."""
        with self.app.test_request_context('/'):
            return self.client.post(url_for('main.login'), data={
                'email': 'test@example.com',
                'password': 'Password123!'
            }, follow_redirects=True)

    def test_index_route_requires_login(self):
        """Prueba que la ruta de índice requiera autenticación."""
        with self.app.test_request_context('/'):
            response = self.client.get(url_for('main.index'))
            self.assertEqual(response.status_code, 302)  # Redirige a la página de login
            self.assertIn(url_for('main.login'), response.location)

    def test_successful_login(self):
        """Prueba un inicio de sesión exitoso."""
        response = self.login()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testuser', response.data)

    def test_register_route(self):
        """Prueba el registro de un nuevo usuario."""
        with self.app.test_request_context('/'):
            response = self.client.post(url_for('main.register'), data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'NewPassword123!',
                'confirm_password': 'NewPassword123!'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Bienvenid@, newuser!', response.data)  # Cambiar por un texto seguro de la página

    def test_dashboard_route(self):
        """Prueba que la ruta del dashboard sea accesible después de iniciar sesión."""
        self.login()
        with self.app.test_request_context('/'):
            response = self.client.get(url_for('main.dashboard'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incidencias', response.data)  # Cambiar 'Dashboard' por 'Incidencias'

    def test_register_incident(self):
        """Prueba el registro de un nuevo incidente."""
        self.login()
        with self.app.test_request_context('/'):
            response = self.client.post(url_for('main.register_incident'), data={
                'project': 'Madrid_T7',
                'description': 'Nueva incidencia',
                'position': 'Estructuras',
                'responsible': 'Electrico',
                'status': 'Abierto'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incidencias', response.data)  # Cambiar por un texto seguro de la página

if __name__ == '__main__':
    unittest.main()
