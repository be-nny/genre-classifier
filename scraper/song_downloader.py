import yt_dlp

def download_genre(links, genre, path):
    """
    Downloads a set of songs associated with a genre.

    Args:
        links (list): Array of song links
        genre (str):  Genre name
        path (str): Path to save downloaded song
    """

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

        download_music(link, opts)
        i += 1

def download_music(url, opts):
    """
    Downloads a song given the URL.

    Args:
        url (str): URL of the song
        opts (dict): Download options
    """

    try:
        with yt_dlp.YoutubeDL(opts) as downloader:
            downloader.download(url)
    except yt_dlp.DownloadError:
        print(f"couldn't download playlist: {url}")