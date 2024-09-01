import unittest
from config import TestingConfig
from app import create_app, db
from app.models import User, Incident

class TestAcceptance(unittest.TestCase):

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
        return self.client.post('/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def test_user_registration_flow(self):
        """Prueba el flujo completo de registro de usuario y confirmación."""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'NewPassword123!',
            'confirm_password': 'NewPassword123!'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenid@, newuser!', response.data)  # Verificar que el usuario llegue al perfil

        # Simular la redirección a la página principal
        response = self.client.get('/index', follow_redirects=True)
        self.assertIn(b'Registrar Incidencia', response.data)  # Verificar que "Registrar Incidencia" está presente

    def test_user_login_flow(self):
        """Prueba el flujo completo de inicio de sesión y acceso al dashboard."""
        response = self.login('test@example.com', 'Password123!')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bienvenid@, testuser!', response.data)  # Verificar que el usuario llegue al perfil

        # Simular la redirección al dashboard
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Incidencias', response.data)  # Verificar que "Incidencias" está presente

    def test_create_incident_via_ui(self):
        """Prueba la creación de una incidencia a través de la interfaz de usuario."""
        self.login('test@example.com', 'Password123!')
        response = self.client.post('/register_incident', data={
            'project': 'Madrid_T7',
            'description': 'Incidencia UAT',
            'position': 'Estructuras',
            'responsible': 'Electrico',
            'status': 'Abierto'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incidencias', response.data)
        self.assertIn(b'Incidencia UAT', response.data)

        # Verificar que la incidencia aparezca en el dashboard
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incidencia UAT', response.data)

if __name__ == '__main__':
    unittest.main()
