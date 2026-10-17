from typing import Dict
from models.playlist import Playlist
from models.song import Song


class PlaylistManager:
    _instance = None

    def __init__(self):
        self._playlists: Dict[str, Playlist] = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PlaylistManager()
        return cls._instance

    def create_playlist(self, name: str):
        if name in self._playlists:
            raise Exception(f'Playlist "{name}" already exists.')

        self._playlists[name] = Playlist(name)

    def add_song_to_playlist(self, playlist_name: str, song: Song):
        if playlist_name not in self._playlists:
            raise Exception(f'Playlist "{playlist_name}" not found.')

        self._playlists[playlist_name].add_song_to_playlist(song)

    def get_playlist(self, name: str) -> Playlist:
        if name not in self._playlists:
            raise Exception(f'Playlist "{name}" not found.')

        return self._playlists[name]