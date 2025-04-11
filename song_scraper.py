import os
import time
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

"""

WEB SCRAPING CODE THAT DIVIDES SONGS BY GENRE AND DECADE

"""


class Song:
    # Initialize song objects
    def __init__(self, title, artist, release_date, genre):
        self.title = title
        self.artist = artist
        self.release_date = release_date
        self.genre = genre

    def __str__(self):
        return f"Title: {self.title}\nArtist: {self.artist}\nRelease Date: {self.release_date}\nGenre: {', '.join(self.genre)}"


songs_by_decade_genre = {}


# Separates music based on the 5 main genres used
def add_song(title, artist, release_date, genres):
    song = Song(title, artist, release_date, genres)
    decade = release_date[-4:-1] + "0s"
    if decade not in songs_by_decade_genre:
        songs_by_decade_genre[decade] = {"Rock": [], "Country": [], "Pop": [], "Hip Hop": [], "Jazz": []}
    for genre in genres:
        if "Rock" in genre:
            songs_by_decade_genre[decade]["Rock"].append(song)
        elif "Country" in genre:
            songs_by_decade_genre[decade]["Country"].append(song)
        elif "Pop" in genre:
            songs_by_decade_genre[decade]["Pop"].append(song)
        elif "Hip Hop" in genre or "Hip-Hop" in genre:
            songs_by_decade_genre[decade]["Hip Hop"].append(song)
        elif "Jazz" in genre:
            songs_by_decade_genre[decade]["Jazz"].append(song)


def save_songs_to_file(filename):
    songs_to_save = {decade: {genre: [vars(song) for song in songs]
                               for genre, songs in genres.items()}
                      for decade, genres in songs_by_decade_genre.items()}
    with open(filename, 'w') as f:
        json.dump(songs_to_save, f, indent=4)


# Path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\kolby\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

assert os.path.isfile(chrome_driver_path), f"ChromeDriver not found at {chrome_driver_path}"

# Set up ChromeDriver service
service = Service(chrome_driver_path)


def scrape_rock_songs(decade):
    url = f'https://rateyourmusic.com/charts/top/single/{decade}s/g:rock/'
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "page_charts_section_charts"))
        )
        song_list_row = element.find_elements(By.CLASS_NAME, 'page_charts_section_charts_item')

        for song in song_list_row:
            song_title = song.find_element(By.CLASS_NAME, 'ui_name_locale_original').text
            song_release_date = song.find_element(By.CLASS_NAME, 'page_charts_section_charts_item_date').text
            artist_name = song.find_element(By.CLASS_NAME, 'artist').text

            try:
                song_genre = song.find_element(By.CLASS_NAME, 'genre')
                genre_text = song_genre.text.split(", ")
            except NoSuchElementException:
                genre_text = ["N/A"]

            add_song(song_title, artist_name, song_release_date, genre_text)
    except TimeoutException:
        print(f"Timeout while trying to scrape {decade}s Rock songs")
    finally:
        driver.quit()


def scrape_country_songs(decade):
    url = f'https://rateyourmusic.com/charts/top/single/{decade}s/g:country/'
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "page_charts_section_charts"))
        )
        song_list_row = element.find_elements(By.CLASS_NAME, 'page_charts_section_charts_item')

        for song in song_list_row:
            song_title = song.find_element(By.CLASS_NAME, 'ui_name_locale_original').text
            song_release_date = song.find_element(By.CLASS_NAME, 'page_charts_section_charts_item_date').text
            artist_name = song.find_element(By.CLASS_NAME, 'artist').text

            try:
                song_genre = song.find_element(By.CLASS_NAME, 'genre')
                genre_text = song_genre.text.split(", ")
            except NoSuchElementException:
                genre_text = ["N/A"]

            add_song(song_title, artist_name, song_release_date, genre_text)
    except TimeoutException:
        print(f"Timeout while trying to scrape {decade}s Country songs")
    finally:
        driver.quit()


def scrape_pop_songs(decade):
    url = f'https://rateyourmusic.com/charts/top/single/{decade}s/g:pop/'
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "page_charts_section_charts"))
        )
        song_list_row = element.find_elements(By.CLASS_NAME, 'page_charts_section_charts_item')

        for song in song_list_row:
            song_title = song.find_element(By.CLASS_NAME, 'ui_name_locale_original').text
            song_release_date = song.find_element(By.CLASS_NAME, 'page_charts_section_charts_item_date').text
            artist_name = song.find_element(By.CLASS_NAME, 'artist').text

            try:
                song_genre = song.find_element(By.CLASS_NAME, 'genre')
                genre_text = song_genre.text.split(", ")
            except NoSuchElementException:
                genre_text = ["N/A"]

            add_song(song_title, artist_name, song_release_date, genre_text)
    except TimeoutException:
        print(f"Timeout while trying to scrape {decade}s Pop songs")
    finally:
        driver.quit()


def scrape_hip_hop_songs(decade):
    url = f'https://rateyourmusic.com/charts/top/single/{decade}s/g:hip%2dhop/'
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "page_charts_section_charts"))
        )
        song_list_row = element.find_elements(By.CLASS_NAME, 'page_charts_section_charts_item')

        for song in song_list_row:
            song_title = song.find_element(By.CLASS_NAME, 'ui_name_locale_original').text
            song_release_date = song.find_element(By.CLASS_NAME, 'page_charts_section_charts_item_date').text
            artist_name = song.find_element(By.CLASS_NAME, 'artist').text

            try:
                song_genre = song.find_element(By.CLASS_NAME, 'genre')
                genre_text = song_genre.text.split(", ")
            except NoSuchElementException:
                genre_text = ["N/A"]

            add_song(song_title, artist_name, song_release_date, genre_text)
    except TimeoutException:
        print(f"Timeout while trying to scrape {decade}s Hip Hop songs")
    finally:
        driver.quit()


def scrape_jazz_songs(decade):
    url = f'https://rateyourmusic.com/charts/top/single/{decade}s/g:jazz/'
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "page_charts_section_charts"))
        )
        song_list_row = element.find_elements(By.CLASS_NAME, 'page_charts_section_charts_item')

        for song in song_list_row:
            song_title = song.find_element(By.CLASS_NAME, 'ui_name_locale_original').text
            song_release_date = song.find_element(By.CLASS_NAME, 'page_charts_section_charts_item_date').text
            artist_name = song.find_element(By.CLASS_NAME, 'artist').text

            try:
                song_genre = song.find_element(By.CLASS_NAME, 'genre')
                genre_text = song_genre.text.split(", ")
            except NoSuchElementException:
                genre_text = ["N/A"]

            add_song(song_title, artist_name, song_release_date, genre_text)
    except TimeoutException:
        print(f"Timeout while trying to scrape {decade}s Jazz songs")
    finally:
        driver.quit()


def song_scraping():
    decades = [2020, 2010, 2000, 1990, 1980, 1970, 1960, 1950]
    for decade in decades:
        scrape_rock_songs(decade)
        time.sleep(random.uniform(5, 28))

        scrape_country_songs(decade)
        time.sleep(random.uniform(5, 28))
        scrape_pop_songs(decade)
        time.sleep(random.uniform(5, 28))
        scrape_hip_hop_songs(decade)
        time.sleep(random.uniform(5, 28))
        scrape_jazz_songs(decade)
        time.sleep(random.uniform(5, 28))
    save_songs_to_file('songs_by_decade_genre.json')
    print("Done")


if __name__ == "__main__":
    song_scraping()

