from django.test import TestCase
from django.contrib.auth.models import User

from decimal import Decimal

from ..models import Profile
from ..utils import Transaction


class UtilsTestCase(TestCase):

    def setUp(self):
        user_one = User.objects.create_user(username='testuser1', password='12345')
        user_two = User.objects.create_user(username='testuser2', password='54321')
        user_three = User.objects.create_user(username='testuser3', password='12321')
        user_four = User.objects.create_user(username='testuser4', password='12521')
        user_five = User.objects.create_user(username='testuser5', password='15321')

        self.one = Profile.objects.create(user=user_one, full_name="1", inn="101", wallet=Decimal("0.0"))
        self.two = Profile.objects.create(user=user_two, full_name="2", inn="102", wallet=Decimal("10.00"))
        self.three = Profile.objects.create(user=user_three, full_name="3", inn="103", wallet=Decimal("100.00"))
        self.four = Profile.objects.create(user=user_four, full_name="4", inn="104", wallet=Decimal("0.0"))
        self.five = Profile.objects.create(user=user_five, full_name="5", inn="105", wallet=Decimal("0.0"))

    def test_init(self):
        t = Transaction(payer="3", inns="101,102", money_to_be_debited=50.00)
        self.assertEqual(t.payer, "3")
        self.assertEqual(t.count_recipients, 2)
        self.assertEqual(t.money, 50.00)

        cases = (
            ("-" * 23, 1),
            ("00,0" * 10, 11),
            ("", 1),
            ("6", 1),
            ("0312324444,123456789098,456", 3),
            ("0312324444,123456789098,", 2),
            (",0312324444,123456789098,", 2),
            (",0312324444123456789098,", 1),
        )
        for num, i in enumerate(cases):
            t = Transaction(payer="2", inns=i[0], money_to_be_debited=0.00)
            self.assertEqual(t.count_recipients, i[1], msg=f"{num}")

    def test_string(self):
        t = Transaction(payer=self.one, inns="0,23" * 3, money_to_be_debited=9999999)
        self.assertEqual(t.__str__(), "(<Profile: ('1', '101')>, ['0', '230', '230', '23'], 4, Decimal('9999999'))")

    def test_calculate_subtraction(self):
        t = Transaction(payer=self.two, inns="0,23", money_to_be_debited=9.99)
        item = t.calculate_subtraction(up_wallet=2)
        self.assertEqual(item, 4)

        cases = (
            ("1", 1, 1),
            ("1", 2, 2),
            ("1,1", 1, 2),
            ("1,1,", 2, 4),
            ("11," * 23, 2, 2 * 23),
            ("" * 10, 2, 2),
            ("9,", 1.99, 1.99),
            ("9," * 2, 1.99, 3.98),
            ("9," * 4, 1.99, 7.96),
            ("," * 4, 1.99, 1.99),
            ("J," * 9999, 99.02, 990100.98),
        )
        for num, i in enumerate(cases):
            t = Transaction(payer="None", inns=i[0], money_to_be_debited=0)
            item = t.calculate_subtraction(up_wallet=i[1])
            self.assertEqual(item, i[2], msg=f"{num}")

    def test_calculate_average(self):
        cases = (
            ("101", "10.00", Decimal("10.00")),
            ("101", "1.00", Decimal("1.00")),
            ("101,100,99", "10.00", Decimal("3.33")),
            ("101,101", "10.00", Decimal("5.00")),
            ("101", "0.01", Decimal("0.01")),

            ("101," * 9999, "0.00", Decimal("0.00")),
            ("101,101," * 9999, "99.98", Decimal("0.00")),
            ("101,101," * 9999, "199.98", Decimal("0.01")),
            ("101,101," * 9999, "199.97", Decimal("0.00")),

            ("101", "10", Decimal("10.00")),
            ("101, 100, 99", "99999999.999", Decimal("33333333.33")),
        )
        for num, i in enumerate(cases):
            t = Transaction(payer="2", inns=i[0], money_to_be_debited=i[1])
            item = t.calculate_average()
            self.assertEqual(item, i[2], msg=f"{num}")

    def tearDown(self):
        del self.two, self.one, self.three, self.four, self.five
