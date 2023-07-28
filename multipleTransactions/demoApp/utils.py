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
        """Создание и обработка транзакции"""
        sender_wallet = Profile.objects.get(pk=self.payer.pk).wallet
        recipient_wallets = Profile.objects.filter(inn__in=self.inns_list).values_list('id', 'wallet')
        try:
            up_wallet = self.calculate_average()
            down_wallet = self.calculate_subtraction(up_wallet)

            if self.up_wallet_in_model(up_wallet) and self.down_wallet(down_wallet):
                print("Транзакция проведена успешно")
                print(f"Списано {down_wallet} по {up_wallet} с {self.count_recipients} пользователей")

        except Exception as e:
            Profile.objects.get(pk=self.payer.pk).wallet = sender_wallet
            print("Транзакция отменена: ", e)
            print("Возвращено значение кошелька для ", self.payer, " на ", sender_wallet)
            for obj in recipient_wallets:
                Profile.objects.get(id=obj[0]).wallet = obj[1]
                print("Возвращено значение кошелька получателя №", obj[0], " на ", obj[1])

        else:
            del sender_wallet
            del recipient_wallets

        finally:
            print(self.__str__())

    def calculate_average(self):
        """Высчитывает, сколько средств должен получить каждый пользователь"""
        item = Decimal(self.money / self.count_recipients).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        return item

    def calculate_subtraction(self, up_wallet):
        """Высчитывает сумму списания"""
        item = up_wallet * self.count_recipients
        return item

    def up_wallet_in_model(self, up_wallet):
        """Перезаписывает значения Wallet, пользователей с перечисленными ИНН"""
        Profile.objects.filter(inn__in=self.inns_list).update(wallet=F("wallet") + up_wallet)
        return True

    def down_wallet(self, down_wallet):
        """Уменьшение значение Wallet конкретного пользователя"""
        Profile.objects.filter(pk=self.payer.pk).update(wallet=F("wallet") - down_wallet)
        return True

    def __str__(self):
        return str(f"{self.payer, self.inns_list, self.count_recipients, self.money}")
