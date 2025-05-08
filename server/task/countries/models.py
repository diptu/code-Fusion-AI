from django.db import models
from django.urls import reverse
from django.utils import timezone


class Country(models.Model):
    # Basic Identifiers
    cca2 = models.CharField(
        max_length=3,
        unique=True,
        help_text="ISO 3166-1 alpha-2 two-letter country codes",
        db_index=True,
    )
    cca3 = models.CharField(
        max_length=3,
        unique=True,
        help_text="ISO 3166-1 alpha-3 three-letter country codes",
        db_index=True,
    )
    ccn3 = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        help_text="ISO 3166-1 numeric code (UN M49)",
    )
    cioc = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Code of the International Olympic Committee",
    )
    fifa = models.CharField(max_length=10, null=True, blank=True, help_text="FIFA code")

    # Names
    name_common = models.CharField(
        max_length=255, unique=True, help_text="common country name", db_index=True
    )
    name_official = models.CharField(
        max_length=255, unique=True, help_text="Official country name", db_index=True
    )
    native_name = models.JSONField(
        null=True, blank=True, help_text="Native country name"
    )

    # Geo Info
    region = models.CharField(
        max_length=100, null=True, blank=True, help_text="UN demographic regions"
    )
    subregion = models.CharField(
        max_length=100, null=True, blank=True, help_text="UN demographic subregions"
    )
    latlng = models.JSONField(null=True, blank=True, help_text="Latitude and longitude")
    capital_info = models.JSONField(null=True, blank=True, help_text="Capital cities")
    area = models.FloatField(null=True, blank=True, help_text="Geographical size")
    landlocked = models.BooleanField(default=False, help_text="Landlocked country")

    # Capital, Borders, TLDs
    capital = models.JSONField(
        null=True, blank=True, help_text="Capital latitude and longitude"
    )
    borders = models.JSONField(null=True, blank=True, help_text="Border countries")
    tld = models.JSONField(
        null=True, blank=True, help_text="Internet top level domains"
    )

    # Languages, Currencies, Demonyms
    languages = models.JSONField(
        null=True, blank=True, help_text="List of official languages"
    )
    currencies = models.JSONField(
        null=True, blank=True, help_text="List of all currencies"
    )
    demonyms = models.JSONField(
        null=True, blank=True, help_text="Genderized inhabitants of the country"
    )

    # Flags, Coat of Arms, Maps
    flag = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Link to the svg flag on Flagpedia, v3: flag emoji",
    )
    flags = models.JSONField(
        null=True, blank=True, help_text="Flagpedia links to svg and png flags"
    )
    coat_of_arms = models.JSONField(
        null=True, blank=True, help_text="MainFacts.com links to svg and png images"
    )
    maps = models.JSONField(
        null=True, blank=True, help_text="Link to Google maps and Open Street maps"
    )

    # Additional info
    gini = models.JSONField(null=True, blank=True, help_text="Worldbank Gini index")
    car = models.JSONField(
        null=True,
        blank=True,
        help_text="Car distinguised (oval) signs, Car driving side",
    )
    idd = models.JSONField(
        null=True, blank=True, help_text="International dialing codes"
    )
    alt_spellings = models.JSONField(
        null=True, blank=True, help_text="Alternate spellings of the country name"
    )
    status = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="ISO 3166-1 independence status (the country is considered a sovereign state)",
    )
    un_member = models.BooleanField(default=False, help_text="UN Member status")
    independent = models.BooleanField(
        default=False,
        help_text="SO 3166-1 independence status (the country is considered a sovereign state)",
    )
    start_of_week = models.CharField(
        max_length=20,
        choices=[("monday", "Monday"), ("sunday", "Sunday"), ("saturday", "Saturday")],
        null=True,
        blank=True,
        help_text="Day the week starts on",
    )
    population = models.BigIntegerField(
        null=True, blank=True, help_text="Country population"
    )
    timezones = models.JSONField(null=True, blank=True, help_text="Timezones")
    continents = models.JSONField(
        null=True, blank=True, help_text="List of continents the country is on"
    )
    translations = models.JSONField(
        null=True, blank=True, help_text="List of country name translations"
    )
    postal_code = models.JSONField(
        null=True, blank=True, help_text="Country postal codes"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text="Timestamp when this country record was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=True,
        help_text="Timestamp when this country record was last updated",
    )

    def __str__(self):
        return self.name_common

    def get_absolute_url(self):
        return reverse(
            "travel:detail", kwargs={"pk": self.pk}
        )  # f"/transportation/{self.pk}"

    @property
    def summary(self):
        languages = (
            ", ".join(self.languages.values())
            if isinstance(self.languages, dict)
            else "N/A"
        )
        currencies = (
            ", ".join(v.get("name", "") for v in self.currencies.values())
            if isinstance(self.currencies, dict)
            else "N/A"
        )
        latlng = (
            f"Latitude: {self.latlng[0]}, Longitude: {self.latlng[1]}"
            if isinstance(self.latlng, list) and len(self.latlng) == 2
            else "LatLon: N/A"
        )

        return (
            f"Country: {self.name_common}\n"
            f"Official Name: {self.name_official}\n"
            f"Region/Subregion: {self.region}/{self.subregion}\n"
            f"Population: {self.population}\n"
            f"Capital: {', '.join(self.capital or [])}\n"
            f"Borders: {', '.join(self.borders or [])}\n"
            f"Languages: {languages}\n"
            f"Currency: {currencies}\n"
            f"{latlng}"
        )

    @property
    def language(self):
        """
        Returns a list of language names from the 'languages' JSON field.

        Example:
            If languages = {"eng": "English", "fra": "French"}, returns ["English", "French"]

        Returns:
            list[str]: List of language names or an empty list if not available.
        """
        if isinstance(self.languages, dict):
            return list(self.languages.values())
        return []

    @property
    def neighbour(self):
        """
        Returns a queryset of Country objects that share a border with this one.
        """
        if isinstance(self.borders, dict):
            return list(self.borders.values())
        return []

    @property
    def shared_borders(self):
        if not self.borders:
            return Country.objects.none()
        return Country.objects.filter(cca3__in=self.borders)

    @property
    def population_density(self):
        """
        Returns the population density (people per square kilometer).

        Returns:
            float | str: Density value or "N/A" if population or area is missing.
        """
        if self.population and self.area and self.area > 0:
            return round(self.population / self.area, 2)
        return "N/A"

    @property
    def primary_currency(self):
        """
        Returns the first listed currency name.

        Returns:
            str
        """
        if isinstance(self.currencies, dict) and self.currencies:
            return next(iter(self.currencies.values())).get("name", "N/A")
        return "N/A"

    @property
    def local_weekend(self):
        """
        Guesses typical weekend days based on the region.

        Returns:
            str
        """
        if self.region == "Middle East":
            return "Friday-Saturday"
        elif self.region == "Asia" and self.subregion == "South-Eastern Asia":
            return "Saturday-Sunday"
        else:
            return "Saturday-Sunday"

    @property
    def spoken_language(self):
        """
        Returns a human-friendly, comma-separated string of spoken languages.

        Returns:
            str: Languages spoken in a readable format.
        """
        languages = self.spoken_language
        if not languages:
            return "No official languages listed"
        if len(languages) == 1:
            return languages[0]
        if len(languages) == 2:
            return f"{languages[0]} and {languages[1]}"
        return f"{', '.join(languages[:-1])}, and {languages[-1]}"
