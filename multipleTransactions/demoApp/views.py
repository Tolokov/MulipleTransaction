from django.views.generic import FormView, ListView, CreateView
from django.urls import reverse_lazy

from .models import Profile
from .forms import FormAddProfile, FormAddTransaction
from .utils import Transaction


class ShowProfilesView(ListView):
    model = Profile
    template_name = 'profiles.html'
    context_object_name = 'profiles'


class AddProfileView(CreateView):
    form_class = FormAddProfile
    template_name = 'add_profile.html'
    success_url = reverse_lazy('profiles')


class CreateTransactionView(FormView):
    form_class = FormAddTransaction
    template_name = 'transaction.html'
    success_url = reverse_lazy('profiles')

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            data = form.cleaned_data
            t = Transaction(payer=data["full_name"], inns=data["inns"], money_to_be_debited=data["wallet"])
            t.run()
        else:
            print("Форма не валидна")

        return super().post(request, *args, **kwargs)
