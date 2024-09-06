import json
import os

from scraper import scraper_utils
from scraper.scraper import get_songs
from scraper.song_downloader import download_genre

run_dir = "datasets/scraper_runs"

def process_batch(path):
    for file in os.listdir(path):
        pass

    cleanup_batch(path)

def download_songs(path):
    tmp_dir = os.path.join(path, "tmp")
    genres_path = os.path.join(path, "genre-links.json")

    with open(genres_path, "r") as data:
        music_library = json.load(data)

        for genre, links in music_library.items():
            download_genre(links, genre, tmp_dir)
            process_batch(tmp_dir)

def cleanup_batch(path):
    for file in os.listdir(path):
        os.remove(file)

def main():
    # creating new run directory
    run_number = len(os.listdir(run_dir)) + 1
    dir_name = f"run_{str(run_number)}"
    run_path = os.path.join(run_dir, dir_name)
    genre_links_path = os.path.join(run_path, "genre-links.json")
    os.mkdir(run_path)

    # getting the songs
    get_songs(genre_links_path)


if __name__ == "__main__":
    with open("datasets/scraper_runs/run_1/genre-links.json", "r") as json_file:
        data_set = json.load(json_file)
        sample_size, mean, std_dev, var = scraper_utils.dataset_info(data_set)
