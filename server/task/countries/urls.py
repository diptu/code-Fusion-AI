from django.urls import path
from countries.views import country_summary_view
from .views import CountryListView, CountryDetailView

urlpatterns = [
    path("<str:cca2>", country_summary_view, name="country_summary"),
    path("", CountryListView.as_view(), name="country-list"),
    path(
        "<int:pk>/",
        CountryDetailView.as_view(),
        name="country-detail",
    ),
]
