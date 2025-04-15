import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")


def search_song(artist_name):
    headers = {'Authorization': f'Bearer {GENIUS_API_TOKEN}'}
    search_url = 'https://api.genius.com/search'
    data = {'q': f' {artist_name}'}
    response = requests.get(search_url, params=data, headers=headers).json()

    hits = response['response']['hits']
    if hits:
        hit_list = []
        for hit in hits:
            song_path = hit['result']['path']
            hit_list.append(f'https://genius.com{song_path}')
        return hit_list
    return None


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


def get_lyrics(url):
    driver.get(url)
    song_name = driver.find_element(By.CLASS_NAME, "SongHeader-desktop__HiddenMask-sc-ffb24f94-11").text

    lyrics_divs = driver.find_elements(By.CLASS_NAME, "ReferentFragment-desktop__Highlight-sc-380d78dd-1")
    lyrics = "\n".join([div.text for div in lyrics_divs])
    return [song_name, lyrics]


artists_list = []
songs_name_list = []
lyrics_list = []


def get_songs_by_artists(artists):
    for artist in artists:
        urls = search_song(artist_name=artist)

        for url in urls:
            obj = get_lyrics(url)
            song_name = obj[0]
            lyrics = obj[1]

            artists_list.append(artist)
            songs_name_list.append(song_name)
            lyrics_list.append(lyrics)

    data = {
        "artist": artists_list,
        "song": songs_name_list,
        "lyrics": lyrics_list
    }
    df = pd.DataFrame(data)
    df.to_csv("BUNA.csv")


get_songs_by_artists(["Tyler the Creator", "Billie Eilish", "Kanye West"])
