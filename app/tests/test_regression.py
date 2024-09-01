import sys
import os
import unittest
from app import create_app, db
from app.models import User, Incident
from config import TestingConfig

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

class RegressionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Crear un usuario de prueba
        self.test_user = User(username='testuser', email='testuser@example.com')
        self.test_user.set_password('testpassword')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self):
        return self.client.post('/login', data={
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)

    def test_create_incident(self):
        self.login()
        response = self.client.post('/register_incident', data={
            'project': 'TestProject',
            'description': 'Test description',
            'position': 'Test position',
            'responsible': 'IT',
            'status': 'Abierto'
        }, follow_redirects=True)
        
        # Verifica que el incidente fue agregado a la tabla
        self.assertIn(b'TestProject', response.data)
        self.assertIn(b'Test description', response.data)

    def test_homepage_access(self):
        # Intenta acceder a la página de inicio sin autenticarse
        response = self.client.get('/', follow_redirects=True)
        
        # Verifica si la redirección fue a la página de login
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Iniciar Sesi\xc3\xb3n', response.data)

    def test_user_login(self):
        response = self.login()
        self.assertIn(b'Bienvenid@', response.data)

    def test_user_registration(self):
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)
        self.assertIn(b'Bienvenid@', response.data)

if __name__ == '__main__':
    unittest.main()
