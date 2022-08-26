WEB CRAWLER

--> crawling artist's names, songs, and corresponding lyrics to database 

--> Also had a funtion to scrap the data and download to the local directory named called artists/, in that lyrics stored corresponding to the songs name

--> usage: crawler.py [-h] [-d] [--db DB] {addir,initdb,crawl,web} ...

    Do following arguments for working:
    
    - to create table and initiate connection :
                    python3 crawler.py initdb
    
    - to crawl data from web and insert values:
                    python3 crawler.py crawl
    
    -to run the template in localhost:
                    python3 crawler.py web
