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
        self.data = {"full_name": "USER", "inn": "090807060504", "wallet": "100.0"}

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

    def test_messages(self):
        serializer = ProfileCreateSerializer()

        with self.assertRaises(ValidationError) as context:
            serializer.validate_full_name("qwe-rty")
        self.assertEqual(
            str(context.exception.get_full_details()[0]["message"]),
            "ФИО пользователя должно содержать только символы и пробелы"
        )

        with self.assertRaises(ValidationError) as context:
            serializer.validate_wallet(-1)
        self.assertEqual(
            str(context.exception.get_full_details()[0]["message"]),
            "Пользователь не может иметь долг"
        )

        with self.assertRaises(ValidationError) as context:
            serializer.validate_inn("text")
        self.assertEqual(
            str(context.exception.get_full_details()[0]["message"]),
            "Идентификационный номер налогоплательщика должен содержать только цифры"
        )

        with self.assertRaises(ValidationError) as context:
            serializer.validate_inn("0" * 11)
        self.assertEqual(
            str(context.exception.get_full_details()[0]["message"]),
            "Идентификационный номер налогоплательщика должен состоять из 10 или 12 символов"
        )

    def tearDown(self):
        user_one = User.objects.get(username='USER')
        user_one.delete()
        del self.one


class TransactionCreateSerializerTest(TestCase):

    def setUp(self):
        user_one = User.objects.create_user(username='USER', password='USER')
        self.one = Profile.objects.create(user=user_one, full_name="User", inn="090807060504", wallet=100.0)

    def test_messages(self):
        serializer = TransactionCreateSerializer()

        with self.assertRaises(ValidationError) as context:
            serializer.validate_wallet(-10)
        self.assertEqual(
            str(context.exception.get_full_details()[0]["message"]),
            "Нельзя переводить отрицательную или нулевую сумму"
        )

        with self.assertRaises(ValidationError) as context:
            serializer.validate_inns("0000000000")
        self.assertEqual(
            str(context.exception.get_full_details()[0]["message"]),
            "Одного из пользователей, с представленным ИНН, не существует"
        )

        with self.assertRaises(ValidationError) as context:
            serializer.validate_inns(",0000000000,")
        self.assertEqual(
            str(context.exception.get_full_details()[0]["message"]),
            "Перечисление не может начинаться или заканчиваться разделителем"
        )

        with self.assertRaises(ValidationError) as context:
            serializer.validate_inns("0" * 11)
        self.assertEqual(
            str(context.exception.get_full_details()[0]["message"]),
            "Введен неверный ИНН"
        )

        with self.assertRaises(ValidationError) as context:
            serializer.validate_inns("0,0" * 10)
        self.assertEqual(
            str(context.exception.get_full_details()[0]["message"]),
            "Одного из пользователей, с представленным ИНН, не существует"
        )

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
        serializer = TransactionCreateSerializer()
        validated_value = serializer.validate_wallet(Decimal("10.09"))
        self.assertEqual(validated_value, Decimal("10.09"))
        for i in (-1, -10, -100.01, -9999999.99, Decimal('-0.01'), 0.00):
            with self.assertRaises(ValidationError):
                serializer.validate_wallet(i)

    def test_validate(self):
        serializer = TransactionCreateSerializer()
        data = {"full_name": "User", "inn": "090807060504", "wallet": 10.0, "inns": "090807060504"}
        validated_value = serializer.validate(data)
        self.assertEqual(validated_value,
                         {'full_name': 'User', 'inn': '090807060504', 'wallet': 10.0, 'inns': '090807060504'})

    def test_validate_messages(self):
        serializer = TransactionCreateSerializer()

        data = {"full_name": "User0", "inn": "090807060504", "wallet": 10.0, "inns": "090807060504"}
        with self.assertRaises(ValidationError) as context:
            validated_value = serializer.validate(data)
        self.assertEqual(str(context.exception.get_full_details()[0]["message"]),
                         "Пользователя с такими данными не существует, либо поля 'full_name' и 'inn' не уникальные вместе.")

        data = {"full_name": "User", "inn": "09080706050", "wallet": 10.0, "inns": "090807060504"}
        with self.assertRaises(ValidationError) as context:
            validated_value = serializer.validate(data)
        self.assertEqual(str(context.exception.get_full_details()[0]["message"]),
                         "Пользователя с такими данными не существует, либо поля 'full_name' и 'inn' не уникальные вместе.")

        data = {"full_name": "User", "inn": "090807060504", "wallet": 100.01, "inns": "090807060504"}
        with self.assertRaises(ValidationError) as context:
            validated_value = serializer.validate(data)
        self.assertEqual(str(context.exception.get_full_details().get('wallet')["message"]),
                         "У пользователя нет таких денег.")

    def tearDown(self):
        user_one = User.objects.get(username='USER')
        user_one.delete()
        del self.one
