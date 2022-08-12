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


def crawl(base):
    
    logger.debug("Crawling starting")
    for link in a
        
    logger.debug("Completed crawling")

def main():

    args = parse_args()
    if args.debug:
        configure_logging(logging.DEBUG)
    else:
        configure_logging(logging.INFO)
   
    crawl("http://www.songlyrics.com/top-artists-lyrics.html")


if __name__ == "__main__":
    main()