"""
Test cases for MusicBrainzAPI uses hardcoded ID for artist
 At the Gates
"""

import jsonpickle
from src.music_brainz_api_micro.music_brainz_api import MusicBrainzAPI as MB

def test_get_recording_cover():
    """
    Checking if a recording is a cover
    """
    mb = MB()
    # mb.root_endpoint = "http://127.0.0.1:3000/"
    recording_mbid = 'f4946271-1064-4496-8b9a-674212a7d0fa'
    #recording_mbid = '23456'
    cover_response = mb.get_recording_cover(recording_mbid)
    assert cover_response is not None
    assert cover_response.cover_track_mbid == recording_mbid
    assert cover_response.cover_track_artist == 'Children of Bodom'
    assert cover_response.original_work_mbid == '19862b40-6a25-3499-8b8c-2a647007d1bb'

def test_get_artist_by_mbid():
    """
    Run a simple call with one mbid, confirm it is the correct
    artist by checking type and sort-name
    """
    mb = MB()
    # mb.root_endpoint = "http://127.0.0.1:3000/"
    artist_mbid_list = ['35f92c4a-69d0-4ed1-ab9e-05259db89d14']
    artist = mb.get_artist_by_mbid(artist_mbid_list[0])
    if artist.error:
        assert("123" == artist.error_text)
    assert artist.error is False
    thawed = jsonpickle.decode(artist.response)
    assert thawed['type'] == "Group"
    assert thawed['sort-name'] == "At the Gates"


def test_get_release_titles_by_artist():
    """
    Test returning the full release list of an artist, implicitly
    tests get_releases_by_artist, we tentively check the length
    of the returned array
    """
    mb = MB()
    # mb.root_endpoint = "http://127.0.0.1:3000/"
    artist_mbid_list = ['35f92c4a-69d0-4ed1-ab9e-05259db89d14']
    releases = mb.get_release_titles_by_artist(artist_mbid_list[0])
    assert len(releases) > 24
