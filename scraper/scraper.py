import json
import math
import time
import urllib.parse

from contextlib import contextmanager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from scraper.scraper_utils import print_progress_bar

sc_search_playlist = "https://soundcloud.com/search/sets?q="
sc_url = "https://soundcloud.com"
genres = "scraper/genres.json"

def write_json(path, data):
    with open(path, 'w') as fp:
        json.dump(data, fp, indent=4)


def get_songs(genre_links):
    print("started: getting song links")
    with open(genres) as genre_data:
        data = json.load(genre_data)
        genre_links_dict = {}
        total_genres = len(data["genres"])
        total_songs = 0
        i = 1
        total_time = 0
        for genre in data["genres"]:
            # getting start time for average process time
            start_time = time.time()

            print_progress_bar(i, total_genres)
            print()
            print(f"\t- getting songs for: '{genre['name']}' - PROCESSING")

            genre_format = genre["name"].replace(" ", "-").lower()
            genre_playlist_links = get_playlist_links(genre["name"])
            genre_songs = get_genre_songs(genre_playlist_links)

            genre_links_dict.update({genre_format: genre_songs})
            write_json(genre_links, genre_links_dict)
            total_songs += len(genre_songs)

            # getting average time remaining
            end_time = time.time()
            process_time = (end_time - start_time) / 60
            total_time += process_time
            avg_time_mins = math.ceil(total_time / i)

            i += 1
            print(f"\t- getting songs for: '{genre['name']}' - COMPLETE with {len(genre_songs)} songs. total songs: {total_songs}. estimated time remaining: {avg_time_mins * (total_genres - i)} mins")
            break
    print()
    print("finished: getting song links")
    print(f"total songs: {total_songs}, avg time: {avg_time_mins} mins")

def get_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    return chrome_options


@contextmanager
def get_driver(max_retries=5, delay=2):
    # Uncomment the following lines for Raspberry Pi
    # service = Service("/usr/lib/chromium-browser/chromedriver")

    service = Service(ChromeDriverManager().install())
    chrome_options = get_options()

    driver = None
    try:
        for attempt in range(max_retries):
            try:
                driver = webdriver.Chrome(service=service, options=chrome_options)
                # Attempt to open a simple page (can be a local file or a simple page on the web)
                driver.get("data:,")  # An empty data URL, just to check if the driver is responsive
                break  # If successful, break out of the loop
            except WebDriverException as e:
                print(f"\t? attempt {attempt + 1} to start WebDriver failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
        else:
            raise Exception("Failed to start WebDriver after several attempts.")

        yield driver

    finally:
        if driver:
            driver.quit()


def wait_load(element, driver, timeout):
    # waiting for the content to load
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(element)
    )


def get_playlist_links(genre):
    links = []

    # formatting url
    url_encoded = urllib.parse.quote_plus(genre)
    url = sc_search_playlist + url_encoded

    # getting the driver
    with get_driver() as driver:
        try:
            driver.get(url)

            # Call the function to accept cookies
            accept_cookies(driver)

            # waiting for the content to load
            wait_load((By.CSS_SELECTOR, "div.searchList.lazyLoadingList"), driver, 20)

            # getting the page contents
            soup = BeautifulSoup(driver.page_source, "html.parser")
            div_element = soup.find("div", {"class": "searchList lazyLoadingList"})
            playlist_items = div_element.find_all("li", class_="searchList__item sc-mt-3x")

            # extracting the playlist links
            for playlist in playlist_items:
                links.append(playlist.find("a", {"class": "sc-link-primary soundTitle__title sc-link-dark sc-text-h4"}).get("href"))
        except Exception:
            print(f"\t* failed getting songs for: '{genre}' - SKIPPING")
            return links

    return links


def get_genre_songs(play_list_links):
    links = []
    for link in play_list_links:
        url = sc_url + link

        # getting the driver
        with get_driver() as driver:
            try:
                driver.get(url)

                # Call the function to accept cookies
                accept_cookies(driver)

                # waiting for the content to load
                wait_load((By.CSS_SELECTOR, "div.trackList.g-all-transitions-300.lazyLoadingList"), driver, 20)

                # getting the page contents
                soup = BeautifulSoup(driver.page_source, "html.parser")
                div_element = soup.find("div", {"class": "trackList g-all-transitions-300 lazyLoadingList"})
                song_items = div_element.find_all("li", class_="trackList__item sc-border-light-bottom sc-px-2x")

                # getting the soundcloud links
                for song in song_items:
                    song_url = sc_url + song.find("a", {"class", "trackItem__trackTitle sc-link-dark sc-link-primary sc-font-light"}).get("href")
                    links.append(song_url)
            except Exception:
                print(f"\t* failed getting song: '{url}' - SKIPPING")
                continue
    return links


def accept_cookies(driver):
    # Wait until the cookie accept button is clickable
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'I Accept')]"))
    )
    # Click the cookie accept button
    cookie_button.click()
    time.sleep(3)
