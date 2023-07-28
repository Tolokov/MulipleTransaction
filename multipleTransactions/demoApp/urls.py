from django.urls import path

from .views import ShowProfilesView, AddProfileView, CreateTransactionView

urlpatterns = [
    path('', ShowProfilesView.as_view(), name='profiles'),
    path('add/', AddProfileView.as_view(), name='add_profile'),
    path('transaction/', CreateTransactionView.as_view(), name='add_transaction'),

]
