from countries.models import Country
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class JWTLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        response = HttpResponseRedirect(reverse_lazy("login"))

        # Remove JWT cookies
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        messages.success(request, "You have been logged out.")
        return response


class JWTLoginView(LoginView):
    template_name = "registration/login.html"

    def form_valid(self, form):
        # Log in the user (standard Django)
        response = super().form_valid(form)

        # Generate JWT tokens
        user = form.get_user()
        serializer = TokenObtainPairSerializer()
        tokens = serializer.get_token(user)
        access_token = str(tokens.access_token)
        refresh_token = str(tokens)

        # Set tokens in HTTP-only cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
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

            # Set tokens in HTTP-only cookies
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,  # Use False only in development
                samesite="Lax",
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="Lax",
            )

        return response


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
