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
