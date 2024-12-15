# backend/api/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime

class APIConnectionTests(APITestCase):
    def setUp(self):
        """Set up data used in the tests"""
        self.test_url = reverse('test')
        self.login_url = reverse('login')
        self.valid_email = "test@gmu.edu"
        self.invalid_email = "test@gmail.com"
        self.password = "testpassword123"
        self.test_data = {
            'testData': 'Test message',
            'timestamp': '2024-03-18T12:00:00Z'
        }

    def test_get_endpoint_status(self):
        """Test the GET endpoint returns correct status"""
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'connected')

    def test_get_endpoint_method(self):
        """Test the GET endpoint returns correct method"""
        response = self.client.get(self.test_url)
        self.assertEqual(response.data['method'], 'GET')

    def test_get_endpoint_timestamp(self):
        """Test the GET endpoint returns a valid timestamp"""
        response = self.client.get(self.test_url)
        self.assertIn('timestamp', response.data)

    def test_get_endpoint_test_data(self):
        """Test the GET endpoint returns correct test data structure"""
        response = self.client.get(self.test_url)
        test_data = response.data['test_data']
        self.assertEqual(test_data['number'], 42)
        self.assertEqual(test_data['list'], [1, 2, 3])
        self.assertEqual(test_data['nested'], {'key': 'value'})

    def test_post_endpoint_success(self):
        """Test successful POST request to test endpoint"""
        response = self.client.post(self.test_url, self.test_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'received')
        self.assertEqual(response.data['method'], 'POST')
        self.assertEqual(response.data['received_data'], self.test_data)

    def test_post_endpoint_empty_data(self):
        """Test POST request with empty data"""
        response = self.client.post(self.test_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['received_data'], {})

    def test_post_endpoint_null_data(self):
        """Test POST request with null data"""
        response = self.client.post(self.test_url, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['received_data'], {})  # Django REST framework converts null to empty dict

# class LoginAPITests(APITestCase):
#     def setUp(self):
#         """Set up data used in the tests"""
#         self.login_url = reverse('login')
#         self.valid_email = "test@gmu.edu"
#         self.invalid_email = "test@gmail.com"
#         self.password = "testpassword123"

#     def test_login_success(self):
#         """Test successful login with valid GMU email"""
#         data = {
#             'email': self.valid_email,
#             'password': self.password
#         }
#         response = self.client.post(self.login_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['status'], 'success')
#         self.assertEqual(response.data['email'], self.valid_email)

#     def test_login_invalid_email_domain(self):
#         """Test login with non-GMU email domain"""
#         data = {
#             'email': self.invalid_email,
#             'password': self.password
#         }
#         response = self.client.post(self.login_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('email', response.data)

#     def test_login_missing_email(self):
#         """Test login with missing email"""
#         data = {
#             'password': self.password
#         }
#         response = self.client.post(self.login_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('email', response.data)

#     def test_login_missing_password(self):
#         """Test login with missing password"""
#         data = {
#             'email': self.valid_email
#         }
#         response = self.client.post(self.login_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('password', response.data)

#     def test_login_empty_request(self):
#         """Test login with empty request body"""
#         response = self.client.post(self.login_url, {}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('email', response.data)
#         self.assertIn('password', response.data)

#     def test_login_invalid_email_format(self):
#         """Test login with invalid email format"""
#         data = {
#             'email': 'invalid-email',
#             'password': self.password
#         }
#         response = self.client.post(self.login_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn('email', response.data)

# class URLTests(APITestCase):
#     def test_test_url_resolves(self):
#         """Test that test URL pattern resolves correctly"""
#         url = reverse('test')
#         self.assertEqual(url, '/api/test/')

#     def test_login_url_resolves(self):
#         """Test that login URL pattern resolves correctly"""
#         url = reverse('login')
#         self.assertEqual(url, '/api/login/')