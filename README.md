# GeoInsightFetcher

### NOTE:
I could not find an API that would allow me to get the currency and country by one request. Therefore, I had to use several services

At first, I try to get the country code by city
('https://public.opendatasoft.com/explore/dataset/worldcitiespop/api/?disjunctive.country')
(Also I get geolocation like addition field)

Next, I take the code, and get the country name with currency.
('https://restcountries.eu/')

In settings.py you can find the constants.



### Launch:
1. pip install -r requirements.txt

2. python main.py -h -> for help

2.1. python main.py Kyiv -> for info

2.2 python main.py kyiv, dnipro, london -> for multiply cities