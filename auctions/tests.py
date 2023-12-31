from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.login_url = reverse('login')
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username='testuser', password='12345')

    def test_index_view(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)

    def test_login_view_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_view_POST(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_view_POST_no_data(self):
        response = self.client.post(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username and password are required.")
