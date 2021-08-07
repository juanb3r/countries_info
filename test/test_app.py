import hashlib
import json
from service.app import get_regions, get_one_country_per_region,\
    get_country_name, get_languege_by_country_encode


def test_get_regions():

    regions_test = ["Africa", "Americas", "Asia", "Europe", "Oceania", "Polar"]

    regions = get_regions()

    assert regions_test == regions


def test_get_country_per_region_africa():

    region = ["Africa"]

    country = get_one_country_per_region(region)

    assert region[0] == country[0][0]['region']


def test_get_country_per_region_americas():

    region = ["Americas"]

    country = get_one_country_per_region(region)

    assert region[0] == country[0][0]['region']


def test_get_country_per_region_asia():

    region = ["Asia"]

    country = get_one_country_per_region(region)

    assert region[0] == country[0][0]['region']


def test_get_country_per_region_europe():

    region = ["Europe"]

    country = get_one_country_per_region(region)

    assert region[0] == country[0][0]['region']


def test_get_country_per_region_oceania():

    region = ["Oceania"]

    country = get_one_country_per_region(region)

    assert region[0] == country[0][0]['region']


def test_get_country_per_region_polar():

    region = ["Polar"]

    country = get_one_country_per_region(region)

    assert region[0] == country[0][0]['region']


def test_get_languege_by_country_encode():

    language_test = 'Spanish'
    language_encode = hashlib.sha1()
    language_encode.update(language_test.encode("utf-8"))
    language_test_encode = language_encode.hexdigest().upper()
    countries_file = open("test/settings/getting-countries.json", "r")
    country_dict = json.loads(countries_file.read())
    americas_country = country_dict[2]
    country_data = [americas_country["Americas"]]
    countries_file.close()

    language_encode = get_languege_by_country_encode(country_data)

    assert language_test_encode == language_encode[0]


def test_get_country_name():

    country_name_test = 'Albania'
    countries_file = open("test/settings/getting-countries.json", "r")
    country_dict = json.loads(countries_file.read())
    europe_country = country_dict[0]
    country_data = [europe_country["Europe"]]
    countries_file.close()

    country_name = get_country_name(country_data)

    assert country_name_test == country_name[0]
