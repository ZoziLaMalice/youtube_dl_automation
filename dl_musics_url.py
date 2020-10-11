#!/bin/python3.8

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import re
import subprocess

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

musics_url = list(set(musics_url) - set(already_dl))

error_url = []

if len(musics_url) > 1:
    for url in musics_url:
        try:
            subprocess.run(["python3", "/usr/local/bin/youtube-dl", url, "-o", f"/media/patamousse/Music/{playlist[choice][0]}/%(uploader)s/%(title)s.%(ext)s"], check = True)
        except subprocess.CalledProcessError:
            print('Download error - Please check that video is still available')
            error_url.append(url)
elif len(musics_url) == 0:
    print('No music to download in this playlist bro!')
else:
    try:
        subprocess.run(["python3", "/usr/local/bin/youtube-dl", musics_url[0], "-o", f"/media/patamousse/Music/{playlist[choice][0]}/%(uploader)s/%(title)s.%(ext)s"], check = True)
    except subprocess.CalledProcessError:
        print('Download error - Please check that video is still available')
        error_url.append(url)

if len(musics_url) != 0:
    all_musics_url = already_dl + musics_url
    musics_url_no_error = list(set(musics_url) - set(error_url))

    with open(f'{playlist[choice][0]}/already_download.txt', 'w') as f:
        for url in musics_url_no_error:
            f.write(f"{url}\n")

    with open(f'{playlist[choice][0]}/error_download.txt', 'w') as f:
        for url in error_url:
            f.write(f"{url}\n")

driver.quit()
