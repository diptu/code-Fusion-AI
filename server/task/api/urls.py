from django.urls import path
from .views import (
    CountryListView,
    CountryCreateView,
    CountryDetailView,
    CountryUpdateView,
    CountrySearchByNameView,
    CountriesInSameRegionView,
    CountriesByLanguageView,
    CountryDeleteView,
)

app_name = "countries"

urlpatterns = [
    # GET /api/countries/
    path("", CountryListView.as_view(), name="country-list"),
    # /api/countries/search/?name_common=pak
    path(
        "search/",
        CountrySearchByNameView.as_view(),
        name="country-search-by-name",
    ),
    # /api/countries/region/?region=Africa
    path(
        "region/",
        CountriesInSameRegionView.as_view(),
        name="same-region-countries",
    ),
    # GET: /api/countries/language/?ln=spanish
    path(
        "language/",
        CountriesByLanguageView.as_view(),
        name="countries-by-language",
    ),
    #  POST api/countries/create/
    path("create/", CountryCreateView.as_view(), name="country-create"),
    # PUT /api/countries/update/Norway
    path(
        "update/<str:name_common>/",
        CountryUpdateView.as_view(),
        name="country-update",
    ),
    # GET /api/countries/Lithuania/
    path(
        "<str:name_common>/",
        CountryDetailView.as_view(),
        name="country-detail",
    ),
    path("<int:item_id>", CountryDeleteView.as_view(), name="country-delete"),
]
