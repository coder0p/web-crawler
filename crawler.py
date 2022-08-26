import argparse
import logging
import os


import requests
from bs4 import BeautifulSoup


import db
import web
import alchamey

logger = None
dbname = "lyrics"

def parse_args():
    parser = argparse.ArgumentParser(description = "Web crawler")
    parser.add_argument("-d", "--debug", help = "Enable debug logging", action="store_true")
    parser.add_argument("--db", help="Name of database to use")
    subcommands = parser.add_subparsers(help="Commands", dest="command", required=True)
    subcommands.add_parser("addir", help="Adding directory named artists to store lyrics")
    subcommands.add_parser("initdb", help="Initialise the database")
    subcommands.add_parser("crawl", help="Perform a crawl")
    subcommands.add_parser("web", help="Start web server")
    return parser.parse_args()

def configure_logging(level=logging.DEBUG):
    global logger
    logger = logging.getLogger("crawler")
    logger.setLevel(level)
    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(level)
    formatter = logging.Formatter("[%(levelname)s] : %(filename)s(%(lineno)d) : %(message)s")
    screen_handler.setFormatter(formatter)
    logger.addHandler(screen_handler)


def get_artists_list(base):
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
        for heading in headings[:10]:
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
    songs = track.find_all('a')
    if songs:
        logger.debug("song list parsed successfully")
        for song in songs[:5]:
            songs_link[song.text] = song["href"]
            
    else:
        logger.debug("song list could not parsed successfully")

    return songs_link


def get_song_lyrics(base):
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

    for artist_name ,artist_link in get_artists_list("https://www.songlyrics.com/top-artists-lyrics.html").items():
        logger.debug("Artist:  %s", artist_name)
        artist_dirt = os.path.join(download_dir, artist_name)
        artist_dirt = artist_dirt.lower()
        os.makedirs(artist_dirt, exist_ok=True)
        
        for song, song_link in get_song_list(artist_link).items():
            song_name = song.replace("/","-")
            song_name = song_name.lower()
            with open(f"{artist_dirt}/{song_name}-lyrics.txt",'w') as file:
                n_bytes = file.write(get_song_lyrics(song_link))
                if n_bytes < 5:
                    logger.debug("File size is too short!")
                else:
                    logger.debug("File downloaded successfully")


def create_tables():
    """This function creates table with given sql file into the database mentioned """

    conn = db.get_connection(dbname)
    with conn.cursor() as cursor:
        with open("init.sql") as f:
            sql = f.read()
            cursor.execute(sql)
    conn.commit()
    

def add_database():
    """ This function adds the artist name and song's lyrics into database """

    conn = db.get_connection(dbname)
    for artist_name, artist_link in get_artists_list('http://www.songlyrics.com/top-artists-lyrics.html').items():
        artist_name = artist_name.replace("/", " ")
        last_id = alchamey.add_artist(artist_name)
        for song_name, song_link in get_song_list(artist_link).items():
            song_name = song_name.replace("/"," ")
            lyrics = get_song_lyrics(song_link)
            alchamey.add_song(song_name, lyrics,last_id)
            logger.debug("%s added and corresponding %s song and lyrics",artist_name,song_name)
    logger.info("Data adding successful, connection is closing.....")
    conn.close()



def main():
    args = parse_args()

    if args.debug:
        configure_logging(logging.DEBUG)
    else:
        configure_logging(logging.INFO)

    
    if args.command == "crawl":
        logger.info("Scraping song-lyrics.com ....")
        add_database()
        logger.info("Scraping completed!")
    elif args.command == "initdb":
        logger.info("Initializing database....")
        alchamey.create_table()
        logger.info("%s database initialized!!", dbname)
    elif args.command == "addir":
        logger.info("Creating directory...")
        crawl('artists')
        logger.info("Directory created successfully!")
    elif args.command == "web":
        logger.info("starting web server")
        web.app.run()

    else:
        logger.warning("%s not implemented!!!", args.command)
    

 

if __name__ == "__main__":
    main()
    