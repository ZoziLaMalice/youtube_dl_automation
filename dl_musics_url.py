#!/bin/python

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import re

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=chrome_options)

url = 'https://www.youtube.com/playlist?list=PLvEaFQJe3P3IJzXrBqFSrqAUPGwkUMw9a'

print('Opening Youtube .......')
driver.get(url)
print('.....Youtube opened!!\n')

print('Getting missing music from your library ......')
musics = []
nb_music = driver.find_element_by_xpath('//*[@id="stats"]/yt-formatted-string[1]/span[1]').text
while len(musics) != int(nb_music):
    driver.execute_script("window.scrollTo(0, 100000);")
    musics = driver.find_elements_by_xpath('//*[@id="content"]/a')

comp = re.compile('^(.+)&list')
musics_url = [comp.search(music.get_attribute('href')).group(1) for music in musics]
print('..... All done!!\n\nStart downloading .....')

with open('already_download.txt', 'r') as f:
    already_dl = [line.rstrip() for line in f]

with open('already_download.txt', 'w') as f:
    for url in musics_url:
        f.write(f"{url}\n")

musics_url = list(set(musics_url) - set(already_dl))

with open('urls_to_download.txt', 'w') as f:
    for url in musics_url:
        f.write(f"{url}\n")
