from django.forms import ModelChoiceField, ModelForm, CharField, DecimalField, Form
from django.core.exceptions import ValidationError

from .models import Profile


class FormAddProfile(ModelForm):
    """Форма для добавления нового пользователя"""

    class Meta:
        model = Profile
        fields = "__all__"

    def clean_inn(self):
        data = self.cleaned_data["inn"]
        if not data.isdigit():
            raise ValidationError("Идентификационный номер налогоплательщика должен содержать только цифры")
        elif data.__len__() != 10 and data.__len__() != 12:
            raise ValidationError("Идентификационный номер налогоплательщика должен состоять из 10 или 12 символов")
        return data

    def clean_wallet(self):
        data = self.cleaned_data["wallet"]
        if data < 0:
            raise ValidationError("Пользователь не может иметь долг")
        return data

    def clean_full_name(self):
        data = self.cleaned_data["full_name"]
        if not data.replace(" ", "").isalpha():
            raise ValidationError("ФИО пользователя должно содержать только символы и пробелы")
        return data


class FormAddTransaction(Form):
    """Форма для проведения перевода"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].empty_label = "---Выберите пользователя---"

    Queryset = Profile.objects.filter(wallet__gt=0.01)

    full_name = ModelChoiceField(queryset=Queryset, label="Имя пользователя")
    wallet = DecimalField(max_digits=12, decimal_places=2, min_value=0.00, label="К списанию")
    inns = CharField(max_length=255, label="Инн получателей через запятую")

    def clean_inns(self):
        data = self.cleaned_data["inns"]
        if 10 != data.__len__() != 12 and data.count(",") == 0:
            raise ValidationError("Введен неверный ИНН")
        elif data.__len__() > 12 and data.count(",") == 0:
            raise ValidationError("Неправильный формат ввода данных")
        elif data[-1] == ",":
            raise ValidationError("Перечисление не может начинаться или заканчиваться разделителем")
        elif not data.replace(",", "").isdigit():
            raise ValidationError("Идентификационный номер налогоплательщика должен содержать только цифры и запятые")

        inns_split = set(data.split(","))
        for inn in inns_split:
            orm_response = Profile.objects.filter(inn=inn)
            if not bool(orm_response):
                raise ValidationError("Одного из пользователей, с представленным ИНН, не существует")

        return data

    def clean_wallet(self):
        wallet_data = self.cleaned_data["wallet"]
        full_name_data = self.cleaned_data["full_name"]

        wallet_values = Profile.objects.get(pk=full_name_data.pk).wallet
        if wallet_data <= 0:
            raise ValidationError("Нельзя переводить отрицательную или нулевую сумму")
        elif wallet_data > wallet_values:
            raise ValidationError("У пользователя нет таких денег")
        return wallet_data
