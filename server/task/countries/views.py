from django.http import HttpResponse
from countries.models import Country

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# views.py
import requests
from django.conf import settings
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


import requests
from django.conf import settings
from django.views.generic import ListView
from django.shortcuts import redirect
from django.core.paginator import Paginator
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Country


class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    template_name = "countries/country_list.html"
    context_object_name = "countries"
    paginate_by = 10
    ordering = ["name_common"]
    login_url = "/api/login/"  # Redirects unauthenticated users to login


class CountryDetailView(DetailView):
    model = Country
    template_name = "countries/country_detail.html"
    context_object_name = "country"

    def get_context_data(self, **kwargs):
        # Call the parent class's method to get the context data
        context = super().get_context_data(**kwargs)

        # Add the summary property to the context
        context["summary"] = self.object.summary

        return context


# class CountryListView(LoginRequiredMixin, ListView):
#     model = Country
#     template_name = "countries/country_list.html"
#     context_object_name = "countries"
#     paginate_by = 10  # Number of countries per page
#     ordering = ["name_common"]  # Optional


def country_summary_view(request, *args, **kwargs):
    cca2 = kwargs.get("cca2")
    if not cca2:
        return HttpResponse("Missing 'cca2' parameter.", status=400)

    try:
        country = Country.objects.get(cca2=cca2.upper())
        return HttpResponse(f"<pre>{country.summary}</pre>")
    except Country.DoesNotExist:
        return HttpResponse("Country not found", status=404)
