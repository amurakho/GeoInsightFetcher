import logging

BASE_CITY_URL = 'https://public.opendatasoft.com/api/records/1.0/search/?dataset=worldcitiespop&q={}&facet=country'

BASE_CURRENCY_URL = 'https://restcountries.eu/rest/v2/name/{}?fullText=true'

HELP_TEXT = """
-> python main.py <CITY_NAME>

If you want to check multiply cities you should separate it by comma(",")
-> python main.py <CITY_NAME>, <CITY_NAME>, <CITY_NAME>
"""

LOGLEVEL = logging.INFO