from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from ..models import Profile


class TestView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user_one = User.objects.create_user(username='testuser5', password='15321')
        self.one = Profile.objects.create(
            user=self.user_one, full_name="User number One", inn="1010101010", wallet=100.0)

    def test_urls(self):
        cases = ('add_profile', 'profiles', 'add_transaction')
        for i in cases:
            response = self.c.get(reverse(i))
            self.assertEqual(response.status_code, 200)

    def test_post_not_valid(self):
        response = self.c.post('/transaction/', {
            "full_name": '1',
            "inns": '2',
            "money_to_be_debited": '3',
        })
        self.assertEqual(response.status_code, 200)

    def test_post_valid(self):
        response = self.c.post('/transaction/', {'full_name': ['1'],
                                                'wallet': ['0.03'],
                                                'inns': ['1010101010']
                                                })

        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        del self.c, self.user_one, self.one
