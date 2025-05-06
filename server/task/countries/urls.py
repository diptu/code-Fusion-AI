from django.urls import path
from countries.views import country_summary_view
from .views import (
    CountryListView,
    CountryDetailView,
    SameRegionCountriesWithLanguagesView,
)

urlpatterns = [
    path("<str:cca2>", country_summary_view, name="country_summary"),
    path("", CountryListView.as_view(), name="country-list"),
    path(
        "<int:pk>/",
        CountryDetailView.as_view(),
        name="country-detail",
    ),
    path(
        "<int:pk>/related/",
        SameRegionCountriesWithLanguagesView.as_view(),
        name="same-region-languages",
    ),
]
