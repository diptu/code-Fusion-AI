from countries.models import Country
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.views.generic import DetailView, ListView
from .models import Country


class SameRegionCountriesWithLanguagesView(generic.DetailView):
    model = Country
    template_name = "countries/same_region_languages.html"
    context_object_name = "target_country"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_country = self.object
        same_region_countries = Country.objects.filter(
            region=target_country.region
        ).exclude(pk=target_country.pk)

        same_region_data = []
        for country in same_region_countries:
            languages_json = country.languages  # Access the JSON field
            spoken_languages = (
                languages_json if languages_json else []
            )  # Handle potential None or empty JSON
            same_region_data.append(
                {
                    "country": country,
                    "spoken_languages": spoken_languages,
                }
            )

        context["same_region_countries_data"] = same_region_data
        return context


class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    template_name = "countries/country_list.html"
    context_object_name = "countries"
    paginate_by = 10
    ordering = ["name_common"]
    login_url = "/api/login/"  # Redirects unauthenticated users to login

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("name_common", "")
        if query:
            queryset = queryset.filter(name_common__icontains=query)
        return queryset


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


def country_summary_view(request, *args, **kwargs):
    cca2 = kwargs.get("cca2")
    if not cca2:
        return render(
            request,
            "country_summary.html",
            {"message": "Missing 'cca2' parameter."},
            status=400,
        )

    try:
        country = Country.objects.get(cca2=cca2.upper())
        return render(
            request,
            "country_summary.html",
            {
                "summary": country.summary,
                "population_density": country.population_density,
                "primary_currency": country.primary_currency,
                "local_weekend": country.local_weekend,
            },
        )
    except Country.DoesNotExist:
        return render(
            request,
            "country_summary.html",
            {"message": "Country not found"},
            status=404,
        )
