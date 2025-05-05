from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from countries.models import Country


class CountryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alabasta_data = {
            "cca2": "AB",
            "cca3": "ALB",
            "ccn3": None,
            "cioc": None,
            "fifa": None,
            "name_common": "Alabasta",
            "name_official": "Alabasta Kingdom",
            "native_name": None,
            "region": "Grand Line",
            "subregion": "Paradise",
            "latlng": [22.0, 23.0],
            "capital_info": None,
            "area": None,
            "landlocked": True,
            "capital": ["Alubarna"],
            "borders": ["Drum Kingdom", "Dressrosa"],
            "tld": [".ab"],
            "languages": {"abs": "Alabastian"},
            "currencies": {"BEL": {"name": "Beli", "symbol": "B"}},
            "demonyms": {"eng": {"f": "Alabastian", "m": "Alabastian"}},
            "flag": None,
            "flags": None,
            "coat_of_arms": None,
            "maps": None,
            "gini": None,
            "car": None,
            "idd": None,
            "alt_spellings": ["Arabasta"],
            "status": "Kingdom",
            "un_member": False,
            "independent": True,
            "start_of_week": "sunday",
            "population": 10000000,
            "timezones": ["UTC+0"],
            "continents": ["Grand Line"],
            "translations": {
                "eng": {"official": "Alabasta Kingdom", "common": "Alabasta"},
                "jpn": {"official": "アラバスタ王国", "common": "アラバスタ"},
            },
            "postal_code": None,
        }
        cls.alabasta = Country.objects.create(**cls.alabasta_data)

        cls.drum_kingdom_data = {
            "cca2": "DK",
            "cca3": "DRK",
            "name_common": "Drum Kingdom",
            "name_official": "Drum Kingdom",
            "independent": True,
        }
        cls.drum_kingdom = Country.objects.create(**cls.drum_kingdom_data)

        cls.dressrosa_data = {
            "cca2": "DR",
            "cca3": "DRS",
            "name_common": "Dressrosa",
            "name_official": "Kingdom of Dressrosa",
            "independent": True,
        }
        cls.dressrosa = Country.objects.create(**cls.dressrosa_data)

    def test_country_creation(self):
        self.assertIsNotNone(self.alabasta.id)
        self.assertEqual(Country.objects.count(), 3)
        self.assertEqual(self.alabasta.name_common, "Alabasta")
        self.assertEqual(self.alabasta.cca2, "AB")

    def test_cca2_unique(self):
        with self.assertRaises(IntegrityError):
            Country.objects.create(
                cca2="AB", cca3="ALB2", name_common="Duplicate Alabasta"
            )

    def test_cca3_unique(self):
        with self.assertRaises(IntegrityError):
            Country.objects.create(
                cca2="XX", cca3="ALB", name_common="Another Alabasta"
            )

    def test_name_common_unique(self):
        with self.assertRaises(IntegrityError):
            Country.objects.create(cca2="XX", cca3="XXA", name_common="Alabasta")

    def test_name_official_unique(self):
        with self.assertRaises(IntegrityError):
            Country.objects.create(
                cca2="YY", cca3="YYA", name_official="Alabasta Kingdom"
            )

    def test_str_method(self):
        self.assertEqual(str(self.alabasta), "Alabasta")

    def test_summary_contains_all_expected_data(self):
        summary = self.alabasta.summary
        self.assertIn(f"Country: {self.alabasta.name_common}", summary)
        self.assertIn(f"Official Name: {self.alabasta.name_official}", summary)
        self.assertIn(
            f"Region/Subregion: {self.alabasta.region}/{self.alabasta.subregion}",
            summary,
        )
        self.assertIn(f"Population: {self.alabasta.population}", summary)
        self.assertIn(f"Capital: {', '.join(self.alabasta.capital)}", summary)
        self.assertIn(f"Borders: {', '.join(self.alabasta.borders)}", summary)
        self.assertIn(
            f"Languages: {', '.join(self.alabasta.languages.values())}", summary
        )
        self.assertIn(f"Currency: {self.alabasta.currencies['BEL']['name']}", summary)
        self.assertIn("Latitude: 22.0", summary)
        self.assertIn("Longitude: 23.0", summary)

    def test_summary_with_missing_data(self):
        empty_country = Country.objects.create(
            cca2="ZZ",
            cca3="ZZZ",
            name_common="Empty Island",
            name_official="Empty Territory",
        )
        summary = empty_country.summary
        self.assertIn("Languages: N/A", summary)
        self.assertIn("Currency: N/A", summary)
        self.assertIn("LatLon: N/A", summary)
        self.assertIn("Capital: ", summary)
        self.assertIn("Borders: ", summary)
        self.assertIn("Population: None", summary)
        self.assertIn(f"Region/Subregion: None/None", summary)

    def test_latlng_formatting(self):
        self.assertIn("Latitude: 22.0", self.alabasta.summary)
        self.assertIn("Longitude: 23.0", self.alabasta.summary)

    def test_language_parsing(self):
        self.assertEqual(", ".join(self.alabasta.languages.values()), "Alabastian")

    def test_currency_parsing(self):
        currencies = self.alabasta.currencies
        currency_names = ", ".join(v["name"] for v in currencies.values())
        self.assertIn("Beli", currency_names)

    def test_created_at_is_auto_populated(self):
        self.assertIsNotNone(self.alabasta.created_at)
        self.assertLessEqual(self.alabasta.created_at, timezone.now())

    def test_updated_at_is_auto_populated_on_creation(self):
        self.assertIsNotNone(self.alabasta.updated_at)
        self.assertLessEqual(self.alabasta.updated_at, timezone.now())

    def test_updated_at_is_updated_on_save(self):
        initial_updated_at = self.alabasta.updated_at
        self.alabasta.population = 11000000
        self.alabasta.save()
        self.alabasta.refresh_from_db()
        self.assertGreater(self.alabasta.updated_at, initial_updated_at)

    def test_boolean_fields_default_value(self):
        new_country = Country.objects.create(
            cca2="XXA",
            cca3="XXB",
            name_common="New Island",
            name_official="New Territory",
        )
        self.assertFalse(new_country.landlocked)
        self.assertFalse(new_country.un_member)
        self.assertFalse(new_country.independent)

    def test_nullable_blankable_fields(self):
        country_partial = Country.objects.create(
            cca2="YYB",
            cca3="YYC",
            name_common="Partial Island",
            name_official="Partial Land",
        )
        self.assertIsNone(country_partial.ccn3)
        self.assertIsNone(country_partial.cioc)
        self.assertIsNone(country_partial.fifa)
        self.assertIsNone(country_partial.native_name)
        self.assertIsNone(country_partial.region)
        self.assertIsNone(country_partial.subregion)
        self.assertIsNone(country_partial.latlng)
        self.assertIsNone(country_partial.capital_info)
        self.assertIsNone(country_partial.area)
        self.assertIsNone(country_partial.capital)
        self.assertIsNone(country_partial.borders)
        self.assertIsNone(country_partial.tld)
        self.assertIsNone(country_partial.languages)
        self.assertIsNone(country_partial.currencies)
        self.assertIsNone(country_partial.demonyms)
        self.assertIsNone(country_partial.flag)
        self.assertIsNone(country_partial.flags)
        self.assertIsNone(country_partial.coat_of_arms)
        self.assertIsNone(country_partial.maps)
        self.assertIsNone(country_partial.gini)
        self.assertIsNone(country_partial.car)
        self.assertIsNone(country_partial.idd)
        self.assertIsNone(country_partial.alt_spellings)
        self.assertIsNone(country_partial.status)
        self.assertIsNone(country_partial.start_of_week)
        self.assertIsNone(country_partial.population)
        self.assertIsNone(country_partial.timezones)
        self.assertIsNone(country_partial.continents)
        self.assertIsNone(country_partial.translations)
        self.assertIsNone(country_partial.postal_code)

    def test_start_of_week_choices(self):
        valid_choices = ["monday", "sunday", "saturday"]
        for choice in valid_choices:
            country = Country.objects.create(
                cca2=f"{choice[:2].upper()}C",
                cca3=f"{choice[:3].upper()}",
                name_common=f"{choice.capitalize()} Island",
                name_official=f"{choice.capitalize()} Territory",
                start_of_week=choice,
            )
            self.assertEqual(country.start_of_week, choice)

        invalid_country = Country(
            cca2="INV",
            cca3="INVD",
            name_common="Invalid Land",
            name_official="Invalid State",
            start_of_week="tuesday",
        )
        with self.assertRaises(ValidationError) as cm:
            invalid_country.full_clean()
        self.assertIn("start_of_week", cm.exception.message_dict)
