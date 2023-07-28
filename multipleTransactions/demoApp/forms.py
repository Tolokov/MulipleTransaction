from django import forms
from django.forms import ModelChoiceField
from django.core.exceptions import ValidationError
from django.forms import Textarea, CharField

from .models import Profile


class FormAddProfile(forms.ModelForm):
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


class FormAddTransaction(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].empty_label = "---Выберите пользователя---"

    inn_receivers = forms.CharField(widget=forms.Textarea(attrs={'cols': 30, 'rows': 10}), label="Инн получателей через запятую")
    # full_name = ModelChoiceField(queryset=Profile.objects.filter(wallet__gt=0.01), label="Имя пользователя")

    class Meta:
        model = Profile
        fields = ["full_name", "wallet"]

    def clean_wallet(self):
        wallet_data = self.cleaned_data["wallet"]
        full_name_data = self.cleaned_data["full_name"]

        wallet_values = Profile.objects.filter(full_name=full_name_data).first().wallet

        if wallet_data <= 0:
            raise ValidationError("Нельзя переводить отрицательную или нулевую сумму")
        elif wallet_data > wallet_values:
            raise ValidationError("У пользователя нет таких денег")
        return wallet_data

