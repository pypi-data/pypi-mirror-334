"""
Retrieve REST results from the MusicBrainz API

    import jsonpickle
    from music_brainz_api_micro.music_brainz_api import MusicBrainzAPI as MB

    mb = MB()
    artist = mb.get_artist_by_mbid(
        "35f92c4a-69d0-4ed1-ab9e-05259db89d14"
        )
    if artist.error is False:
        artist_obj = jsonpickle.decode(artist.reponse)
        print(artist_obj["sort-name"])
"""
from .music_brainz_api import MusicBrainzAPI

VERSION = (0,1,8)

VERSION_STRING = '.'.join(map(str, VERSION))

MusicBrainzAPI
