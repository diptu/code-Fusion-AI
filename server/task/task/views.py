from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views import View


from django.shortcuts import render
from django.contrib.auth import logout
from django.views import View


from django.shortcuts import render

# Create your views here.


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from datetime import timedelta
from django.conf import settings

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.response import Response
from django.conf import settings


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginView(LoginView):
    """
    A custom LoginView to generate JWT token on successful login.
    """

    template_name = "registration/login.html"
    form_class = AuthenticationForm

    def form_valid(self, form):
        """
        Override form_valid to generate JWT token upon successful login.
        """
        user = form.get_user()

        # Log the user in with Django's default login
        login(self.request, user)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        # Return token as JSON response
        return JsonResponse(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )

    def form_invalid(self, form):
        """
        Override form_invalid to return an error message if login is unsuccessful.
        """
        return JsonResponse({"error": "Invalid credentials"}, status=400)


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            access_token = data.get("access")
            refresh_token = data.get("refresh")

            # Set the access token in cookies
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=settings.DEBUG is False,  # Set to True in production
                samesite="Lax",
                max_age=3600,  # 1 hour
            )

            # Set the refresh token in cookies
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=settings.DEBUG is False,
                samesite="Lax",
                max_age=7 * 24 * 3600,  # 7 days
            )

        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            data = response.data
            access_token = data.get("access")
            refresh_token = data.get("refresh")

            # Set secure cookie attributes as needed
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=settings.DEBUG is False,  # Set to True in production
                samesite="Lax",
                max_age=3600,  # 1 hour
            )

            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=settings.DEBUG is False,
                samesite="Lax",
                max_age=7 * 24 * 3600,  # 7 days
            )

        return response


def home_view(request):
    context = {
        "title": "home",
    }
    return render(request, "home.html", context)


class LogoutView(View):
    """
    Logs out an authenticated user and serves a logout confirmation page.
    """

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, "registration/logout.html")  # This template should exist


class CustomLoginView(APIView):
    """
    Login endpoint that returns JWT token on successful login.

    POST /api/login/
    {
        "username": "user",
        "password": "password"
    }
    Returns:
    {
        "access": "<JWT access token>",
        "refresh": "<JWT refresh token>"
    }
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Generate the JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response(
                {"access": access_token, "refresh": str(refresh)},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )
