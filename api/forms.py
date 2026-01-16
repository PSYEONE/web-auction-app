from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class SignUpForm(UserCreationForm):
    """
    Form for user registration.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'date_of_birth', 'profile_image')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class LoginForm(AuthenticationForm):
    """
    Form for user authentication.
    """
    pass
