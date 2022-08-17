import argparse
import logging
import os


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
    """Returns a dictionary of artists with argument of popular artist link"""
    
    artists = {}
    logger.debug("requesting %s ...",base)
    res = requests.get(base)
    logger.debug("status: %s",res.status_code)
    soup = BeautifulSoup(res.content, "lxml")
    tracklist = soup.find("table", attrs={"class": "tracklist"})
    headings = tracklist.find_all('h3')
    if headings:
        logger.debug('artist list parsed successfully')
        for heading in headings[:5]:
            artists[heading.text] = heading.a['href']
    else:
        logger.debug("artist list could not parsed successfully")

    return artists
    

def get_song_list(base):
    """Returns a dictionary of song's links with given artist"""

    songs_link = {}
    logger.debug("requesting %s...",base)
    res = requests.get(base)
    logger.debug("status: %s",res.status_code)
    soup = BeautifulSoup(res.content, "lxml")
    track = soup.find("table", attrs={"class": "tracklist"})
    links = track.find_all('a')
    if links:
        logger.debug("song list parsed successfully")
        for link in links[:5]:
            songs_link[link.text] = link["href"]
    else:
        logger.debug("song list could not parsed successfully")

    return songs_link


def get_lyrics(base):
    """Return lyrics string which is corresponding to selected song"""

    logger.debug(f"requesting {base} ...")
    res = requests.get(base)
    logger.debug("status: %s",res.status_code)
    soup = BeautifulSoup(res.content, "lxml")
    lyrics = soup.find("p", attrs={"id": "songLyricsDiv"})
    if lyrics:
        logger.debug("lyrics parsed successfully")
    else:
        logger.debug("lyrics could not parsed successfully")

    return lyrics.text


def crawl(download_dir):
    """Funtion for downloading lyrics and storing in artist's directory"""

    for artist_name ,artist_link in get_artists("https://www.songlyrics.com/top-artists-lyrics.html").items():
        logger.debug("Artist:  %s", artist_name)
        artist_dirt = os.path.join(download_dir, artist_name)
        artist_dirt = artist_dirt.lower()
        os.makedirs(artist_dirt, exist_ok=True)
        
        for song, song_link in get_song_list(artist_link).items():
            song_name = song.replace("/","-")
            song_name = song_name.lower()
            with open(f"{artist_dirt}/{song_name}-lyrics.txt",'w') as file:
                n_bytes = file.write(get_lyrics(song_link))
                if n_bytes < 5:
                    logger.debug("File size is too short!")
                else:
                    logger.debug("File downloaded successfully")

    
def main():
    args = parse_args()
    if args.debug:
        configure_logging(logging.DEBUG)
    else:
        configure_logging(logging.INFO)
    
    crawl('artists')

if __name__ == "__main__":
    main()