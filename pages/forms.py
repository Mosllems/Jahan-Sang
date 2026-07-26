from django import forms

from .models import ContactForm


class Contact(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'شماره تلفن'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ایمیل'}),
            'message': forms.Textarea(attrs={
                'placeholder': 'در مورد پروژه خود برای ما بگویید ...',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Logged-in users don't retype their contact info — we fill it from
        # their account in the view. Keep only the message field for them
        # we delete the extra fields for the user logged in and there will be showing one field (message) in teplate
        if self.user and self.user.is_authenticated:
            del self.fields['first_name']
            del self.fields['last_name']
            del self.fields['phone_number']
            del self.fields['email']
