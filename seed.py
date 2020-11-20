"""seed file to make sample data"""

from models import Song, Playlist, PlaylistSong, db
from app import app

def drop_everything():
    """(On a live db) drops all foreign key constraints before dropping all tables.
    Workaround for SQLAlchemy not doing DROP ## CASCADE for drop_all()
    (https://github.com/pallets/flask-sqlalchemy/issues/722)
    """
    from sqlalchemy.engine.reflection import Inspector
    from sqlalchemy.schema import DropConstraint, DropTable, MetaData, Table

    con = db.engine.connect()
    trans = con.begin()
    inspector = Inspector.from_engine(db.engine)

    # We need to re-create a minimal metadata with only the required things to
    # successfully emit drop constraints and tables commands for postgres (based
    # on the actual schema of the running instance)
    meta = MetaData()
    tables = []
    all_fkeys = []

    for table_name in inspector.get_table_names():
        fkeys = []

        for fkey in inspector.get_foreign_keys(table_name):
            if not fkey["name"]:
                continue

            fkeys.append(db.ForeignKeyConstraint((), (), name=fkey["name"]))

        tables.append(Table(table_name, meta, *fkeys))
        all_fkeys.extend(fkeys)

    for fkey in all_fkeys:
        con.execute(DropConstraint(fkey))

    for table in tables:
        con.execute(DropTable(table))

    trans.commit()

#create all tables
drop_everything()
#db.drop_all()
db.create_all()

#if table isn't empty, empty it
PlaylistSong.query.delete()
Playlist.query.delete()
Song.query.delete()

#add songs
s1 = Song(title='Yellow Submarine', artist='The Beatles')
s2 = Song(title='Stealing', artist='Bob Dylan')
s3 = Song(title='Wild Side', artist='Lou Reed')
s4 = Song(title='Noise', artist='Noise Factory')
s5 = Song(title='Toxic', artist='Britney Spears')

#add new objects to session, so they persist
db.session.add_all([s1, s2, s3, s4, s5])
db.session.commit()

#add playlists
p1 = Playlist(name='1st Playlist', description='pop songs')
p2 = Playlist(name='2nd Playlist', description='best songs ever')

#add new objects to session & commit
db.session.add_all([p1, p2])
db.session.commit()

#add playlist_songs
ps1 = PlaylistSong(playlist_id=1, song_id=5)
ps2 = PlaylistSong(playlist_id=1, song_id=4)
ps3 = PlaylistSong(playlist_id=2, song_id=3)
ps4 = PlaylistSong(playlist_id=2, song_id=5)
ps5 = PlaylistSong(playlist_id=2, song_id=2)
ps6 = PlaylistSong(playlist_id=2, song_id=1)

#add new objects to session & commit
db.session.add_all([ps1, ps2, ps3, ps4, ps5, ps6])
db.session.commit()


