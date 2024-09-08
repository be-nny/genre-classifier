import datetime
import json
import os
import argparse

from utils import project_utils
from scraper.scraper import get_songs
from scraper.song_downloader import download_genre

run_dir = "datasets/scraper_runs"
dataset_name = "genre-links.json"

# command line arguments
parser = argparse.ArgumentParser(
    prog="Genre Classifier",
    description="Genre Classification with Machine Learning. Scrape and analyse song links to train a machine learning model.",
    epilog="Ben Abbott 2024"
)

# adding arguments
parser.add_argument("-s", "--scrape", action="store_true",
                    help=f"creates a new dataset of song links called '{dataset_name}' from 'genres.json'. saved to dataset/runs/run_*")
parser.add_argument("-p", "--preprocess", action="store_true",
                    help="preprocess the dataset ready for training and testing. if not dataset path is given, the most recent dataset run is used.")
parser.add_argument("-l", "--load", help="loads a dataset")
parser.add_argument("-i", "--info", action="store_true", help="gets the info of the most recent dataset run, or the dataset specified with '-l'")


def process_batch(path):
    for file in os.listdir(path):
        pass

    cleanup_batch(path)


def download_songs(path):
    tmp_dir = os.path.join(path, "tmp")
    genres_path = os.path.join(path, dataset_name)

    with open(genres_path, "r") as data:
        music_library = json.load(data)

        for genre, links in music_library.items():
            download_genre(links, genre, tmp_dir)
            process_batch(tmp_dir)


def cleanup_batch(path):
    for file in os.listdir(path):
        os.remove(file)


def main(args):
    # creating a new dataset
    if args.scrape:
        print("\n--creating new dataset--")

        # creating new run directory
        run_number = len(os.listdir(run_dir)) + 1
        dir_name = f"run_{str(run_number)}"
        run_path = os.path.join(run_dir, dir_name)
        os.mkdir(run_path)
        genre_links_path = os.path.join(run_path, dataset_name)

        print(f"├─ start time: {datetime.datetime.now()}")
        print(f"└─ output dataset location:  {genre_links_path}")
        print("starting...\n")

        # getting the songs
        total_songs, avg_time = get_songs(genre_links_path)

        print("\nfinished!")
        print(f"├─ finish time: {datetime.datetime.now()}")
        print(f"└─ total songs: {total_songs}, avg time: {avg_time} mins")

    # loading the dataset
    # if -l not set, uses the last run's dataset
    print("\n--loading dataset--")
    if args.load and not args.scrape:
        if not os.path.exists(args.load):
            print(f"\t* '{args.load}' doesn't exist")
            return
        if not os.path.isdir(args.load):
            print(f"\t* '{args.load}' must be a directory")
            return

        run_path = args.load
        print(f"└─ loaded '{run_path}'")

    else:
        run_number = len(os.listdir(run_dir))
        dir_name = f"run_{str(run_number)}"
        run_path = os.path.join(run_dir, dir_name)

        print(f"└─ using defaults. loaded '{run_path}' (last 'run' session)")

    # getting dataset info
    if args.info:
        path = os.path.join(run_path, dataset_name)
        with open(path, "r") as json_file:
            data_set = json.load(json_file)
            sample_size, mean, std_dev, var, common, common_percent, genres = project_utils.dataset_info(data_set)

            print("\n--dataset info--")
            print(f"'{dataset_name}'...")
            print(f"* sample size: {sample_size}")
            print(f"* mean genre size: {round(mean, 3)}")
            print(f"* standard deviation of genre size: {round(std_dev, 3)}")
            print(f"* variance of genre size: {round(var, 3)}")
            print(f"* uniqueness: {round((1 - common_percent) * 100, 3)}% - {common} shared songs between different genres")
            print("\t└─ percentage of songs seen in other genres:")
            for genre, common_count in genres.items():
                if len(data_set[genre]) > 0:
                    percent = round((common_count / len(data_set[genre])) * 100, 3)
                    print(f"\t\t- {genre} - {percent}%")

    # preprocessing the datset
    if args.preprocess:
        print("\n--pre-processing dataset--")


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)

    # with open("datasets/scraper_runs/run_1/genre-links.json", "r") as json_file:
    #     data_set = json.load(json_file)
    #     sample_size, mean, std_dev, var = scraper_utils.dataset_info(data_set)
