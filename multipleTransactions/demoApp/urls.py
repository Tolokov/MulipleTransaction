from django.urls import path

from .views import ProfileListView, ProfileCreateView


urlpatterns = [
    path('', ProfileListView.as_view()),
    path('add/', ProfileCreateView.as_view())
]
