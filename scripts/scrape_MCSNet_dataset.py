# Simple script to scrape the Minecraftskins.net webpage and download each of its
# skins, and save them along with its description as a .txt file which will work
# as captions for the dalle-pytorch library.

from aiohttp import request
from bs4 import BeautifulSoup
import requests
import os

MAIN_PATH = 'https://www.minecraftskins.net'

main_html_text = requests.get(MAIN_PATH).text
soup = BeautifulSoup(main_html_text, 'lxml')
categories = soup.find('nav', class_='main').find_all('a')

current_dir = './dataset/MCSNet/'
if not os.path.exists(current_dir):
  os.makedirs(current_dir)
for cat in categories:
  current_cat_html_text = requests.get(MAIN_PATH + cat['href']).text
  cat_soup = BeautifulSoup(current_cat_html_text, 'lxml')
  next_btn = cat_soup.find('a', class_='next-page')
  print("Scraping category: " + cat['href'])
  while next_btn is not None:
    skin_links = cat_soup.find_all('a', class_='panel-link')
    for skin in skin_links:
      skin_html_text = requests.get(MAIN_PATH + skin['href']).text
      skin_soup = BeautifulSoup(skin_html_text, 'lxml')
      skin_title = skin_soup.find('h2', class_='hero-title').text + '\n'
      skin_desc = skin_soup.find('p', class_='card-description').text
      skin_filename = current_dir + skin['href'][1:]
      img_data = requests.get(MAIN_PATH + skin['href'] + '/download').content
      with open(skin_filename + '.png', 'wb') as handler:
        handler.write(img_data)
      with open(skin_filename + '.txt', 'w') as handler:
        handler.writelines([skin_title, skin_desc])
    next_page_html_text = requests.get(MAIN_PATH + next_btn['href']).text
    cat_soup = BeautifulSoup(next_page_html_text, 'lxml')
    next_btn = cat_soup.find('a', class_='next-page')