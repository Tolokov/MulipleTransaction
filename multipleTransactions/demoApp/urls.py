from django.urls import path

from .views import ProfileListAPIView, ProfileCreateAPIView, TransactionCreateAPIView, TransactionListAPIView


urlpatterns = [
    path('', ProfileListAPIView.as_view()),
    path('add/', ProfileCreateAPIView.as_view()),
    path('transaction/', TransactionListAPIView.as_view()),
    path('add_transaction/', TransactionCreateAPIView.as_view()),
]
