# coding: utf-8

from bs4 import BeautifulSoup
import requests
from datetime import datetime
import time
import csv

def main(month, year, game_type, csv_writer):
    now = datetime.now()
   
    today = str(now.month) + '.' + str(now.day) + '.' + str(now.year)
    today = datetime.strptime(today, "%m.%d.%Y")
    
    
    url = """http://sports.news.naver.com/basketball/schedule/index.nhn?&month={}&year={}&teamCode=&category={}""".format(month, year, game_type)
    req = requests.get(url)
    
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    
    
    frame = soup.find('div', {'class': 'sch_volleyball tb_kbl'})
    
    rows = frame.find_all('div', {'class': ['sch_tb ', 'sch_tb2 selected', 'sch_tb2 ']})
    
    
    for row in rows:
        trs = row.find_all('tr')
        g_date = trs[0].select('span.td_date strong')[0].text
        g_month = g_date.split('.')[0]
        g_day = g_date.split('.')[1]
        game_datetime = g_date + '.2016'
        game_datetime = datetime.strptime(game_datetime, "%m.%d.%Y")
        
        if today > game_datetime: 
            for index, tr in enumerate(trs):
                td = tr.find_all('td')
                if index == 0:
                    time = td[1].text
                    home = td[2].find_all('span')[0].text
                    home_score = td[2].find('strong').text.split(':')[0]
                    away = td[2].find_all('span')[1].text
                    away_score = td[2].find('strong').text.split(':')[0]          

                else:
                    time = td[0].text
                    home = td[1].find_all('span')[0].text
                    home_score = td[1].find('strong').text.split(':')[0]
                    away = td[1].find_all('span')[1].text
                    away_score = td[1].find('strong').text.split(':')[0]      
                print("{}월 {}일 경기 결과 {}팀 {}점 VS {}팀 {}점".format(g_month, g_day,home, home_score , away, away_score))
                csv_writer.writerow([g_month, g_day, home, home_score])
                csv_writer.writerow([g_month, g_day, away, away_score])
                

if __name__ == "__main__":
    f = open('kbl_score.csv', 'a')
    csv_writer = csv.writer(f)
    main(11, 2016, "kbl", csv_writer)
    f.close()
    
   
