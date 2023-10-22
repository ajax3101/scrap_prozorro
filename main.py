import csv
import json
import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime




def get_all_pages():
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    # r = requests.get(url='https://www.dzo.com.ua/tenders/current?&filter%5Bidentifiers%5D=00022504', headers=headers)
    
    # if not os.path.exists("data"):
    #     os.mkdir("data")

    # with open("data/page_1.html", "w", encoding="utf-8") as file:
    #     file.write(r.text)

    with open("data/page_1.html", encoding="utf-8") as file:
         src = file.read()
    
    soup = BeautifulSoup(src, 'lxml')
    
    pages_count = int(soup.find('div', class_="pages relative clear").find_all('a')[-1].text)
    #print(pages_count)
    
    for i in range(1, 2):
        url = f"https://www.dzo.com.ua/tenders/current?filter%5Bidentifiers%5D=00022504&page={i}"
        #print(url)
        r = requests.get(url=url, headers=headers)
        with open (f"data/page_{i}.html", "w", encoding="utf-8") as file:
            file.write(r.text)
        time.sleep(2)
    return pages_count + 1 


def collect_data(pages_count):
    # cur_date = datetime.now().strftime("%d_%m_%Y")

    # with open(f"data_{cur_date}.csv", "w") as file:
    #     writer = csv.writer(file)

    #     writer.writerow(
    #         (
    #             "Tender",
    #             "URL",
    #             "CPV"
    #         )
    #     )

    # data = []
        
    for page in range(1, 2):
        with open(f"data/page_{page}.html", encoding="utf-8" ) as file:
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

            print(f"Tender: {t} - URL: {tl} - INFO: {cpv} - Очікувана вартість закупівлі: {v} - Дата оголошення процедури: {a} - Поточний статус процедури: {s} - Ідентифікатор закупівлі: {t_id} - Організатор закупівлі: {cdb} - Процедура закупівлі: {t_method}")


        print(f"Обработана {page}/{pages_count}")
        time.sleep(3)
     

def main():
    pages_count =  get_all_pages()
    collect_data(pages_count=pages_count)

if __name__ == '__main__':
    main()
