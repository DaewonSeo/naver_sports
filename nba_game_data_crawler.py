import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import csv

# 2016111910

def clean_int(value):
    value = round(int(value) * 0.01, 2)

    return value

def main(game_id, csv_writer):

    driver = webdriver.Chrome('../chrome_driver/chromedriver')
    driver.get('http://sports.news.naver.com/sports/index.nhn?category=nba&ctg=result&game_id={}&sub_menu=team_record'.format(game_id))
    driver.implicitly_wait(1)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    table = soup.find('div', {'id': 'content'})
    home_score = int(table.find_all('tr', {'bgcolor': '#FFFFFF'})[0].find_all('td')[-1].text)
    away_score = int(table.find_all('tr', {'bgcolor': '#FFFFFF'})[1].find_all('td')[-1].text)
    home_team = table.find_all('tr', {'bgcolor': '#FFFFFF'})[0].find_all('td')[0].text
    away_team = table.find_all('tr', {'bgcolor': '#FFFFFF'})[1].find_all('td')[0].text
    date = table.select('span#game_date')[0].text.split(' ')
    year = date[0][:4]
    month = date[1][:2]
    day = date[2][:2]
    
    
    content = table.find_all('table', {'bgcolor': '#DCDCDC'})[1].find('tbody')
    
    # print(game_id, home_team, home_score, su)
    success_ratio_of_2_point_home = int(content.find_all('tr')[0].find_all('td')[0].text.split('/')[0])
    trial_ratio_of_2_point_home = int(content.find_all('tr')[0].find_all('td')[0].text.split('/')[1])
    success_ratio_of_2_point_away = int(content.find_all('tr')[0].find_all('td')[2].text.split('/')[0])
    trial_ratio_of_2_point_away = int(content.find_all('tr')[0].find_all('td')[2].text.split('/')[1])
    success_ratio_of_3_point_home = int(content.find_all('tr')[2].find_all('td')[0].text.split('/')[0])
    trial_ratio_of_3_point_home = int(content.find_all('tr')[2].find_all('td')[0].text.split('/')[1])
    success_ratio_of_3_point_away = int(content.find_all('tr')[2].find_all('td')[2].text.split('/')[0])
    trial_ratio_of_3_point_away = int(content.find_all('tr')[2].find_all('td')[2].text.split('/')[1])
    success_free_draw_point_home = int(content.find_all('tr')[4].find_all('td')[0].text.split('/')[0])
    trial_free_draw_point_home = int(content.find_all('tr')[4].find_all('td')[0].text.split('/')[1])
    success_free_draw_point_away = int(content.find_all('tr')[4].find_all('td')[2].text.split('/')[0])
    trial_free_draw_point_away = int(content.find_all('tr')[4].find_all('td')[2].text.split('/')[1])
    # ratio_of_2_point_home = clean_int(content.find_all('tr')[2].find_all('td')[0].text[:-1])
    # ratio_of_2_point_away = clean_int(content.find_all('tr')[2].find_all('td')[2].text[:-1])
    # ratio_of_3_point_home = clean_int(content.find_all('tr')[4].find_all('td')[0].text[:-1])
    # ratio_of_3_point_away = clean_int(content.find_all('tr')[4].find_all('td')[2].text[:-1])
    # free_draw_point_home = clean_int(content.find_all('tr')[6].find_all('td')[0].text[:-1])
    # free_draw_point_away = clean_int(content.find_all('tr')[6].find_all('td')[2].text[:-1])
    assist_home = int(content.find_all('tr')[6].find_all('td')[0].text)
    assist_away = int(content.find_all('tr')[6].find_all('td')[2].text)
    offense_rebound_home = int(content.find_all('tr')[7].find_all('td')[0].text)
    offense_rebound_away = int(content.find_all('tr')[7].find_all('td')[2].text)
    defense_rebound_home = int(content.find_all('tr')[8].find_all('td')[0].text)
    defense_rebound_away = int(content.find_all('tr')[8].find_all('td')[2].text)
    steal_home = int(content.find_all('tr')[10].find_all('td')[0].text)
    steal_away = int(content.find_all('tr')[10].find_all('td')[2].text)
    block_home = int(content.find_all('tr')[11].find_all('td')[0].text)
    block_away = int(content.find_all('tr')[11].find_all('td')[2].text)
    foul_home = int(content.find_all('tr')[12].find_all('td')[0].text)
    foul_away = int(content.find_all('tr')[12].find_all('td')[2].text)
    
    csv_writer.writerow([year, month, day, str(game_id), home_team, 1, home_score, success_ratio_of_2_point_home, \
                         trial_ratio_of_2_point_home, success_ratio_of_3_point_home, trial_ratio_of_3_point_home,\
                         success_free_draw_point_home, trial_free_draw_point_home, assist_home, offense_rebound_home,\
                         defense_rebound_home, steal_home, block_home, foul_home])
    csv_writer.writerow([year, month, day, str(game_id), away_team, 2, away_score, success_ratio_of_2_point_away, \
                         trial_ratio_of_2_point_away, success_ratio_of_3_point_away, trial_ratio_of_3_point_away,\
                         success_free_draw_point_away, trial_free_draw_point_away, assist_away, offense_rebound_away, defense_rebound_away,\
                         steal_away, block_away, foul_away])
    # print(date, home_score, home_team, ratio_of_2_point_home, ratio_of_3_point_home, free_draw_point_home, assist_home)


    driver.quit()

if __name__ == '__main__':
    f = open('nba_score_2016.csv', 'r')
    csv_reader = csv.reader(f)
    fw = open('nba_game_data_2016.csv', 'w')
    csv_writer = csv.writer(fw)
    list_of_game_id = [ row[3] for row in csv_reader ]
    list_of_game_id = set(list_of_game_id)
    for game_id in list_of_game_id:
        main(game_id, csv_writer)
