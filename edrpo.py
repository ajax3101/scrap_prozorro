import csv

file_path = 'edrpo.csv'
edrpo_data = [] 

with open(file_path, 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=';')

    for row in csv_reader:
        edrpo_data.append(row[2].zfill(8))

# Выведем массив данных на экран
print(edrpo_data)
