from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy


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
    return render_template('artists.html', artists = artists)

@app.route("/artist/<int:artist_id>")
def artist(artist_id):
    
    songs = Songs.query.filter_by(artist_id = artist_id).all()
    
    artist = Artists.query.get(artist_id)

    return render_template('songs.html',artist = artist.name, songs = songs)

@app.route("/song/<int:song_id>")
def song(song_id):
    song = Songs.query.filter_by(id = song_id).first()
    lyrics = song.lyrics.replace("\n","<br>")
    return render_template('lyrics.html', song_name =song.name, lyrics=lyrics)  



