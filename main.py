import os
import csv
import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from tqdm import tqdm



load_dotenv()

def read_csv_file(file_path):
    edrpo_data = []

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')

        for row in csv_reader:
            edrpo_data.append(row[2].zfill(8))

    return edrpo_data

def get_all_pages(code_e):
    for i, code_e_value in enumerate(code_e, start=1):
        folder_path = os.path.join("data", str(code_e_value))

        if os.path.exists(folder_path):
            print(f"[INFO] Итерация {i}/{len(code_e)}, Папка уже существует. Пропускаем.")
            continue

        os.makedirs(folder_path, exist_ok=True)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }

        r = requests.get(url=f'https://www.dzo.com.ua/tenders/current?&filter%5Bidentifiers%5D={code_e_value}', headers=headers)

        with open(os.path.join(folder_path, "page_1.html"), "w", encoding="utf-8") as file:
            file.write(r.text)

        with open(os.path.join(folder_path, "page_1.html"), encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        pages_count_element = soup.find('div', class_="pages relative clear")

        if pages_count_element:
            pages_count = int(pages_count_element.find_all('a')[-1].text)
        else:
            pages_count = 1

        for j in range(1, pages_count + 1):
            url = f"https://www.dzo.com.ua/tenders/current?filter%5Bidentifiers%5D={code_e_value}&page={j}"
            r = requests.get(url=url, headers=headers)
            with open(os.path.join(folder_path, f"page_{j}.html"), "w", encoding="utf-8") as file:
                file.write(r.text)
            time.sleep(3)
            print(f"[INFO] Итерация {i}/{len(code_e)}, Скачено страниц {j}/{pages_count}")

    print("[INFO] Все итерации завершены")

def collect_data(code_e):
    cur_date = datetime.now().strftime("%d_%m_%Y")
    
    csv_filename = f"data_{cur_date}.csv"
    json_filename = f"data_{cur_date}.json"

    with open(csv_filename, "w", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            (
                "Tender",
                "URL",
                "CPV",
                "Очікувана вартість закупівлі",
                "Дата оголошення процедури",
                "Поточний статус процедури",
                "Ідентифікатор закупівлі",
                "Організатор закупівлі",
                "Процедура закупівлі",
                "edr_id"  
            )
        )

    data = []

    for code_e_value in code_e:
        folder_path = os.path.join("data", str(code_e_value))
        pages_count = len(os.listdir(folder_path))

        for page in tqdm(range(1, pages_count + 1), desc=f"Обработка edr_id={code_e_value}", leave=False):
            file_path = os.path.join(folder_path, f"page_{page}.html")

            if not os.path.exists(file_path):
                print(f"[WARNING] File not found: {file_path}")
                continue

            with open(file_path, encoding="utf-8") as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")
            items_cards = soup.find_all("div", class_="item relative")

            for item in items_cards:
                t = item.find("h2", class_="title").text
                tl = 'https://www.dzo.com.ua' + item.find('a', class_="globalLink").get('href')
                cpv = item.find("div", class_="cpv cd").text
                v = item.find("div", class_="newkvaziName clear").find_next('span').find_next('span').text.rstrip(' Гривня')
                a = item.find("div", class_="newauction").find_next('span').find_next('span').text
                s = item.find("div", class_="newstatus").find_next('span').find_next('span').text
                t_id = item.find("div", class_="cd newtenderId").find_next('span').find_next('span').text
                cdb = item.find("div", class_="cd newtenderMethod CDB_Number").find_next('span').find_next('span').text
                t_method = item.find("div", class_="cd newtenderMethod").find_next('span').find_next('span').text

                # Convert the date string to the desired format
                a_datetime = datetime.strptime(a, "%d.%m.%Y %H:%M")
                formatted_date = a_datetime.strftime("%Y-%m-%d %H:%M:%S%z")
                # Remove "`" symbol from the "Очікувана вартість закупівлі" field
                v = v.replace("`", "")
                # Additional check for empty values
                if not any(value for value in (t, tl, cpv, v, formatted_date, s, t_id, cdb, t_method, code_e_value)):
                    print(f"[WARNING] Empty values detected for edr_id={code_e_value}. Skipping...")
                    continue
                data.append(
                    {
                        "t": t,
                        "tl": tl,
                        "cpv": cpv,
                        "v": v,
                        "a": formatted_date,
                        "s": s,
                        "t_id": t_id,
                        "cdb": cdb,
                        "t_method": t_method,
                        "edr_id": code_e_value 
                    }
                )

                with open(csv_filename, "a", encoding="utf-8", newline="") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(
                        (
                            t,
                            tl,
                            cpv,
                            v,
                            formatted_date,
                            s,
                            t_id,
                            cdb,
                            t_method,
                            code_e_value 
                        )
                    )

            print(f"[INFO] Обработана страница для edr_id={code_e_value}")
            # time.sleep(2)

    with open(json_filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print("[INFO] Все итерации завершены")

if __name__ == '__main__':
    code_e = read_csv_file('edrpo.csv')
    get_all_pages(code_e)
    collect_data(code_e)
