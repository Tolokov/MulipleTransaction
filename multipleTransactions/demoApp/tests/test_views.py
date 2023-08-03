from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from ..models import Profile
from ..views import *
from rest_framework.test import APIRequestFactory


class TestView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user_one = User.objects.create_user(username='testuser5', password='15321')
        self.one = Profile.objects.create(
            user=self.user_one, full_name="User number One", inn="1010101010", wallet=100.0)

    def test_url_ProfileListAPIView(self):
        view = ProfileListAPIView.as_view()
        request = self.factory.get('', {'title': 'new idea'})
        response = view(request)
        response.render()
        self.assertEqual(response.content,
                         b'[{"user":"testuser5","full_name":"User number One","inn":"1010101010","wallet":"100.00"}]')
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('', {'title': 'new idea'})
        response = view(request)
        response.render()
        self.assertEqual(response.status_code, 405)

    def test_url_ProfileCreateAPIView(self):
        view = ProfileCreateAPIView.as_view()
        request = self.factory.post('/add/', {'title': 'new idea'})
        response = view(request).render()
        self.assertEqual(response.status_code, 400)

