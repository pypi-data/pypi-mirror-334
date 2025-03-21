from cProfile import Profile
from pstats import SortKey, Stats
from src.music_brainz_api_micro import MusicBrainzAPI as MB


def create_mb():
    mb = MB()
    mb.clear_cache()
    artist_mbid_list = ['35f92c4a-69d0-4ed1-ab9e-05259db89d14']
    artist = mb.get_artist_by_mbid(artist_mbid_list[0])


with Profile() as profile:
    print(f"{create_mb()=}")
    (
        Stats(profile)
        .strip_dirs()
        .sort_stats(SortKey.TIME)
        .print_stats()
    )
