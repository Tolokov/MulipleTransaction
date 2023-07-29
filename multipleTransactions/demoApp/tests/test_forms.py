from django.test import TestCase
from ..models import Profile
from ..forms import FormAddProfile, FormAddTransaction
from django.contrib.auth.models import User


class FormAddProfileTest(TestCase):

    def setUp(self):
        self.user_one = User.objects.create_user(username='admin', password='admin')

    def test_clean_valid(self):
        data = {'user': 1, 'full_name': 'Тестовый пользователь', 'wallet': '3003', 'inn': '1111111111'}
        form = FormAddProfile(data=data)
        self.assertTrue(form.is_valid())

    def test_clean_inn_invalid(self):
        data = {'user': 1, 'full_name': 'Тестовый пользователь', 'wallet': '3003', 'inn': 'abc123'}
        form = FormAddProfile(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['inn'], ['Идентификационный номер налогоплательщика должен содержать только цифры'])

    def test_clean_inn_length(self):
        data = {'user': 1, 'full_name': 'Тестовый пользователь', 'wallet': '3003', 'inn': '1234567890123'}
        form = FormAddProfile(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['inn'], ['Убедитесь, что это значение содержит не более 12 символов (сейчас 13).'])

        data = {'user': 1, 'full_name': 'Тестовый пользователь', 'wallet': '3003', 'inn': '1' * 11}
        form = FormAddProfile(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['inn'], ['Идентификационный номер налогоплательщика должен состоять из 10 или 12 символов'])

        data = {'user': 1, 'full_name': 'Тестовый пользователь', 'wallet': '3003', 'inn': '1' * 9}
        form = FormAddProfile(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['inn'], ['Идентификационный номер налогоплательщика должен состоять из 10 или 12 символов'])

    def test_clean_wallet(self):
        data = {'user': 1, 'full_name': 'Тестовый пользователь', 'wallet': '-100', 'inn': '1111111111'}
        form = FormAddProfile(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['wallet'], ['Пользователь не может иметь долг'])

    def test_clean_full_name_valid(self):
        data = {'user': 1, 'full_name': 'Mikhael Mikhaelevich', 'wallet': '3003', 'inn': '1111111111'}
        form = FormAddProfile(data=data)
        self.assertTrue(form.is_valid())

        data['full_name'] = '09'
        form = FormAddProfile(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["full_name"], ["ФИО пользователя должно содержать только символы и пробелы"])

        data['full_name'] = 'Agent 007'
        form = FormAddProfile(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["full_name"], ["ФИО пользователя должно содержать только символы и пробелы"])

        data['full_name'] = '-'
        form = FormAddProfile(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["full_name"], ["ФИО пользователя должно содержать только символы и пробелы"])

        data['full_name'] = '-' * 2190
        form = FormAddProfile(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["full_name"], ['Убедитесь, что это значение содержит не более 150 символов (сейчас 2190).'])

        data['full_name'] = ','
        form = FormAddProfile(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["full_name"], ["ФИО пользователя должно содержать только символы и пробелы"])

    def tearDown(self):
        del self.user_one


class FormAddTransactionTest(TestCase):

    def setUp(self):
        self.user_one = User.objects.create_user(username='admin', password='admin')
        self.one = Profile.objects.create(user=self.user_one, full_name='Тестовый пользователь', wallet=100.10, inn='1111111111')
        self.Queryset = Profile.objects.get(full_name='Тестовый пользователь')
        self.data = {'user': 1, 'full_name': self.Queryset, 'inn': '1111111111', 'inns': '1111111111', 'wallet': 10.00}

    def test_clean_inns_valid(self):
        form = FormAddTransaction(data=self.data)
        # print(form.errors)
        self.assertTrue(form.is_valid())

    def test_clean_inns_invalid_format(self):
        self.data['inns'] = '1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14'
        form = FormAddTransaction(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['inns'], ["Идентификационный номер налогоплательщика должен содержать только цифры и запятые"])

        self.data['inns'] = '111222, 333444'
        form = FormAddTransaction(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['inns'], ["Идентификационный номер налогоплательщика должен содержать только цифры и запятые"])

        self.data['inns'] = '1111111111,abc'
        form = FormAddTransaction(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['inns'], ['Идентификационный номер налогоплательщика должен содержать только цифры и запятые'])

    def test_clean_inns_invalid_ending(self):
        self.data['inns'] = '111,222,333,'
        form = FormAddTransaction(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['inns'], ['Перечисление не может начинаться или заканчиваться разделителем'])

    def test_clean_inns_non_existent(self):
        self.data['inns'] = '333,,,333'
        form = FormAddTransaction(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['inns'], ['Одного из пользователей, с представленным ИНН, не существует'])

        self.data['inns'] = ',111,222,333'
        form = FormAddTransaction(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['inns'], ['Одного из пользователей, с представленным ИНН, не существует'])

    def test_clean_wallet_valid(self):
        self.data['wallet'] = 50
        form = FormAddTransaction(data=self.data)
        self.assertTrue(form.is_valid())

    def test_clean_wallet_invalid_negative(self):
        self.data['wallet'] = -50
        form = FormAddTransaction(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['wallet'], ['Убедитесь, что это значение больше либо равно 0.0.'])

    def test_clean_wallet_invalid_insufficient_funds(self):
        self.data['wallet'] = 200
        form = FormAddTransaction(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['wallet'], ['У пользователя нет таких денег'])

    def tearDown(self):
        del self.user_one, self.one, self.Queryset, self.data