import unittest
from app import app, db
from models import User

class TestApp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Configurar la aplicación para las pruebas
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()
    
    @classmethod
    def tearDownClass(cls):
        # Limpiar la base de datos después de las pruebas
        db.session.remove()
        db.drop_all()
    
    def setUp(self):
        # Crear datos de prueba antes de cada prueba individual
        user1 = User(name='Test User 1', email='test1@example.com', password='password1')
        user2 = User(name='Test User 2', email='test2@example.com', password='password2')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
    
    def tearDown(self):
        # Limpiar datos de prueba después de cada prueba individual
        User.query.delete()
        db.session.commit()
    
    def test_get_users(self):
        with app.test_client() as client:
            response = client.get('/users')
            data = response.json
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 2)  # Verificar que se devuelvan todos los usuarios
    
    def test_get_user(self):
        with app.test_client() as client:
            response = client.get('/users/1')
            data = response.json
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['name'], 'Test User 1')
    
    def test_create_user(self):
        with app.test_client() as client:
            new_user_data = {'name': 'New User', 'email': 'newuser@example.com', 'password': 'newpassword'}
            response = client.post('/users', json=new_user_data)
            data = response.json
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['name'], 'New User')
            self.assertEqual(data['email'], 'newuser@example.com')
    
    def test_update_user(self):
        with app.test_client() as client:
            updated_user_data = {'name': 'Updated User', 'email': 'updateduser@example.com', 'password': 'updatedpassword'}
            response = client.put('/users/1', json=updated_user_data)
            data = response.json
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['name'], 'Updated User')
            self.assertEqual(data['email'], 'updateduser@example.com')
    
    def test_delete_user(self):
        with app.test_client() as client:
            response = client.delete('/users/1')
            data = response.json
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'User deleted')

if __name__ == '__main__':
    unittest.main()
