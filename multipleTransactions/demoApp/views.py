from rest_framework import generics, response, views, status

from .serializers import *
from .models import Profile
from .utils import Transaction


class ProfileListAPIView(generics.ListAPIView):
    """Представление списка записей пользователя"""
    serializer_class = ProfileListSerializer
    http_method_names = ['get']

    def get_queryset(self):
        profiles = Profile.objects.all()
        return profiles


class ProfileCreateAPIView(views.APIView):
    def post(self, request):
        profiles = ProfileCreateSerializer(data=request.data)
        if profiles.is_valid():
            profiles.save()
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            return response.Response(profiles.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListAPIView(views.APIView):

    def get(self, request):
        profiles = Profile.objects.filter(wallet__gt=0.00)
        serializer = TransactionListSerializer(profiles, many=True)
        return response.Response(serializer.data, status=200)

    def post(self, request):
        profiles = TransactionCreateSerializer(data=request.data)
        if profiles.is_valid():
            data = profiles.data

            t = Transaction(
                payer=data["full_name"], inn=data["inn"], inns=data["inns"], money_to_be_debited=data["wallet"])
            t.run()
            return response.Response("Транзакция прошла успешно", status=200)
        return response.Response(profiles.errors, status=status.HTTP_400_BAD_REQUEST)
