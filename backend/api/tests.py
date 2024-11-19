# api/tests.py
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class APIConnectionTests(APITestCase):
    def test_get_endpoint(self):
        """Test the GET endpoint of the API"""
        url = reverse('test')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'connected')
        self.assertEqual(response.data['method'], 'GET')
        self.assertIn('timestamp', response.data)
        self.assertIn('test_data', response.data)
        
    def test_post_endpoint(self):
        """Test the POST endpoint of the API"""
        url = reverse('test')
        test_data = {
            'testData': 'Test message',
            'timestamp': '2024-03-18T12:00:00Z'
        }
        
        response = self.client.post(url, test_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'received')
        self.assertEqual(response.data['method'], 'POST')
        self.assertEqual(response.data['received_data'], test_data)