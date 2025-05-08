from django.urls import path
from .views import (
    CountryListView,
    CountryCreateView,
    CountryDetailView,
    CountryUpdateView,
    CountrySearchByNameView,
    CountriesInSameRegionView,
    CountriesBySpokenLanguageView,
    CountryDeleteView,
)

app_name = "countries"

urlpatterns = [
    # GET /api/country/
    path("", CountryListView.as_view(), name="country-list"),
    # /api/country/search/?name_common=pak
    path(
        "search/",
        CountrySearchByNameView.as_view(),
        name="country-search-by-name",
    ),
    # /api/country/region/?region=Africa
    path(
        "region/",
        CountriesInSameRegionView.as_view(),
        name="same-region-countries",
    ),
    # GET: /api/country/language/?ln=spanish
    path(
        "language/",
        CountriesBySpokenLanguageView.as_view(),
        name="countries-by-language",
    ),
    #  POST api/country/create/
    path("create/", CountryCreateView.as_view(), name="country-create"),
    # PUT /api/country/update/Norway
    path(
        "update/<str:name_common>/",
        CountryUpdateView.as_view(),
        name="country-update",
    ),
    # GET /api/country/Lithuania/
    path(
        "<str:name_common>/",
        CountryDetailView.as_view(),
        name="country-detail",
    ),
    path("<int:item_id>", CountryDeleteView.as_view(), name="country-delete"),
]
