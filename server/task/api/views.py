from countries.models import Country
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CountrySerializer


class CountryListView(generics.ListAPIView):
    """
    API endpoint that returns a list of all countries.

    This view provides a read-only list of country data using the CountrySerializer.
    It uses 'name_common' as the lookup field for individual country identification in other views.

    Returns:
        A list of serialized country objects with complete details for each.

    Example:
        GET /api/country/
    """

    permission_classes = [AllowAny]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "name_common"


# Filter by name_common
class CountryDetailView(generics.RetrieveAPIView):
    """
    API endpoint that retrieves detailed information about a single country.

    Lookup Field:
        name_common (str): The common name of the country to retrieve.

    Returns:
        A serialized representation of the specified country's full data.

    Example:
        GET /api/country/Lithuania/
    """

    permission_classes = [IsAuthenticated]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "name_common"  # or "pk", or another field like "cca2"


class CountryCreateView(generics.CreateAPIView):
    """
    API endpoint for creating a new country record.

    This view accepts POST requests with the country data and creates a new
    country entry in the database. The request payload should contain the
    necessary country information to be saved.

    Example request body:
        {
            "cca2": "LT",
            "cca3": "LTU",
            "ccn3": "440",
            "cioc": "LTU",
            "fifa": "LT",
            "name_common": "Lithuania",
            "name_official": "Republic of Lithuania",
            "native_name": {"lt": "Lietuva"},
            "region": "Europe",
            "subregion": "Northern Europe",
            "languages": {"lt": "Lithuanian"},
            "population": 2722289,
            ...
        }

    Responses:
        - 201: Country created successfully.
        - 400: Bad request if the data is invalid or incomplete.

    Example:
        -  POST api/country/create/
    """

    permission_classes = [IsAuthenticated]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def perform_create(self, serializer):
        # Check if the user is a superuser before saving
        if not self.request.user.is_superuser:
            raise PermissionDenied("You must be a superuser to create a country.")

        # Save the country if the user is a superuser
        serializer.save()


class CountryUpdateView(generics.RetrieveUpdateAPIView):
    """
    API endpoint to retrieve and update a Country instance by its 'name_common' field.

    Methods:
        - GET: Retrieve country details by 'name_common'.
        - PUT/PATCH: Update the specified country's data.

    Path Parameters:
        name_common (str): The common name of the country to retrieve or update.

    Responses:
        200 OK: Successfully retrieved or updated the country.
        404 Not Found: No country found with the provided 'name_common'.

    Example:
        GET /api/country/update/Norway/
        PUT /api/country/update/Norway/
    """

    permission_classes = [IsAuthenticated]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "name_common"

    def get_object(self):
        name_common = self.kwargs.get(self.lookup_field)
        try:
            return Country.objects.get(name_common=name_common)
        except Country.DoesNotExist:
            raise NotFound(detail="Country with the specified name_common not found.")

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except NotFound as e:
            return Response({"error": str(e.detail)}, status=status.HTTP_404_NOT_FOUND)


class CountryDeleteView(APIView):
    """
    API endpoint to delete a specific country by its database ID.

    Method:
        DELETE

    URL Params:
        item_id (int): The primary key (ID) of the country to be deleted.

    Responses:
        204 No Content: Successfully deleted the country.
        404 Not Found: No country found with the given ID.

    Example:
        DELETE /api/countries/1/
    """

    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def delete(self, request, item_id):
        # Check if the user is a superuser
        if not request.user.is_superuser:
            return Response(
                {"error": "You do not have permission to delete this country."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            country = Country.objects.get(id=item_id)
        except Country.DoesNotExist:
            return Response(
                {"error": "Country not found."}, status=status.HTTP_404_NOT_FOUND
            )

        country.delete()
        return Response(
            {"message": "Country deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class CountrySearchByNameView(generics.ListAPIView):
    """
    API endpoint to search for countries by their common name (supports partial matches).

    Query Parameters:
        name_common (str): A partial or full country name to search for (case-insensitive).

    Returns:
        200 OK: A list of country objects that match the search query.
        400 Bad Request: If the query parameter is invalid (optional handling).
        500 Internal Server Error: If an unexpected error occurs on the server.

    Example:
        GET /api/country/search/?name_common=lit

    """

    serializer_class = CountrySerializer

    def get_queryset(self):
        queryset = Country.objects.all()
        name_query = self.request.query_params.get("name_common", None)
        if name_query:
            queryset = queryset.filter(name_common__icontains=name_query)
        return queryset


class CountriesInSameRegionView(generics.ListAPIView):
    """
    API endpoint that returns a list of countries in the specified region.

    Query Parameters:
        region (str): The name of the region (e.g., Africa, Europe).

    Example:
        GET /api/country/region/?region=Africa

    Returns:
        200 OK: A list of countries in the specified region.
        400 Bad Request: If no region is provided.
    """

    serializer_class = CountrySerializer

    def get_queryset(self):
        region = self.request.query_params.get("region", "").strip()
        if not region:
            return Country.objects.none()
        return Country.objects.filter(region__iexact=region)


class CountriesBySpokenLanguageView(generics.ListAPIView):
    """
    API endpoint that returns a sorted list of country names where a specified language is spoken.

    Query Parameters:
        ln (str): The name (or partial name) of a language to filter countries by (case-insensitive).

    Behavior:
        - Filters countries where the 'languages' JSONField contains the given language string.
        - Matches are case-insensitive and partial.
        - Returns only the 'name_common' field (country names).
        - Result is sorted alphabetically in ascending order.

    Example:
        GET /api/country/language/?lang=span

    Responses:
        200 OK: Returns a list of country names.
            Example:
            [
                "Argentina",
                "Chile",
                "Spain"
            ]

        400 Bad Request: If the 'ln' parameter is missing or malformed
                        (not explicitly handled here, returns empty list).
    """

    def get_queryset(self):
        language_query = self.request.query_params.get("lang", "").strip().lower()

        if not language_query:
            return Country.objects.none()

        matching_countries = []
        for country in Country.objects.exclude(languages=None):
            language_values = country.languages.values()
            if any(language_query in value.lower() for value in language_values):
                matching_countries.append(country)

        return matching_countries

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        name_list = [country.name_common for country in queryset]
        name_list.sort()  # Sort alphabetically in ascending order
        return Response(name_list)
