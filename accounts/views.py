from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import ProfileForm, UserInfoForm
from .models import Profile


def get_profile(user):
    """Profiles are auto-created by a signal, but fall back safely for any
    user that predates it."""
    profile = Profile.objects.get(user=user)
    return profile


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['profile'] = get_profile(user)
        context['comment_count'] = user.comments.count()
        context['message_count'] = user.contact_messages.count()
        return context


class ProfileEditView(LoginRequiredMixin, generic.View):
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("accounts:profile")

    # we seperate user's action in get and post method, if they see the profile form get method is used and if they send anything post method is used
    def get(self, request, *args, **kwargs):
        profile = get_profile(request.user) # get the profile of the user
        return render(request, self.template_name, {
            "user_form": UserInfoForm(instance=request.user),
            "profile_form": ProfileForm(instance=profile),
        }) # render the template with the forms

    def post(self, request, *args, **kwargs):
        profile = get_profile(request.user) # get the profile of the user
        user_form = UserInfoForm(request.POST, instance=request.user) # fill the form with the data from the request.post for the user in request.user otherwise it creates a new user
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile) # fill the form with the data from the request.post and request.FILES (for any avatar or other files) for the instance=profile otherwise it creates a new profile

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "اطلاعات شما با موفقیت بروزرسانی شد.")
            return redirect(self.success_url)

        return render(request, self.template_name, {
            "user_form": user_form,
            "profile_form": profile_form,
        }) # we have two forms because some of the fields are in user_form and some in profile_form
