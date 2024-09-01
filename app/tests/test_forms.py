import unittest
from config import TestingConfig
from app.models import User, db
from app import create_app  # Usamos create_app que ya definiste en app/__init__.py
from app.forms import RegistrationForm, LoginForm, IncidentForm

class TestForms(unittest.TestCase):

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

    def test_registration_form_valid_data(self):
        with self.app.test_request_context('/'):
            form = RegistrationForm(
                username='testuser',
                email='test@example.com',
                password='Password123!',
                confirm_password='Password123!'
            )
            is_valid = form.validate()
            if not is_valid:
                print(form.errors)
            self.assertTrue(is_valid)

    def test_registration_form_invalid_email(self):
        with self.app.test_request_context('/'):
            form = RegistrationForm(
                username='testuser',
                email='invalid-email',
                password='Password123!',
                confirm_password='Password123!'
            )
            self.assertFalse(form.validate())

    def test_login_form_valid_data(self):
        with self.app.test_request_context('/'):
            form = LoginForm(
                email='test@example.com',
                password='Password123!'
            )
            self.assertTrue(form.validate())

    def test_incident_form_valid_data(self):
        with self.app.test_request_context('/'):
            form = IncidentForm(
                project='Madrid_T7',
                description='Descripción del incidente',
                position='Estructuras',
                responsible='Electrico',
                status='Abierto'
            )
            self.assertTrue(form.validate())

    def test_incident_form_missing_data(self):
        with self.app.test_request_context('/'):
            form = IncidentForm(
                project='Madrid_T7',
                description='',  # Falta la descripción
                position='Estructuras',
                responsible='Electrico',
                status='Abierto'
            )
            self.assertFalse(form.validate())

if __name__ == '__main__':
    unittest.main()
