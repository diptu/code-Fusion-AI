# countries/utils.py

import requests
import logging
from django.core.exceptions import ValidationError
from countries.models import Country

logger = logging.getLogger(__name__)


def fetch_and_store_countries():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)

    if response.status_code != 200:
        logger.error("Failed to fetch data from API")
        return

    countries_data = response.json()
    logger.info(f"Fetched {len(countries_data)} countries")

    for data in countries_data:
        country_data = {
            "cca2": data.get("cca2"),
            "cca3": data.get("cca3"),
            "ccn3": data.get("ccn3"),
            "cioc": data.get("cioc"),
            "fifa": data.get("fifa"),
            "name_common": data.get("name", {}).get("common"),
            "name_official": data.get("name", {}).get("official"),
            "native_name": data.get("name", {}).get("nativeName"),
            "region": data.get("region"),
            "subregion": data.get("subregion"),
            "latlng": data.get("latlng"),
            "capital_info": data.get("capitalInfo"),
            "area": data.get("area"),
            "landlocked": data.get("landlocked"),
            "capital": data.get("capital"),
            "borders": data.get("borders"),
            "tld": data.get("tld"),
            "languages": data.get("languages"),
            "currencies": data.get("currencies"),
            "demonyms": data.get("demonyms"),
            "flag": data.get("flag"),
            "flags": data.get("flags"),
            "coat_of_arms": data.get("coatOfArms"),
            "maps": data.get("maps"),
            "gini": data.get("gini"),
            "car": data.get("car"),
            "idd": data.get("idd"),
            "alt_spellings": data.get("altSpellings"),
            "status": data.get("status"),
            "un_member": data.get("unMember", False),
            "independent": data.get("independent", False),
            "start_of_week": data.get("startOfWeek"),
            "population": data.get("population"),
            "timezones": data.get("timezones"),
            "continents": data.get("continents"),
            "translations": data.get("translations"),
            "postal_code": data.get("postalCode"),
        }

        # Create in-memory instance to test validity
        country = Country(**country_data)
        try:
            country.full_clean()  # Validates all fields
            country.save()
            logger.info(f"Saved: {country.name_common}")
        except ValidationError as e:
            logger.warning(
                f"Validation failed for {country_data.get('name_common')}: {e.message_dict}"
            )
        except Exception as e:
            logger.error(
                f"Unexpected error while saving {country_data.get('name_common')}: {str(e)}"
            )
