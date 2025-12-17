from datetime import date

from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_POST

import json

from typing import Any, TypedDict, cast

from .models import User

# USER VIEWS
class SignupPayload(TypedDict, total=False):
    email: str
    username: str
    password: str
    date_of_birth: str # Optional

class LoginPayload(TypedDict):
    username: str
    password: str

@require_POST
def login_api(request: HttpRequest) -> JsonResponse:
    """Authenticate a user and start a session."""
    try:
        raw: Any = json.loads(request.body.decode("utf-8"))
        data = cast(LoginPayload, raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return JsonResponse({'success': False, 'message': 'Username and password are required.'}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({"success": False, "message": "Invalid username or password"}, status=401)

    login(request, user)
    return JsonResponse({"success": True, "message": "Logged in!"})

@require_POST
def signup_api(request: HttpRequest) -> JsonResponse:
    """Register a new user account."""
    try:
        raw: Any = json.loads(request.body.decode("utf-8"))
        data = cast(SignupPayload, raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    dob_str = data.get("date_of_birth", "")
    dob: date | None = None

    # Validate date of birth if exists
    if dob_str:
        dob = parse_date(dob_str)  # returns date | None
        if dob is None:
            return JsonResponse(
                {"success": False, "message": "date_of_birth must be YYYY-MM-DD."}, status=400)

    if not username or not password or not email:
        return JsonResponse({'success': False, 'message': 'Username, email and password are required.'}, status=400)

    # Validate email and check if it exists already
    try:
        validate_email(email)
    except ValidationError as e:
        return JsonResponse({"success": False, "message": e.messages}, status=400)

    if User.objects.filter(email__iexact=email).exists():
        return JsonResponse({"success": False, "message": "Email already taken, please try again."}, status=400)

    # Limit the username to 3-30 characters
    if not (3 <= len(username) <= 30):
        return JsonResponse({"success": False, "message": "Username must be between 3 and 30 characters"}, status=400)

    # Validate username to check if it exists already
    if User.objects.filter(username__iexact=username).exists():
        return JsonResponse({"success": False, "message": "Username already taken, please try again."}, status=400)

    # Django password validator
    try:
        validate_password(password)
    except ValidationError as e:
        return JsonResponse({"success": False, "message": e.messages}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password, date_of_birth=dob)

    return JsonResponse({"success": True, "message": "Account created successfully!"})

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})
