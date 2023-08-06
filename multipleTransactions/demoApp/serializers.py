from rest_framework import serializers
from django.forms.models import model_to_dict

from .models import Profile


class ProfileListSerializer(serializers.ModelSerializer):
    """Отображение всех записей"""
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'full_name', 'inn', 'wallet')


class TransactionListSerializer(serializers.ModelSerializer):
    """Отображение всех записей, перевод для которых можно осуществить"""

    class Meta:
        model = Profile
        fields = '__all__'


class ProfileCreateSerializer(serializers.ModelSerializer):
    """Добавление данных к профилю пользователя"""

    class Meta:
        model = Profile
        fields = "__all__"

    def validate_full_name(self, value):
        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("ФИО пользователя должно содержать только символы и пробелы")
        return value

    def validate_wallet(self, value):
        if value < 0:
            raise serializers.ValidationError("Пользователь не может иметь долг")
        return value

    def validate_inn(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Идентификационный номер налогоплательщика должен содержать только цифры")
        elif value.__len__() != 10 and value.__len__() != 12:
            raise serializers.ValidationError(
                "Идентификационный номер налогоплательщика должен состоять из 10 или 12 символов")
        return value


class TransactionCreateSerializer(serializers.ModelSerializer):
    """Проверка данных для транзакции"""
    inns = serializers.CharField(max_length=255)
    inn = serializers.CharField(max_length=12, required=True)
    wallet = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)

    class Meta:
        model = Profile
        fields = ('id', 'full_name', 'inn', 'wallet', 'inns')

    def validate_inns(self, value):
        if 10 != value.__len__() != 12 and value.count(",") == 0:
            raise serializers.ValidationError("Введен неверный ИНН")
        elif value.__len__() > 12 and value.count(",") == 0:
            raise serializers.ValidationError("Неправильный формат ввода данных")
        elif value[-1] == ",":
            raise serializers.ValidationError("Перечисление не может начинаться или заканчиваться разделителем")
        elif not value.replace(",", "").isdigit():
            raise serializers.ValidationError(
                "Поле для идентификационных номеров налогоплательщиков должно содержать только цифры и запятые")

        inns_list = list(set(value.split(",")))
        profiles = Profile.objects.filter(inn__in=inns_list)
        profile_dict = {profile.inn: model_to_dict(profile) for profile in profiles}

        for inn in inns_list:
            if inn not in profile_dict:
                raise serializers.ValidationError("Одного из пользователей, с представленным ИНН, не существует")
        return value

    def validate_wallet(self, value):
        if value <= 0.00:
            raise serializers.ValidationError("Нельзя переводить отрицательную или нулевую сумму")
        return value

    def validate(self, data):
        """Проверяем, есть ли объект с такими же значениями full_name и inn в БД, а так-же количество денег"""
        full_name = data.get('full_name')
        inn = data.get('inn')
        wallet = data.get('wallet')

        if full_name and inn and wallet:
            queryset = Profile.objects.filter(full_name=full_name, inn=inn)
            if not queryset.exists():
                raise serializers.ValidationError(
                    "Пользователя с такими данными не существует, либо поля 'full_name' и 'inn' не уникальные вместе.")

            if queryset.first().wallet < wallet:
                raise serializers.ValidationError({'wallet': "У пользователя нет таких денег."})

        return data
