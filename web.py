from flask import Flask,url_for,render_template,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_accept import accept

import time

app = Flask("lyrics")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///lyrics'
db = SQLAlchemy(app)

class Artists(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    songs = db.relationship("Songs", back_populates = "artist")

    def __repr__(self):
        return f"Artists('{self.name}')"

class Songs(db.Model):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable = False)
    lyrics = db.Column(db.String)
    artist = db.relationship("Artists", back_populates = "songs")

    def __repr__(self):
        return f"Songs('{self.name}')"

@app.route("/")
def index():
    artists = Artists.query.all()
    n_artists = len(artists)
    return render_template('artists.html', no_of_artists = n_artists ,artists = artists)

@app.route("/artist/<int:artist_id>")
def artist(artist_id):
    
    songs = Songs.query.filter_by(artist_id = artist_id).all()
    
    artists = Artists.query.get(artist_id)

    return render_template('songs.html',artist = artists, songs = songs)


@app.route("/song/<int:song_id>")
@accept("text/html")
def song(song_id):
    song = Songs.query.filter_by(id = song_id).first()
    songs = song.artist.songs
    return render_template('lyrics.html', song = song, songs = songs)  


# @app.route("/lyrics/<int:song_id>")
# def lyrics(song_id):
#     song = Songs.query.filter_by(id = song_id).first()
#     time.sleep(2)
#     return render_template("song-lyrics.html",song = song)



@song.support("application/json")
def song_json(song_id):
    print ("I'm returning json!")
    time.sleep(2)
    song = Songs.query.filter_by(id = song_id).first()
    ret = dict(song = dict(name = song.name,
                           lyrics = song.lyrics,
                           id = song.id,
                           artist = dict(name = song.artist.name,
                                         id = song.artist.id)))
    return jsonify(ret)
