from django.test import TestCase
from ..models import User


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The home page loads properly"""
        response = self.client.get('your_server_ip:8000')
        self.assertEqual(response.status_code, 404)
