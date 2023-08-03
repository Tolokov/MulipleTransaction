from rest_framework import serializers, validators, exceptions

from .models import Profile


class ProfileListSerializer(serializers.ModelSerializer):
    """Перечень пользователей"""

    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'full_name', 'inn', 'wallet')


class ProfileCreateSerializer(serializers.ModelSerializer):
    """Форма для новой записи"""

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
