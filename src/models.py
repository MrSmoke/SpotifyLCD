class CurrentTrack:
    def __init__(self, name: str, artist: str, album: str, is_playing: bool = True) -> None:
        self.name = name
        self.artist = artist
        self.album = album
        self.is_playing = is_playing


class ApiError:
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
