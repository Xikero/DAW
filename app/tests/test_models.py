import unittest
from app.models import User, Incident
from datetime import datetime

class TestModels(unittest.TestCase):

    def test_user_set_password(self):
        user = User(username='testuser', email='test@example.com')
        user.set_password('Password123!')
        self.assertTrue(user.check_password('Password123!'))
        self.assertFalse(user.check_password('WrongPassword'))

    def test_incident_to_dict(self):
        incident = Incident(
            project='Madrid_T7',
            description='Descripción del incidente',
            position='Estructuras',
            responsible='Electrico',
            status='Abierto',
            created_by='testuser',
            created_at=datetime.utcnow()
        )
        incident_dict = incident.to_dict()
        self.assertEqual(incident_dict['project'], 'Madrid_T7')
        self.assertEqual(incident_dict['status'], 'Abierto')

if __name__ == '__main__':
    unittest.main()
