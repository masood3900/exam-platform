from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile
from django.views.generic import CreateView,UpdateView
from django.urls import reverse_lazy
from.forms import UserRegisterForm,UserProfileForm
from django.contrib import messages
from apps.accounts.services.profile_service import ProfileService

@login_required
def dashboard(req):
    return render(req,"dashboard/index.html")


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("dashboard")

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
    
class ProfileView(UpdateView):

    model = UserProfile
    form_class = UserProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_status"] = ProfileService.completion(
            self.request.user
        )
        return context

    def form_valid(self, form):

        response = super().form_valid(form)

        user = self.request.user

        user.first_name = form.cleaned_data.get("first_name", "")
        user.last_name = form.cleaned_data.get("last_name", "")
        user.email = form.cleaned_data.get("email", "")

        user.save()

        messages.success(
            self.request,
            "اطلاعات پروفایل با موفقیت ذخیره شد."
        )

        return response