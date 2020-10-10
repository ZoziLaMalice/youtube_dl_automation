#!/bin/python

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import re
import os

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.youtube.com/user/MRCURTIS137599/playlists'

print('Opening Youtube .......\n')
driver.get(url)

names = [n.get_attribute('title') for n in driver.find_elements_by_xpath('//*[@id="video-title"]')]
playlist_urls = [p.get_attribute('href') for p in driver.find_elements_by_xpath('//*[@id="view-more"]/a')]
playlist = dict(zip([i for i in range(len(names))], zip(names, playlist_urls)))

print('.....Youtube opened!!\n\n')

print('Hello ZoziPop!\nHere, your playlists.\nWhich one do you want to update ?\n')
for n, url in playlist.items():
    print(f'[{n}] -> {url[0]}')

choice = int(input('\nEnter the number corresponding to the playlist:\n'))

url = playlist[choice][1]
driver.get(url)

print(f'\nGetting missing music from your {playlist[choice][0]} playlist ......')
musics = []
nb_music = driver.find_element_by_xpath('//*[@id="stats"]/yt-formatted-string[1]/span[1]').text
while len(musics) != int(nb_music):
    driver.execute_script("window.scrollTo(0, 100000);")
    musics = driver.find_elements_by_xpath('//*[@id="content"]/a')

comp = re.compile('^(.+)&list')
musics_url = [comp.search(music.get_attribute('href')).group(1) for music in musics]
print('..... All done!!\n\nStart downloading .....\n')

with open(f'{playlist[choice][0]}/already_download.txt', 'r') as f:
    already_dl = [line.rstrip() for line in f]

with open(f'{playlist[choice][0]}/already_download.txt', 'w') as f:
    for url in musics_url:
        f.write(f"{url}\n")

musics_url = list(set(musics_url) - set(already_dl))

with open(f'{playlist[choice][0]}/urls_to_download.txt', 'w') as f:
    for url in musics_url:
        f.write(f"{url}\n")

os.system(f"python3 /usr/local/bin/youtube-dl -a ./{playlist[choice][0]}/urls_to_download.txt -o '~/Music/{playlist[choice][0]}/%(uploader)s/%(title)s.%(ext)s'")
