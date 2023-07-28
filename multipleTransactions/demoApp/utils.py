from django.db.models import F

from decimal import Decimal, ROUND_DOWN

from .models import Profile


class Transaction:
    """Класс для проведения транзакции"""

    def __init__(self, payer, inns: str, money_to_be_debited):
        self.payer = payer
        self.inns_list = inns.split(",")
        self.count_recipients = self.inns_list.__len__()
        self.money = Decimal(money_to_be_debited)

    def run(self):
        #
        try:
            up_wallet = self.calculate_average()
            down_wallet = self.calculate_subtraction(up_wallet)

            if self.up_wallet_in_model(up_wallet) and self.down_wallet(down_wallet):
                print("Транзакция проведена успешно")
                print(f"Списано {down_wallet} по {up_wallet} с {self.count_recipients} пользователей")

        except Exception as e:
            print("Транзакция отменена: ", e)
        finally:
            print(self.__str__())

    def calculate_average(self):
        """Высчитывает, сколько должен средств должен получить каждый пользователь"""
        item = Decimal(self.money / self.count_recipients).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        return item

    def calculate_subtraction(self, up_wallet):
        """Перезаписывает значение Wallet в базе данных"""
        item = up_wallet * self.count_recipients
        return item

    def up_wallet_in_model(self, up_wallet):
        """Увеличение значения кошелька пользователей с перечисленными ИНН"""
        Profile.objects.filter(inn__in=self.inns_list).update(wallet=F("wallet") + up_wallet)
        return True

    def down_wallet(self, down_wallet):
        """Уменьшение значения кошелька конкретного пользователя"""
        Profile.objects.filter(pk=self.payer.pk).update(wallet=F("wallet") - down_wallet)
        return True

    def __str__(self):
        return str(f"{self.payer, self.inns_list, self.count_recipients, self.money}")
