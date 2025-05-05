from rest_framework import serializers
from countries.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"  # or list specific fields you want to allow
