from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


class CustomSignupForm(SignupForm):
    mobile_number = forms.CharField(
        max_length=15,
        label="شماره موبایل",
        widget=forms.TextInput(attrs={"placeholder": "شماره موبایل"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "نام کاربری"
        self.fields["email"].label = "ایمیل"
        if "password1" in self.fields:
            self.fields["password1"].label = "رمز عبور"
        if "password2" in self.fields:
            self.fields["password2"].label = "تکرار رمز عبور"

    def save(self, request):
        user = super().save(request)
        user.mobile_number = self.cleaned_data["mobile_number"]
        user.save(update_fields=["mobile_number"])
        return user


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "login" in self.fields:
            self.fields["login"].label = "ایمیل"
        if "password" in self.fields:
            self.fields["password"].label = "رمز عبور"
        if "remember" in self.fields:
            self.fields["remember"].label = "مرا به خاطر بسپار"

class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = CustomUser
        fields = ('username', 'email', 'mobile_number')


class CustomUserChangeForm(UserChangeForm):
    class Meta():
        model = CustomUser
        fields = ('username', 'email', 'mobile_number')
