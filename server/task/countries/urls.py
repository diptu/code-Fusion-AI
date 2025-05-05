from django.urls import path
from countries.views import country_summary_view

urlpatterns = [
    path("<str:cca2>", country_summary_view, name="country_summary"),
]
