import unittest
from app import create_app
from app.extensions import db

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])
        self.assertFalse(self.app.config['WTF_CSRF_ENABLED'])

    def test_database_uri(self):
        self.assertEqual(
            self.app.config['SQLALCHEMY_DATABASE_URI'],
            'sqlite:///:memory:'
        )

    def test_jwt_configuration(self):
        self.assertIsNotNone(self.app.config['JWT_SECRET_KEY'])
        self.assertNotEqual(
            self.app.config['JWT_SECRET_KEY'],
            'default secret key'
        )

if __name__ == '__main__':
    unittest.main()