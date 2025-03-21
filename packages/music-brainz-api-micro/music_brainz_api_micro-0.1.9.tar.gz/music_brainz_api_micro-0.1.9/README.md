# MusicBrainzAPI

A series of scripts that enable retrieving information from MusicBrainz API: https://musicbrainz.org/doc/MusicBrainz_API

# Usage

When calling the public functions you will usually get a `Response` object. You can check the `error` property to determine if the REST call was successful, `error_text` will attempt to hold some more useful information regarding the error.

Once successful the `response` property contains the expected data structure from MusicBrainz

```python
import jsonpickle
from music_brainz_api_micro import MusicBrainzAPI as MB

mb = MB()
result = mb.get_artist_by_mbid(
    "35f92c4a-69d0-4ed1-ab9e-05259db89d14"
    )
if result.error is False:
    artist_obj = jsonpickle.decode(result.reponse)
    print(artist_obj["sort-name"])
    # "At the Gates"
```

# Functions

Get artist data using unique identifier

```
get_artist_by_mbid(mbid)
```

Get all releases by artist

```
get_releases_by_artist(mbid)
```

Get just a list of release titles

```
get_release_titles_by_artist(mbid)
```

# Maintenance

Safely delete all cache files, default in `$HOME/.cache/MusicBrainzAPI`

# Build

```python
python -m build
python -m twine upload dist/*
```
