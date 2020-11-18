import time
import logging
import json
import sys

import requests

from exceptions import CantGetCountyError, WrongCityError, HaveNoCitiesError
from settings import HELP_TEXT, LOGLEVEL, BASE_CITY_URL, BASE_CURRENCY_URL

logging.basicConfig(level=LOGLEVEL)


def parse_country_from_data(response):
    """
        Example of JSON

        ...
        "records":
        [
            {
                "datasetid": "worldcitiespop",
                "recordid": "d3d956f52c963af24dd14c1d6ab363c2f5a811e6",
                 "fields":
                    {
                        "city": "kyiv",
                        "country": "ua",
                        "region": "12",
                        "geopoint": [50.433333, 30.516667],
                        "longitude": 30.516667,
                        "latitude": 50.433333,
                        "accentcity": "Kyiv"
                    },
            ...
            }
            ...
        ]
        ...

    """
    data = json.loads(response.text)

    data = data.get('records')
    if not data:
        raise WrongCityError('Wrong city, check it and try again')

    data = {
        'country_code': data[0]['fields']['country'],
        'geolocaion': data[0]['fields']['geopoint']
    }

    return data


def get_country_by_city(city, attempts=3):
    """
    Try to find country.

    If it does not find -> exception

    """
    response = requests.get(BASE_CITY_URL.format(city))

    # Retry if wrong status code
    if response.status_code != 200 and attempts:
        logging.debug(f'Cannt get country. Repeat. Attemps: {attempts}')
        time.sleep(5)
        return get_country_by_city(city, attempts=attempts-1)

    elif not attempts:
        raise CantGetCountyError('Can not contact the server. Try again later')
    
    else:
        return parse_country_from_data(response)


def get_currency_by_country(country_data):
    """
        Example JSON:

        [
            ...
            "currencies":[
                    {"code":"UAH","name":"Ukrainian hryvnia","symbol":"₴"}
                ],
            ...
        ]
    """
    country = country_data['country_code']
    response = requests.get(BASE_CURRENCY_URL.format(country))

    data = json.loads(response.text)[0]
    return data['name'], [currency['code'] for currency in data['currencies']]


def parse_argv():
    argv = sys.argv[1:]

    if argv[0] == '-h':
        print(HELP_TEXT)
        exit(0)

    cities = ' '.join(argv)
    if not cities:
        raise HaveNoCitiesError('You should write some city')

    cities = cities.split(',')

    return cities

def main():
    """
        -Take a city from command line
        -Get country code by city
        -Get country name and currency by country code
    """

    cities = parse_argv()

    for city in cities:
        data = get_country_by_city(city)

        data['country'], data['currency'] = get_currency_by_country(data)

        print(data)


if __name__ == '__main__':
    main()