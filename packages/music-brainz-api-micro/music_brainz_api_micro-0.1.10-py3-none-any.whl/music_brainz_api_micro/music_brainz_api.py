"""
Provides a class and functions to manage sending requests to
MusicBrainz. Calls will include an entire second of waiting
to conform to MusicBrainz API standards
"""
import logging

import jsonpickle
from rest_client_micro import Response as R
from rest_client_micro import BaseRESTAPI
from .cover_reponse import CoverResponse as CR


class MusicBrainzAPI(BaseRESTAPI):
    """
    Main class to run API calls against MusicBrainz
    """

    logging.basicConfig(
        format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)
    debug: bool = False

    def _debug(self, message: str):
        if self.debug:
            logging.debug(str(message))

    def __init__(self,
                 config_dir: str = None,
                 cache_dir: str = None,
                 cache_timeout_mins: int = 10800,
                 force_cache: bool = False,
                 use_cache: bool = True) -> None:
        """Initialise a MusicBrainzAPI instance

        :param config_dir: Directory to store/use configuration
        :param cache_dir: Directory to store cached data
        :param cache_refresh_mins: Duration to store cache data
            (default 10800 minutes)
        :param force_cache: Bypass cached data and force a rest call
            (default False)
        :param use_cache: Store and read results from cache
            (default True)
        """
        app_name = 'MusicBrainzAPI'
        root_endpoint = 'https://musicbrainz.org/ws/2/'
        user_agent = 'MusicBrainzAPI/0.1 (https://github.com/samuelshiels/MusicBrainzAPI)'
        sleep_ms = 1100
        basic_auth = None

        super().__init__(app_name, root_endpoint, user_agent, sleep_ms, basic_auth,
                         config_dir, cache_dir, cache_timeout_mins, force_cache, use_cache)

    def get_artist_by_mbid(self, mbid: str) -> R:
        """ Using the MusicBrainz ID of an artist returns the full
        MusicBrainz response

        :param mbid: MusicBrainz ID including dashes
        :returns: Response, check for error property True or False, if 
            False 'response' property can be used
        """
        return self._run_call(f'artist/{mbid}', {'inc': 'aliases+release-groups'}, "get", mbid)

    def get_releases_by_artist(self, mbid: str) -> R:
        """Using the MusicBrainz ID of an artist returns the full
        MusicBrainz response with `release-groups`

        :param mbid: MusicBrainz ID including dashes
        :returns: Response, check for error property True or False, if 
            False 'response' property can be used
        """
        return self._run_call(f'artist/{mbid}', {'inc': 'aliases+release-groups'}, "get", mbid)

    def get_release(self, mbid: str) -> R:
        """Using the MusicBrainz ID of a release, returns the release response 
        https://musicbrainz.org/doc/Release

        :param mbid: MusicBrainz Id for the release, dashes included
        :returns: Response, check for error property True or False, if 
            False 'response' property can be used
        """
        return self._run_call(f"release/{mbid}", {'inc': 'aliases+artist-credits+labels+discids+recordings'}, "get", mbid)

    def get_release_group(self, mbid: str) -> R:
        """Using the MusicBrainz ID of a release, returns the release response 
        https://musicbrainz.org/doc/Release

        :param mbid: MusicBrainz Id for the release, dashes included
        :returns: Response, check for error property True or False, if 
            False 'response' property can be used
        """
        return self._run_call(f"release-group/{mbid}", {'inc': 'aliases+artist-credits'}, "get", mbid)

    def get_release_titles_by_artist(self, mbid: str) -> list[str] | list[R]:
        """Runs a getReleasesByArtist but returns the release titles of the responses

        :param mbid: MusicBrainz ID including dashes
        :returns: List of release titles for the associated artist or the Response
            with the error message     
        """
        ret_val = []
        artist_releases = self.get_releases_by_artist(mbid)
        if artist_releases.error is True:
            ret_val.append(artist_releases)
            return ret_val
        thawed = jsonpickle.decode(artist_releases.response)
        for release in thawed['release-groups']:
            ret_val.append(release['title'])
        return ret_val

    def get_recording_cover(self, recording_mbid: str) -> CR | None:
        """From a recording mbid determines if it is a recording

        :param mbid: MusicBrainz recording ID including dashes
        :returns: CoverResponse object or None
        """
        recording_rels = self._run_call(
            f"recording/{recording_mbid}",
            {"inc": "aliases+work-rels+artist-credits"},
            "get",
            recording_mbid
        )
        if recording_rels.error is False:
            thawed = jsonpickle.decode(recording_rels.response)
            if 'relations' not in thawed:
                return None
            for r in thawed['relations']:
                if 'cover' in r['attributes']:
                    cr = CR()
                    cr.cover_track_mbid = recording_mbid
                    cr.cover_track_title = thawed['title']
                    cr.cover_track_artist = thawed['artist-credit'][0]['name']
                    cr.original_work_mbid = r['work']['id']
                    return cr
        return None
