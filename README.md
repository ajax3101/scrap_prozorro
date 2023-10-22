# Telegram bot прогноза погоди
[![Python Version](https://img.shields.io/badge/python-3.11-brightgreen.svg)](https://python.org)

Простий сайт на Python за допомогою Flask/Django. 
Працюємо з API Prozorro  та бібліотекою requests. 
Парсим JSON дані.

![Chat Weather Telegram Bot ](/image.png)

Клонуємо репо

``` bash
git clone https://github.com/ajax3101/scrap_prozorro.git
````

Встановлюємо та активуємо віртуальне оточення
``` bash
     python3 -m venv venv
     . venv/bin/activate
  ````

Встановлюємо необхідні модулі для роботи:
Завантажуємо файл із залежностями проекту
``` bash
pip install -r requirements.txt
````
Запуск програми
``` bash
python main.py
````
**Увага!**
Необхідно створити config.py файл та ввести в нього токени сайтів Prozzoro та EDRPOU
Наприклад:
``` bash
# Отримуємо API 
CODE_EDRPOU='00022504'
````
Файл config.py повинен бути вказаний у файлі .gitignore щоб ваші налаштування не відлетіли в репозиторій