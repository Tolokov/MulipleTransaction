from decimal import Decimal, ROUND_DOWN


class Transaction:
    """Класс для проведения транзакции"""

    def __init__(self, payer, inns: str, money_to_be_debited):
        self.payer = payer
        self.inns_list = inns.split(",")
        self.count_recipients = self.inns_list.__len__()
        self.money = Decimal(money_to_be_debited)

    # Списание средств
    def run(self):
        #
        try:
            up_wallet = self.calculate_average()
            down_wallet = self.calculate_subtraction(up_wallet)
            print(up_wallet, down_wallet, self.count_recipients)
        except Exception as e:
            print("Транзакция отменена: ", e)
        finally:
            print(self.__str__())

    def calculate_average(self):
        """Высчитывает, сколько должен средств должен получить каждый пользователь"""
        item = Decimal(self.money/self.count_recipients).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        return item

    def calculate_subtraction(self, up_wallet):
        """Перезаписывает значение Wallet в базе данных"""
        item = up_wallet * self.count_recipients
        return item


    def __str__(self):
        return str(f"{self.payer, self.inns_list, self.count_recipients, self.money}")
