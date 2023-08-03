from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """It stores the client's personal information and the amount of money"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField("Имя пользователя", max_length=150)
    inn = models.CharField("ИНН", max_length=12, unique=True)
    wallet = models.DecimalField("Кошелёк", max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.full_name, self.inn}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
