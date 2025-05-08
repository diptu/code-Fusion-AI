from countries.models import Country
from django.contrib.auth import authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


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
