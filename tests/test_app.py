import unittest
from app.app import app, db
from app.models import User

class TestApp(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        cls.app = app
        cls.client = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()
    
    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        user1 = User(name='Test User 1', email='test1@example.com', password='password1')
        user2 = User(name='Test User 2', email='test2@example.com', password='password2')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
    
    def tearDown(self):
        User.query.delete()
        db.session.commit()
        self.app_context.pop()
    
    def test_get_users(self):
        response = self.client.get('/users')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)
    
    def test_get_user(self):
        response = self.client.get('/users/1')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Test User 1')
    
    def test_create_user(self):
        new_user_data = {'name': 'New User', 'email': 'newuser@example.com', 'password': 'newpassword'}
        response = self.client.post('/users', json=new_user_data)
        data = response.json
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], 'New User')
        self.assertEqual(data['email'], 'newuser@example.com')
    
    def test_update_user(self):
        updated_user_data = {'name': 'Updated User', 'email': 'updateduser@example.com', 'password': 'updatedpassword'}
        response = self.client.put('/users/1', json=updated_user_data)
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Updated User')
        self.assertEqual(data['email'], 'updateduser@example.com')
    
    def test_delete_user(self):
        response = self.client.delete('/users/1')
        data = response.json
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'User deleted')

if __name__ == '__main__':
    unittest.main()
