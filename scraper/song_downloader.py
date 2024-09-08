import json

import yt_dlp

def download_genre(links, genre, path):
    i = 1
    for link in links:
        file_name = genre + f"_{str(i)}"
        opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{path}/{file_name}.%(ext)s',
        }

        _download_music(link, opts)
        i += 1

def _download_music(url, opts):
    try:
        with yt_dlp.YoutubeDL(opts) as downloader:
            downloader.download(url)
    except yt_dlp.DownloadError:
        print(f"couldn't download playlist: {url}")