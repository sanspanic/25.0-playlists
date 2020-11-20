"""Forms for playlist app."""

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.validators import InputRequired

class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    name = StringField('Playlist Name', 
                        validators=[InputRequired(message='Playlist name cannot be blank.')])
    
    description = StringField('Description', 
                        validators =[InputRequired(message='Playlist description cannot be blank.')])

class SongForm(FlaskForm):
    """Form for adding songs."""

    title = StringField('Song Title', 
                        validators=[InputRequired(message='Song title cannot be blank.')])
    
    artist = StringField('Artist', 
                        validators =[InputRequired(message='Artist cannot be blank.')])

class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField('Song To Add', coerce=int)

