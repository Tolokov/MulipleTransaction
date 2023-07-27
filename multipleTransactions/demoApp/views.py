from django.views.generic import FormView, ListView
from .models import Profile


class Profiles(ListView):
    model = Profile
    template_name = 'profiles.html'
    context_object_name = 'profiles'


