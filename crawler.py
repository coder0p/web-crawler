import argparse
import logging

import requests
from bs4 import BeautifulSoup

logger = None

def parse_args():
    parser = argparse.ArgumentParser(description = "Web crawler")
    parser.add_argument("-d", "--debug", help = "Enable debug logging", action="store_true")
    return parser.parse_args()

def configure_logging(level=logging.INFO):
    global logger
    logger = logging.getLogger("crawler")
    logger.setLevel(level)
    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(level)
    formatter = logging.Formatter("[%(levelname)s] : %(filename)s(%(lineno)d) : %(message)s")
    screen_handler.setFormatter(formatter)
    logger.addHandler(screen_handler)


def get_artists(base):
    artists = {}
    logger.debug(f"requesting {base} ...")
    res = requests.get(base)
    logger.debug(f"status: {res.status_code}")
    soup = BeautifulSoup(res.content, "lxml")
    tracklist = soup.find("table", attrs={"class": "tracklist"})
    headings = tracklist.find_all('h3')
    if headings:
        logger.debug('artist list parsed successfully')
    for heading in headings:
        artists[heading.text] = heading.a['href']
    else:
        logger.debug("Something went wrong!")

    return artists
    

def get_song_list(base):
    songsLink = {}
    logger.debug(f"requesting {base} ...")
    res = requests.get(base)
    logger.debug(f"status: {res.status_code}")
    soup = BeautifulSoup(res.content, "lxml")
    track = soup.find("table", attrs={"class": "tracklist"})
    links = track.find_all('a')
    if links:
        logger.debug("song list parsed successfully")
    for link in links:
        songsLink[link.text] = link["href"]
    else:
        logger.debug("Something went wrong!")


    return songsLink


def get_lyrics(base):
    logger.debug(f"requesting {base} ...")
    res = requests.get(base)
    logger.debug(f"status: {res.status_code}")
    soup = BeautifulSoup(res.content, "lxml")
    lyrics = soup.find("p", attrs={"id": "songLyricsDiv"})
    if lyrics:
        logger.debug("lyrics parsed successfully")
    else:
        logger.debug("Something went wrong!")

    return lyrics.text


def main():
    args = parse_args()
    if args.debug:
        configure_logging(logging.DEBUG)
    else:
        configure_logging(logging.INFO)
    
    artists = get_artists("https://www.songlyrics.com/top-artists-lyrics.html")
    songsLink = get_song_list(list(artists.values())[0]) #passing link of first song
    lyrics = get_lyrics(list(songsLink.values())[0]) #passing link of first song's lyrics


if __name__ == "__main__":
    main()