from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Функция для получения данных с API ProZorro
def get_prozorro_data():
    api_url = "https://staging.prozorro.gov.ua//api/2.5/tenders"

    # Здесь вы можете настроить параметры запроса в соответствии с вашими требованиями
    params = {
        "limit": 10  # Пример: получить первые 10 записей
    }

    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

@app.route('/')
def index():
    prozorro_data = get_prozorro_data()
    return render_template('index.html', prozorro_data=prozorro_data)

if __name__ == '__main__':
    app.run(debug=True)

