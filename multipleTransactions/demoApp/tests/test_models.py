from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from decimal import Decimal

from ..models import Profile


class ProfileTestCase(TestCase):

    def setUp(self):
        self.user_one = User.objects.create_user(username='testuser1', password='12345')
        self.user_two = User.objects.create_user(username='testuser2', password='54321')
        self.user_three = User.objects.create_user(username='testuser3', password='12321')
        self.user_four = User.objects.create_user(username='testuser4', password='12521')
        self.user_five = User.objects.create_user(username='testuser5', password='15321')

        self.one = Profile.objects.create(
            user=self.user_one, full_name="User number One", inn="1010101010", wallet=0.0)

        self.two = Profile.objects.create(
            user=self.user_two, full_name="User number Two", inn="010101010101", wallet=9.99)

        self.three = Profile.objects.create(
            user=self.user_three, full_name="User number Tree", inn="1111111111", wallet=10.0)

    def test_string(self):
        self.assertEqual(str(self.one), "('User number One', '1010101010')")
        self.assertEqual(self.two.__str__(), "('User number Two', '010101010101')")
        self.assertEqual(self.three.__repr__(), "<Profile: ('User number Tree', '1111111111')>")

    def test_queryset(self):
        queryset = Profile.objects.all()
        lists = queryset.values_list('id', 'wallet')
        self.assertEqual([i for i in lists], [(1, Decimal('0.00')), (2, Decimal('9.99')), (3, Decimal('10.00'))])

    def test_unique(self):
        with self.assertRaises(IntegrityError):
            self.four = Profile.objects.create(user=self.user_four, full_name="4", inn="1234567890")
            self.five = Profile.objects.create(user=self.user_five, full_name="5", inn="1234567890")

    def tearDown(self):
        del self.two, self.one, self.three, self.user_one, self.user_two, self.user_three, self.user_four, self.user_five
