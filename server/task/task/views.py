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

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from countries.models import Country


class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    template_name = "countries/country_list.html"
    context_object_name = "countries"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by("name_common")
        query = self.request.GET.get("name_common", "")
        if query:
            queryset = queryset.filter(name_common__icontains=query)
        return queryset


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
