import psycopg2




def get_connection(dbname):
    return psycopg2.connect(f"dbname = {dbname}")

def add_artist(conn,artist_name):
    
    with conn.cursor() as curs:
        curs.execute("insert into artists(name) values(%s)", (artist_name,))
        curs.execute("select id from artists order by id DESC")
        id = curs.fetchone()[0]
        conn.commit()
        return id


def add_song(conn,song_name, artist_id, lyrics):
    
    with conn.cursor() as curs:
        curs.execute("insert into songs(name, artist_id, lyrics) values(%s, %s, %s)", (song_name, artist_id, lyrics))
        conn.commit()
      