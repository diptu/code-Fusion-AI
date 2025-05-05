from django.urls import path
from .views import (
    CountryListView,
    CountryCreateView,
    CountryDetailView,
    CountryUpdateView,
    CountryDeleteView,
)

urlpatterns = [
    path("countries/", CountryListView.as_view(), name="country-list"),
    path("countries/create/", CountryCreateView.as_view(), name="country-create"),
    path(
        "countries/<str:name_common>/update/",
        CountryUpdateView.as_view(),
        name="country-update",
    ),
    path(
        "countries/<str:name_common>/",
        CountryDetailView.as_view(),
        name="country-detail",
    ),
    # path(
    #     "countries/<str:name_common>/",
    #     CountryDeleteView.as_view(),
    #     name="country-delete",
    # ),
]
