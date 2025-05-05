from rest_framework import generics
from countries.models import Country
from .serializers import CountrySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "name_common"


class CountryCreateView(generics.CreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


# Filter by name_common
class CountryDetailView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "name_common"  # or "pk", or another field like "cca2"


# Update by name_common
class CountryUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "name_common"


# class CountryDeleteView(APIView):
#     permission_classes = [AllowAny]

#     def delete(self, request, name_common, *args, **kwargs):
#         try:
#             country = Country.objects.get(name_common=name_common)
#             country.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Country.DoesNotExist:
#             return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
