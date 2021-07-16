import os
import youtube_dl


def clean_all_mp3(direct):
    """
    Cleans all mp3 files from directory
    :param direct:
    :return:
    """
    for file in os.listdir(direct):
        if file.endswith(".mp3"):
            os.remove(file)


def download_mp3(ydl_opts, link):
    """
    downloads a youtube music video into an mp3 file then returns information
    about the downloaded mp3 file
    :param ydl_opts:
    :param link:
    :return information about the downloaded file:
    """
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
        info = ydl.extract_info(link, download=False)
        return info


def rename_mp3(direct, info):
    """
    renames every mp3 file in directory to the name of the song downloaded
    :param direct:
    :param info:
    :return:
    """
    for file in os.listdir(direct):
        if file.endswith(".mp3"):
            os.rename(file, f"{info['title']}.mp3")
