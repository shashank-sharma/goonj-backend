import requests
import json
import datetime


from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from rest_framework.views import APIView
from rest_framework.response import Response

from .disease import extract_pdf_to_dict, get_all_pdf, download_pdf
from .imdalerts import earthquake_status

from backend.settings import STATIC_ROOT

# City data consist of City name with it's unique code which is useful
# for the implementation of WeatherViewAPI
with open(STATIC_ROOT + 'data/city-data.json') as handle:
    dictdump = json.loads(handle.read())


# To check similarity between input word and existing word
# Used in WeatherViewAPI for user input city and existing city
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class EarthQuakeViewAPI(APIView):
    permission_classes = []

    def get(self, request, year=None):
        now = datetime.datetime.now()
        if year:
            data = earthquake_status(year)
        else:
            data = earthquake_status(now.year)

        return Response(data)


class DiseaseViewAPI(APIView):
    """
    Disease API to show diseases encounter at particular time
    """
    permission_classes = []

    def get(self, request, year=None, week=None):
        now = datetime.datetime.now()
        all_pdf = get_all_pdf()
        if year:
            if year in all_pdf:
                if week:
                    if int(week) < len(all_pdf[year]):
                        pdf_filename = download_pdf(all_pdf[year][int(week)])
                    else:
                        return Response({'error': 'Invalid input'})
                else:
                    pdf_filename = download_pdf(all_pdf[year][-1])
            else:
                return Response({'error': 'Invalid input'})
        else:
            pdf_filename = download_pdf(all_pdf[str(now.year)][-1])
        pdf_data = extract_pdf_to_dict(pdf_filename)

        return Response(pdf_data)


class WeatherViewAPI(APIView):
    """
    Weather API to show weather for any particular city

    Attributes:
        pk : City Name
    """
    permission_classes = []
    url = 'http://city.imd.gov.in/citywx/city_weather.php?id='

    def get(self, request, pk=None):
        if pk.upper() in dictdump:
            city_name = pk.upper()
        else:
            match = 0
            city_name = ''
            for city in dictdump.keys():
                if pk.upper() in city:
                    city_name = city
                    break
                temp_value = similar(pk.upper(), city)
                if temp_value > match:
                    match = temp_value
                    city_name = city
        if city_name == '':
            data = {'status': 200, 'message': 'Nothing found'}
        else:
            r = requests.get(self.url + dictdump[city_name])
            soup = BeautifulSoup(r.text, 'html.parser')
            page_text = soup.get_text().replace('  ', '').split('\n')
            filtered_page_text = list(filter(lambda x: x != '' and x != ' ', page_text))
            weather_data = filtered_page_text[4:26]
            forecast_data = filtered_page_text[31:]
            data = {
                'city': city_name,
                'dated': soup.find_all('b')[1].text[7:],
                'forecast': []
            }

            for data1, data2 in zip(*[iter(weather_data)] * 2):
                data[data1] = data2

            for data1, data2, data3, data4 in zip(*[iter(forecast_data)] * 4):
                data['forecast'].append({
                    'date': data1,
                    'Min Temp': data2,
                    'Max Temp': data3,
                    'Weather': data4
                })

        return Response(data)
