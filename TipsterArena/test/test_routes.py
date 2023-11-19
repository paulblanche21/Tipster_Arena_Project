# tests/test_routes.py

import unittest
from .. import create_app


class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_route_not_logged_in(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # expecting a redirect since user is not logged in

# More tests...
    def test_login_route(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register_route(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_logout_route(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_subscriptions_route(self):
        response = self.client.get('/subscriptions')
        self.assertEqual(response.status_code, 302)

    def test_chat_route(self):
        response = self.client.get('/chat')
        self.assertEqual(response.status_code, 302)

    def test_sports_route(self):
        response = self.client.get('/sports')
        self.assertEqual(response.status_code, 302)

    def test_about_route(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_contact_route(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)

    def test_privacy_policy_route(self):
        response = self.client.get('/privacy-policy')
        self.assertEqual(response.status_code, 200)

    def test_terms_and_conditions_route(self):
        response = self.client.get('/terms-and-conditions')
        self.assertEqual(response.status_code, 200)
    
    def test_reset_password_route(self):
        response = self.client.get('/reset-password')
        self.assertEqual(response.status_code, 200)
    
    def test_reset_password_request_route(self):
        response = self.client.get('/reset-password-request')
        self.assertEqual(response.status_code, 200)
    
