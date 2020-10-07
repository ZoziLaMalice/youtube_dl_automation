#!/bin/bash

python3 ./dl_musics_url.py

python3 /usr/local/bin/youtube-dl -a ./urls_to_download.txt
