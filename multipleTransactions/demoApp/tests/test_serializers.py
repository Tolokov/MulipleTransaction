from unittest import TestCase
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError

from decimal import Decimal

from ..serializers import *
from ..models import Profile


class ProfileCreateSerializerTest(TestCase):

    def setUp(self):
        user_one = User.objects.create_user(username='USER', password='USER')
        self.one = Profile.objects.create(user=user_one, inn="090807060504", wallet=100.0)

    def test_validate_full_name_(self):
        serializer = ProfileCreateSerializer()
        validated_value = serializer.validate_full_name("fullname")
        self.assertEqual(validated_value, "fullname")
        for i in ("_", '09', 'Agent 007', ',', '- ', '-' * 2190):
            with self.assertRaises(ValidationError):
                serializer.validate_full_name(i)

    def test_validate_wallet(self):
        serializer = ProfileCreateSerializer()

        validated_value = serializer.validate_wallet(Decimal("190.09"))
        self.assertEqual(validated_value, Decimal("190.09"))
        for i in (-1, -10, -100.01, -9999999.99):
            with self.assertRaises(ValidationError):
                serializer.validate_wallet(i)

    def test_validate_inn(self):
        serializer = ProfileCreateSerializer()

        validated_value = serializer.validate_inn("010101010101")
        self.assertEqual(validated_value, "010101010101")

        for i in ("0101010", "o0o0o0o0o0o0", "qwertyyuio", "]" * 10, "-10", ""):
            with self.assertRaises(ValidationError):
                serializer.validate_inn(i)

    def tearDown(self):
        user_one = User.objects.get(username='USER')
        user_one.delete()
        del self.one


class TransactionCreateSerializerTest(TestCase):

    def setUp(self):
        user_one = User.objects.create_user(username='USER', password='USER')
        self.one = Profile.objects.create(user=user_one, full_name="User", inn="090807060504", wallet=100.0)

    def test_validate_inns(self):
        serializer = TransactionCreateSerializer()

        cases = ("12345", "1234567890123456", "12345,", "12345,6789a",
                 "1234567890,123456", "890,090807060504", "jkl", "090807060504,",
                 ",090807060504,", ",090807060504", "0908070605")

        validated_value = serializer.validate_inns("090807060504")
        self.assertEqual(validated_value, "090807060504")

        for i in cases:
            with self.assertRaises(ValidationError):
                serializer.validate_inns(i)

    def test_validate_wallet(self):
        serializer = ProfileCreateSerializer()

        validated_value = serializer.validate_wallet(Decimal("10.09"))
        self.assertEqual(validated_value, Decimal("10.09"))
        for i in (-1, -10, -100.01, -9999999.99):
            with self.assertRaises(ValidationError):
                serializer.validate_wallet(i)

    def test_validate(self):
        serializer = ProfileCreateSerializer()
        data = {"full_name": "user", "inn": "090807060504", "wallet": "100.0"}
        validated_value = serializer.validate(data)
        self.assertEqual(validated_value, {'full_name': 'user', 'inn': '090807060504', 'wallet': '100.0'})

    def tearDown(self):
        user_one = User.objects.get(username='USER')
        user_one.delete()
        del self.one
