with open('Rap/already_download.txt', 'r') as f:
    already_dl = [line.rstrip() for line in f]

print(already_dl[:5])

musics_url = ['mdr']

musics_url += already_dl

musics_url = list(set(musics_url) - set(already_dl))

print(musics_url)
