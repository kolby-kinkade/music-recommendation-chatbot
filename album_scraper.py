import os
import time
import re
import random
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException




"""
WEB SCRAPING CODE THAT DIVIDES ALBUMS BY GENRE AND DECADE

"""


class Album:
    # Initialize album objects
    def __init__(self, title, artist, release_date, genre):
        self.title = title
        self.artist = artist
        self.release_date = release_date
        self.genre = genre

    def __str__(self):
        return f"Title: {self.title}\nArtist: {self.artist}\nRelease Date: {self.release_date}\nGenre: {', '.join(self.genre)}"


albums_by_decade_genre = {}


# Separates music based on the 5 main genres used
def add_album(title, artist, release_date, genres):
    album = Album(title, artist, release_date, genres)
    decade = release_date[-4:-1] + "0s"
    if decade not in albums_by_decade_genre:
        albums_by_decade_genre[decade] = {"Rock": [], "Country": [], "Pop": [], "Hip Hop": [], "Jazz": []}
    for genre in genres:
        if "Rock" in genre:
            albums_by_decade_genre[decade]["Rock"].append(album)
        elif "Country" in genre:
            albums_by_decade_genre[decade]["Country"].append(album)
        elif "Pop" in genre:
            albums_by_decade_genre[decade]["Pop"].append(album)
        elif "Hip Hop" in genre or "Hip-Hop" in genre:
            albums_by_decade_genre[decade]["Hip Hop"].append(album)
        elif "Jazz" in genre:
            albums_by_decade_genre[decade]["Jazz"].append(album)


def save_albums_to_file(filename):
    albums_to_save = {decade: {genre: [vars(album) for album in albums]
                               for genre, albums in genres.items()}
                      for decade, genres in albums_by_decade_genre.items()}
    with open(filename, 'w') as f:
        json.dump(albums_to_save, f, indent=4)



# Path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\kolby\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

assert os.path.isfile(chrome_driver_path), f"ChromeDriver not found at {chrome_driver_path}"

# Set up ChromeDriver service
service = Service(chrome_driver_path)


def scrape_rock_albums(decade):
    url = f'https://www.albumoftheyear.org/genre/7-rock/{decade}s/'
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "centerContent"))
        )
        album_list_row = element.find_elements(By.CLASS_NAME, 'albumListRow')

        for album in album_list_row:
            album_title = album.find_element(By.CLASS_NAME, 'albumListTitle').text
            album_release_date = album.find_element(By.CLASS_NAME, 'albumListDate').text
            artist_name = re.sub(r'^\d+\.\s*', '', album_title.split(' - ')[0]).strip()
            album_title_text = album_title.split(' - ')[1].strip()

            try:
                album_genre = album.find_element(By.CLASS_NAME, 'albumListGenre')
                genre_text = album_genre.text.split(", ")
            except NoSuchElementException:
                genre_text = ["N/A"]

            add_album(album_title_text, artist_name, album_release_date, genre_text)
    finally:
        driver.quit()


def scrape_country_albums(decade):
    url = f'https://www.albumoftheyear.org/genre/18-country/{decade}s/'
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "centerContent"))
        )
        album_list_row = element.find_elements(By.CLASS_NAME, 'albumListRow')

        for album in album_list_row:
            album_title = album.find_element(By.CLASS_NAME, 'albumListTitle').text
            album_release_date = album.find_element(By.CLASS_NAME, 'albumListDate').text
            artist_name = re.sub(r'^\d+\.\s*', '', album_title.split(' - ')[0]).strip()
            album_title_text = album_title.split(' - ')[1].strip()

            try:
                album_genre = album.find_element(By.CLASS_NAME, 'albumListGenre')
                genre_text = album_genre.text.split(", ")
            except NoSuchElementException:
                genre_text = ["N/A"]

            add_album(album_title_text, artist_name, album_release_date, genre_text)
    finally:
        driver.quit()


def scrape_pop_albums(decade):
    url = f'https://www.albumoftheyear.org/genre/15-pop/{decade}s/'
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "centerContent"))
        )
        album_list_row = element.find_elements(By.CLASS_NAME, 'albumListRow')

        for album in album_list_row:
            album_title = album.find_element(By.CLASS_NAME, 'albumListTitle').text
            album_release_date = album.find_element(By.CLASS_NAME, 'albumListDate').text
            artist_name = re.sub(r'^\d+\.\s*', '', album_title.split(' - ')[0]).strip()
            album_title_text = album_title.split(' - ')[1].strip()

            try:
                album_genre = album.find_element(By.CLASS_NAME, 'albumListGenre')
                genre_text = album_genre.text.split(", ")
            except NoSuchElementException:
                genre_text = ["N/A"]

            add_album(album_title_text, artist_name, album_release_date, genre_text)
    finally:
        driver.quit()


def scrape_hip_hop_albums(decade):
    url = f'https://www.albumoftheyear.org/genre/3-hip-hop/{decade}s/'
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "centerContent"))
        )
        album_list_row = element.find_elements(By.CLASS_NAME, 'albumListRow')

        for album in album_list_row:
            album_title = album.find_element(By.CLASS_NAME, 'albumListTitle').text
            album_release_date = album.find_element(By.CLASS_NAME, 'albumListDate').text
            artist_name = re.sub(r'^\d+\.\s*', '', album_title.split(' - ')[0]).strip()
            album_title_text = album_title.split(' - ')[1].strip()

            try:
                album_genre = album.find_element(By.CLASS_NAME, 'albumListGenre')
                genre_text = album_genre.text.split(", ")
            except NoSuchElementException:
                genre_text = ["N/A"]

            add_album(album_title_text, artist_name, album_release_date, genre_text)
    finally:
        driver.quit()


def scrape_jazz_albums(decade):
    url = f'https://www.albumoftheyear.org/genre/35-jazz/{decade}s/'
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "centerContent"))
        )
        album_list_row = element.find_elements(By.CLASS_NAME, 'albumListRow')

        for album in album_list_row:
            album_title = album.find_element(By.CLASS_NAME, 'albumListTitle').text
            album_release_date = album.find_element(By.CLASS_NAME, 'albumListDate').text
            artist_name = re.sub(r'^\d+\.\s*', '', album_title.split(' - ')[0]).strip()
            album_title_text = album_title.split(' - ')[1].strip()

            try:
                album_genre = album.find_element(By.CLASS_NAME, 'albumListGenre')
                genre_text = album_genre.text.split(", ")
            except NoSuchElementException:
                genre_text = ["N/A"]

            add_album(album_title_text, artist_name, album_release_date, genre_text)
    finally:
        driver.quit()


def album_scraping():  # main():
    decades = [2020, 2010, 2000, 1990, 1980, 1970, 1960, 1950]
    for decade in decades:
        scrape_rock_albums(decade)
        time.sleep(random.uniform(5, 28))
        scrape_country_albums(decade)
        time.sleep(random.uniform(5, 28))
        scrape_pop_albums(decade)
        time.sleep(random.uniform(5, 28))
        scrape_hip_hop_albums(decade)
        time.sleep(random.uniform(5, 28))
        scrape_jazz_albums(decade)
        time.sleep(random.uniform(5, 28))
    save_albums_to_file('albums_by_decade_genre.json')
    print("Done")


if __name__ == "__main__":
    album_scraping()