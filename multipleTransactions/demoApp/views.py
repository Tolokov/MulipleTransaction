from rest_framework import generics, response, views, status
from .serializers import *
from .models import Profile


class ProfileListAPIView(generics.ListAPIView):
    """Представление списка записей пользователя"""
    serializer_class = ProfileListSerializer

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


class TransactionCreateAPIView(views.APIView):
    def post(self, request):
        profiles = TransactionCreateSerializer(data=request.data)
        if profiles.is_valid():
            print("Валидация успешна")
            pass
            # profiles.save()

        return response.Response(profiles.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return response.Response(profiles.errors)


