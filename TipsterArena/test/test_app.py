import unittest
from flask import Flask
from app import create_app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_config(self):
        self.assertEqual(self.app.config['TESTING'], True)
        self.assertEqual(self.app.config['DEBUG'], False)

    def test_routes(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')

        response = self.client.get('/test-logging')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Logging test')

    def test_extensions_initialized(self):
        with self.app.app_context():
            self.assertIsNotNone(self.app.extensions['db'])
            self.assertIsNotNone(self.app.extensions['bcrypt'])
            self.assertIsNotNone(self.app.extensions['cors'])
            self.assertIsNotNone(self.app.extensions['csrf'])
            self.assertIsNotNone(self.app.extensions['migrate'])
            self.assertIsNotNone(self.app.extensions['socketio'])
            self.assertIsNotNone(self.app.extensions['login_manager'])

    def test_database_tables_created(self):
        with self.app.app_context():
            db = self.app.extensions['db']
            with self.app.test_request_context():
                db.create_all()
                self.assertTrue(db.engine.dialect.has_table(db.engine, 'table1'))
                self.assertTrue(db.engine.dialect.has_table(db.engine, 'table2'))
                # Add more assertions for other tables

if __name__ == '__main__':
    unittest.main()