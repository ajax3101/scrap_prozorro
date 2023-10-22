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
    #             #    https://www.dzo.com.ua/tenders/current?filter%5Bsearch%5D=&filter%5Bobject%5D=title
    #             #    &filter%5Boperator%5D=and&filter%5Bidentifiers_search%5D=&filter%5Bidentifiers%5D=00022504
    #             #    &filter%5Bclassification%5D=&filter%5BmainProcurementCategory%5D=&filter%5Bmilestones_code%5D=
    #             #    &filter%5Btender_value_amount%5D%5Bstart%5D=&filter%5Btender_value_amount%5D%5Bend%5D=
    #             #    &filter%5BtenderPeriod%5D%5Bstart%5D=&filter%5BtenderPeriod%5D%5Bend%5D=&filter%5Bauction%5D%5Bstart%5D=
    #             #    &filter%5Bauction%5D%5Bend%5D=&filter%5BpubDate%5D%5Bstart%5D=&filter%5BpubDate%5D%5Bend%5D=
    #             #    &filter%5Border%5D=pubDate_desc&formname=filter
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
    for page in range(1, pages_count):
        with open(f"data/page_{page}.html", encoding="utf-8" ) as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        items_cards = soup.find_all("div", class_="item relative")

        for item in items_cards:
            t = item.find("h2", class_="title").text
            tl = 'https://www.dzo.com.ua' + item.find('a', class_="globalLink").get('href')
            cpv = item.find("div", class_="cpv cd").text

            v = item.find("div", class_="newkvaziName clear").text
            a = item.find("div", class_="newauction").text
            s = item.find("div", class_="newstatus").text
            t_id = item.find("div", class_="cd newtenderId").text
            cdb = item.find("div", class_="cd newtenderMethod CDB_Number").text
            t_method = item.find("div", class_="cd newtenderMethod").text

            print(f"Tender: {t} - URL: {tl} - INFO: {cpv} - V: {v} - A: {a} - S: {s} - T-ID: {t_id} - CDB: {cdb} - T_M: {t_method}")


        print(f"Обработана {page}/{pages_count}")
        time.sleep(3)
     

def main():
    pages_count =  get_all_pages()
    collect_data(pages_count=pages_count)

if __name__ == '__main__':
    main()
