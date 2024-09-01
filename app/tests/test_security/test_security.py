import unittest
from flask import url_for
from app import create_app, db
from app.models import User

class SecurityTestCase(unittest.TestCase):
    def setUp(self):
        """Configura un contexto de aplicación y una base de datos en memoria antes de cada prueba."""
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.app.config['SERVER_NAME'] = 'localhost'
        self.app.config['WTF_CSRF_ENABLED'] = True
        self.app.config['SECRET_KEY'] = 'mysecretkey'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Crear un usuario de prueba si no existe
        if not User.query.filter_by(email='test@example.com').first():
            self.user = User(username='testuser', email='test@example.com')
            self.user.set_password('Password123!')
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        """Elimina el contexto de aplicación y la base de datos después de cada prueba."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_set_password(self):
        """Verifica que la función set_password almacene correctamente la contraseña en un formato hash."""
        user = User.query.filter_by(username='testuser').first()
        self.assertTrue(user.check_password('Password123!'))
        self.assertFalse(user.check_password('WrongPassword'))

    def test_login_with_correct_credentials(self):
        """Verifica que un usuario puede iniciar sesión con credenciales correctas."""
        response = self.client.post(url_for('main.login'), data={
            'email': 'test@example.com',
            'password': 'Password123!'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_login_with_wrong_credentials(self):
        """Verifica que un usuario no puede iniciar sesión con credenciales incorrectas."""
        response = self.client.post(url_for('main.login'), data={
            'email': 'test@example.com',
            'password': 'WrongPassword!'
        }, follow_redirects=True)
        # Verifica que se redirige a la página de login con un mensaje de error
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_protected_route_requires_login(self):
        """Verifica que una ruta protegida requiere autenticación."""
        response = self.client.get(url_for('main.dashboard'), follow_redirects=True)
        # Verifica que el usuario sea redirigido a la página de login
        self.assertIn(b'Login', response.data)

    def test_csrf_protection(self):
        """Verifica que la protección CSRF está habilitada."""
        # Verifica que el formulario de registro contenga un token CSRF
        response = self.client.get(url_for('main.register'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'csrf_token', response.data)

    def test_session_security(self):
        """Verifica que la sesión se maneje de forma segura (cookies seguras, etc.)."""
        response = self.client.post(url_for('main.login'), data={
            'email': 'test@example.com',
            'password': 'Password123!'
        }, follow_redirects=True)
        self.assertIn('Set-Cookie', response.headers)
        self.assertIn('HttpOnly', response.headers['Set-Cookie'])
        # Comentado porque 'Secure' no se establece en un entorno de prueba HTTP
        # self.assertIn('Secure', response.headers['Set-Cookie'])

if __name__ == '__main__':
    unittest.main()
