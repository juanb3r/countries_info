import hashlib
import json
import random
import requests
import pandas as pd

from datetime import datetime
from service.create_bd import create_connection, create_table


def get_regions() -> list:
    """Get all region in the world using restcountries API

    Returns:
        list: Contains all region
    """

    url: str = "https://restcountries-v1.p.rapidapi.com/all"

    headers: dict = {
        'x-rapidapi-key': "30a5e9327bmshd228acc97626ebfp1635cbjsn541e99aa03bc",
        'x-rapidapi-host': "restcountries-v1.p.rapidapi.com"
    }

    response_countries = requests.request("GET", url, headers=headers)
    countries: list = json.loads(response_countries.text)

    regions = [country["region"] for country in countries]
    regions = set(regions)
    regions = [region for region in regions if region != ""]
    regions = sorted(regions)
    return regions


def get_one_country_per_region(regions: list) -> tuple:
    """Get one country randomly per region

    Args:
        regions (list): All regions in the world

    Returns:
        tuple: countries located at different regions and
        their query time
    """

    url: str = "https://restcountries.eu/rest/v2/region/"
    countries_per_region: list = []
    time_request: list = []
    for region in regions:
        now = datetime.now()
        timestamp_now = datetime.timestamp(now)
        countries = json.loads(requests.request("GET", url+region).text)
        select_random_country_by_index = random.randint(0, len(countries)-1)
        countries_per_region.append(countries[select_random_country_by_index])
        later = datetime.now()
        timestamp_later = datetime.timestamp(later)
        time_request.append(round(timestamp_later - timestamp_now, 2))

    return (countries_per_region, time_request)


def get_country_name(countries: list) -> list:
    """Get country name

    Args:
        countries (list): All countries in the world

    Returns:
        list: country's name
    """
    countries_name: list = [country["name"] for country in countries]

    return countries_name


def get_languege_by_country_encode(countries: list) -> list:
    """Get language by country

    Args:
        countries (list): List with different countries
        located at different regions

    Returns:
        List: Langueges spoken in those countries
    """

    languages: list = [country["languages"][0]["name"]
                       for country in countries]
    languages_encode: list = []
    for language in languages:
        language_encode = hashlib.sha1()
        language_encode.update(language.encode("utf-8"))
        languages_encode.append(language_encode.hexdigest().upper())

    return languages_encode


def set_data_dict() -> list:
    """Create a dictionary with all the data

    Returns:
        list: dictionary with info by countries and its region
    """
    regions: list = get_regions()
    countries, times = get_one_country_per_region(regions)
    languages: list = get_languege_by_country_encode(countries)
    countries_name: list = get_country_name(countries)

    data_list: list = []

    for index in range(0, len(regions)-1):

        data_list.append({
            "region": regions[index],
            "country": countries_name[index],
            "language": languages[index],
            "time": times[index]})

    return data_list


def save_data_in_db(conn, data_list: list) -> None:
    """Save data in the countries table

    Args:
        conn (sqllite.connect): Connection to bd
        data_list (list): countries data with their keys
    """
    for data in data_list:
        conn.execute(
            "INSERT INTO countries(region, country, language, time)\
                VALUES (:region, :country, :language, :time)",
            data)
        conn.commit()


def display(conn) -> None:
    """ Create a query to see what is inside the countries table
        Using pandas library 

    Args:
        conn ([type]): [description]
    """
    data_pd = pd.read_sql('SELECT * FROM countries', conn)
    print(data_pd)


def main():
    data_countries = set_data_dict()
    df = pd.DataFrame.from_dict(data_countries)
    print(df)
    df_time = df["time"]
    print(f"Total: {df_time.sum()}, Mean: {df_time.mean()},"
          + f"Max: {df_time.max()}, Min: {df_time.min()}")

    countries_json = json.dumps(data_countries)
    countries_json_file = open("data.json", "w")
    countries_json_file.write(countries_json)
    countries_json_file.close()

    conn = create_connection('countries_db')
    create_table(conn)
    save_data_in_db(conn, data_countries)
    # ! Use only if you want to see database data "display(conn)"
    conn.close()


if __name__ == '__main__':
    main()
