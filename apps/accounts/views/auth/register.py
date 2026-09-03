from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from apps.accounts.forms import UserRegisterForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "accounts/registration/register.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        print("FORM VALID")
        print(form.cleaned_data)

        response = super().form_valid(form)

        print("USER CREATED:", self.object)

        login(self.request, self.object)

        return response
    def form_invalid(self, form):

        print("FORM INVALID")
        print(form.errors.as_json())
        return super().form_invalid(form)
    