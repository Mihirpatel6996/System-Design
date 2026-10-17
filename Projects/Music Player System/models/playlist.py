from typing import List
from models.song import Song


class Playlist:
    def __init__(self, name: str):
        self._playlist_name = name
        self._songs: List[Song] = []

    @property
    def playlist_name(self):
        return self._playlist_name

    @property
    def songs(self):
        return self._songs

    def get_size(self) -> int:
        return len(self._songs)

    def add_song_to_playlist(self, song: Song):
        if song is None:
            raise ValueError("Cannot add null song to playlist.")
        self._songs.append(song)