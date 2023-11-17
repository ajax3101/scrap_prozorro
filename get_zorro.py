import requests
import fake_useragent
from bs4 import BeautifulSoup
import time
import os




# Адреса API ProZorro
url = 'https://api.openprocurement.org/api/2.5/tenders'

# Приклад кодів ЄДРПОУ організацій
edrpou_codes = ['00123456', '00234567', '00345678']

# Заголовок для запиту
headers = {'Content-Type': 'application/json'}

# Список для зберігання даних тендерів
tenders_data = []

# Перебір кодів ЄДРПОУ
for edrpou_code in edrpou_codes:
    # Створення параметра запиту для фільтрації за учасником тендеру
    params = {'opt_fields': 'tenderers', 'tenderer_id': edrpou_code}

    # Запит до API
    response = requests.get(url, headers=headers, params=params)

    # Перевірка наявності даних у відповіді
    if response.status_code == 200:
        # Додавання даних тендерів до списку
        tenders_data.extend(response.json().get('data', []))
    else:
        print(f"Error fetching data for {edrpou_code}. Status Code: {response.status_code}")

# Виведення результатів
print(tenders_data)
