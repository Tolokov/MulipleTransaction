from django.test import TestCase
from django.contrib.auth.models import User
from ..views import *
from rest_framework.test import APIRequestFactory


class TestView(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user_one = User.objects.create_user(username='testuser1', password='15321')
        self.user_two = User.objects.create_user(username='testuser2', password='15321')

        self.one = Profile.objects.create(
            user=self.user_one, full_name="User number One", inn="1010101010", wallet=100.0)

    def test_url_ProfileListAPIView(self):
        view = ProfileListAPIView.as_view()
        request = self.factory.get('', {})

        response = view(request).render()
        self.assertEqual(response.content,
                         b'[{"user":"testuser1","full_name":"User number One","inn":"1010101010","wallet":"100.00"}]')
        self.assertEqual(response.status_code, 200)

        request = self.factory.post('', {'title': 'new idea'})
        response = view(request).render()
        self.assertEqual(response.status_code, 405)

    def test_url_ProfileCreateAPIView(self):
        view = ProfileCreateAPIView.as_view()
        request = self.factory.post('/add/', {'title': 'new idea'})
        response = view(request).render()
        self.assertEqual(response.status_code, 400)

        view = ProfileCreateAPIView.as_view()
        request = self.factory.post('/add/',
                                    {"user": 2, "full_name": "User number Two", "inn": "1111111111", "wallet": 10.00})
        response = view(request).render()
        self.assertEqual(response.status_code, 201)

    def test_get_url_TransactionListAPIView(self):
        view = TransactionListAPIView.as_view()
        request = self.factory.get('/transaction/', {})
        response = view(request).render()
        self.assertEqual(response.content,
                         b'[{"id":1,"full_name":"User number One","inn":"1010101010","wallet":"100.00","user":1}]')
        self.assertEqual(response.status_code, 200)

    def test_post_url_TransactionListAPIView(self):
        view = TransactionListAPIView.as_view()
        request = self.factory.post('', {
            "full_name": "User number One", "inn": "1010101010", "wallet": "100.00", "inns": "1010101010"
        })
        response = view(request).render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, str.encode('"Транзакция прошла успешно"', encoding='utf-8'))

        request = self.factory.post('', {
            "full_name": "User number One", "inn": "1010101010", "wallet": "100.00", "inns": "10101010"
        })
        response = view(request).render()
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        del self.one, self.user_one
