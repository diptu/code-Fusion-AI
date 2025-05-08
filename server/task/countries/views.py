from countries.models import Country
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.views import generic
from django.views.generic import DetailView, ListView
from .models import Country


class LoginRequiredMessageMixin(LoginRequiredMixin):
    login_url = settings.LOGIN_URL  # Just in case it's not picked up
    redirect_field_name = "next"

    def handle_no_permission(self):
        messages.error(self.request, "You must be logged in to view this page.")
        return redirect(f"{self.get_login_url()}?next={self.request.get_full_path()}")


class SameRegionCountriesWithLanguagesView(
    LoginRequiredMessageMixin, generic.DetailView
):
    model = Country
    template_name = "countries/same_region_languages.html"
    context_object_name = "target_country"
    paginate_by = settings.PAGE_SIZE  # e.g., 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target_country = self.object

        # Get same region countries (excluding the target one)
        same_region_countries = Country.objects.filter(
            region=target_country.region
        ).exclude(pk=target_country.pk)

        # Prepare data
        same_region_data = []
        for country in same_region_countries:
            languages_json = country.languages or {}
            same_region_data.append(
                {
                    "country": country,
                    "spoken_languages": languages_json,
                }
            )

        # Paginate the data
        paginator = Paginator(same_region_data, self.paginate_by)
        page_number = self.request.GET.get("page")

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # Add to context
        context["same_region_countries_data"] = page_obj
        context["page_obj"] = page_obj
        context["paginator"] = paginator  # Required for pagination controls
        context["is_paginated"] = page_obj.has_other_pages()
        return context


class CountryListView(ListView):
    model = Country
    template_name = "countries/country_list.html"
    context_object_name = "countries"
    paginate_by = settings.PAGE_SIZE
    ordering = ["name_common"]
    login_url = "/api/login/"  # Redirects unauthenticated users to login

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("name_common", "")
        if query:
            queryset = queryset.filter(name_common__icontains=query)
        return queryset


class CountryDetailView(LoginRequiredMessageMixin, DetailView):
    model = Country
    template_name = "countries/country_detail.html"
    context_object_name = "country"

    def get_context_data(self, **kwargs):
        # Call the parent class's method to get the context data
        context = super().get_context_data(**kwargs)

        # Add the summary property to the context
        context["summary"] = self.object.summary
        context["language"] = self.object.language

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


# def country_summary_view(request, *args, **kwargs):
#     cca2 = kwargs.get("cca2")
#     if not cca2:
#         return render(
#             request,
#             "country_summary.html",
#             {"message": "Missing 'cca2' parameter."},
#             status=400,
#         )

#     try:
#         country = Country.objects.get(cca2=cca2.upper())
#         return render(
#             request,
#             "country_summary.html",
#             {
#                 "summary": country.summary,
#                 "population_density": country.population_density,
#                 "primary_currency": country.primary_currency,
#                 "local_weekend": country.local_weekend,
#             },
#         )
#     except Country.DoesNotExist:
#         return render(
#             request,
#             "country_summary.html",
#             {"message": "Country not found"},
#             status=404,
#         )
