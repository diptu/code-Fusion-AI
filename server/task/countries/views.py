from django.http import HttpResponse
from countries.models import Country


def country_summary_view(request, *args, **kwargs):
    cca2 = kwargs.get("cca2")
    if not cca2:
        return HttpResponse("Missing 'cca2' parameter.", status=400)

    try:
        country = Country.objects.get(cca2=cca2.upper())
        return HttpResponse(f"<pre>{country.summary}</pre>")
    except Country.DoesNotExist:
        return HttpResponse("Country not found", status=404)
