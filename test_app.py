import unittest
from app import app, db

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        response = self.client.post('/auth/register', json={"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        self.client.post('/auth/register', json={"username": "testuser", "password": "testpass"})
        response = self.client.post('/auth/login', json={"username": "testuser", "password": "testpass"})
        self.assertEqual(response.status_code, 200)

    def test_create_item(self):
        self.client.post('/auth/register', json={"username": "testuser", "password": "testpass"})
        response = self.client.post('/auth/login', json={"username": "testuser", "password": "testpass"})
        token = response.get_json()['token']
        response = self.client.post('/items', json={"name": "Item1", "description": "A test item"}, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()