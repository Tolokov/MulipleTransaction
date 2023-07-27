from django.urls import path

from .views import Profiles

urlpatterns = [
    path('', Profiles.as_view(), name='profiles')
]
