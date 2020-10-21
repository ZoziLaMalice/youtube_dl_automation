#!/bin/python3.8

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import subprocess

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.youtube.com/user/MRCURTIS137599/playlists'

print('Opening Youtube .......\n')

driver.get(url)

names = [i.get_attribute('title') for i in driver.find_elements_by_xpath('//*[@id="video-title"]')]
urls = [str(i.get_attribute('href')) for i in driver.find_elements_by_xpath('//*[@id="video-title"]')]

nb_playlists = len(urls)

playlists = dict(zip(names, urls))

driver.quit()

print('.....Youtube opened!!\n\n')

print('Hello ZoziPop!\nHere, your playlists.\nWhich one do you want to update ?\n')
for i, (name, url) in enumerate(playlists.items()):
    print(f'[{i}] -> {name}')

choice = int(input('\nEnter the number corresponding to the playlist:\n'))

url = list(playlists.values())[choice]

subprocess.run(["youtube-dl", "--download-archive", f"{list(playlists)[choice]}_archive.txt",  url, "-o", f"/media/patamousse/Music/{list(playlists)[choice]}/%(title)s.%(ext)s"], check=True)
