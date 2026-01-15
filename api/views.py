from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from typing import Any

from .forms import SignUpForm, LoginForm
from .models import User

@login_required(login_url='login')
def main_spa(request: HttpRequest) -> HttpResponse:
    """
    Renders the Single Page Application (SPA).
    Requires the user to be logged in.
    """
    return render(request, 'api/spa/index.html', {})

class CustomLoginView(LoginView):
    """
    Custom Login View using the defined LoginForm.
    """
    authentication_form = LoginForm
    template_name = 'api/login.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return str(reverse_lazy('spa_home'))

class SignUpView(CreateView):
    """
    View for user registration.
    """
    model = User
    form_class = SignUpForm
    template_name = 'api/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form: Any) -> HttpResponse:
        """
        Handles valid form submission. 
        """
        return super().form_valid(form)

def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Logs out the user and redirects to login.
    """
    logout(request)
    return redirect('login')