import requests
import json


def get_prozorro_data():
    url = 'http://lb-api-sandbox.prozorro.gov.ua/api/2.5/tenders/'
    data = requests.get(url).text
    return data

result = get_prozorro_data()
print(result)

