from flask import url_for
import unittest
from app import create_app, db
from config import TestingConfig
from app.models import User, Incident  # Import your models

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        # Create all database tables
        db.create_all()

        # Optionally, add a test user to the database
        test_user = User(username='testuser', email='test@example.com')
        test_user.set_password('password')
        db.session.add(test_user)
        db.session.commit()

        # Login before tests
        self.client.post(url_for('main.login'), data={
            'email': 'test@example.com',
            'password': 'password'
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_incident_creation(self):
        response = self.client.post(url_for('main.register_incident'), data={
            'project': 'Test Project',
            'description': 'Test Description',
            'position': 'Test Position',
            'responsible': 'Test Responsible',
            'status': 'Abierto'
        }, follow_redirects=True)
        
        # Verifica que la solicitud se completó correctamente
        self.assertEqual(response.status_code, 200)
        
        # Verifica que la redirección al dashboard fue exitosa o que el proyecto aparece en la lista de incidencias
        self.assertIn(b'Test Project', response.data)



    def test_dashboard_access(self):
        response = self.client.get('/dashboard')
        self.assertIn(b'Incidencias', response.data)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Iniciar Sesi\xc3\xb3n', response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
