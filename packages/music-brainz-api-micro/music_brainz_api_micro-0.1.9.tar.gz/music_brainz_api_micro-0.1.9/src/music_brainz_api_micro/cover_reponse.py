class CoverResponse():

    cover_track_mbid: str
    cover_track_title: str
    cover_track_artist: str
    original_work_mbid: str
    original_work_artist: str

    def __str__(self) -> str:
        return f"{self.cover_track_artist} - {self.cover_track_title}"

    def __repr__(self) -> str:
        return f"{self.cover_track_artist} - {self.cover_track_title}"
