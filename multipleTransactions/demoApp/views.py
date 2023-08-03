from rest_framework import generics, response, views, status
from .serializers import ProfileListSerializer, ProfileCreateSerializer
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
            return response.Response(status=201)
        else:
            return response.Response(profiles.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionCreateView(views.APIView):
    pass
