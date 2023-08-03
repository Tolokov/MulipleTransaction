from django.urls import path

from .views import ProfileListAPIView, ProfileCreateAPIView, TransactionListAPIView


urlpatterns = [
    path('', ProfileListAPIView.as_view()),
    path('add/', ProfileCreateAPIView.as_view()),
    path('transaction/', TransactionListAPIView.as_view()),
]
