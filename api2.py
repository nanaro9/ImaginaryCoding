import requests
import json
limit = 10
response = requests.get(f'http://itunes.apple.com/search?entity=song&limit={limit}&term=softwilly?')

data = response.json()

for song in data['results']:
    songName = song['trackName']
    artistName = song['artistName']
    print(artistName,"-",songName)