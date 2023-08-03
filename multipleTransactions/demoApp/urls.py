from django.urls import path

from .views import ProfileListAPIView, ProfileCreateAPIView, TransactionCreateView


urlpatterns = [
    path('', ProfileListAPIView.as_view()),
    path('add/', ProfileCreateAPIView.as_view()),
    path('transaction/', TransactionCreateView.as_view()),
]
