from apps.accounts.models import UserProfile
from django.views.generic import UpdateView
from apps.accounts.forms import UserProfileForm
from django.urls import reverse_lazy
from django.contrib import messages
from apps.accounts.services.profile_service import ProfileService


class ProfileView(UpdateView):

    model = UserProfile

    form_class = UserProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("accounts:dashboard")

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