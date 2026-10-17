from typing import List

from models.song import Song

from managers.playlist_manager import PlaylistManager
from enums.device_type import DeviceType
from enums.play_strategy_type import PlayStrategyType

from music_player_facade import MusicPlayerFacade


class MusicPlayerApplication:

    _instance = None

    def __init__(self):
        self._song_library: List[Song] = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MusicPlayerApplication()
        return cls._instance

    # ---------------- Library ----------------
    def create_song_in_library(self, title: str, artist: str, path: str):
        song = Song(title, artist, path)
        self._song_library.append(song)

    def find_song_by_title(self, title: str) -> Song | None:
        for song in self._song_library:
            if song.title == title:
                return song
        return None

    # ---------------- Playlist management ----------------
    def create_playlist(self, playlist_name: str):
        PlaylistManager.get_instance().create_playlist(playlist_name)

    def add_song_to_playlist(self, playlist_name: str, song_title: str):
        song = self.find_song_by_title(song_title)

        if song is None:
            raise RuntimeError(f"Song '{song_title}' not found in library.")

        PlaylistManager.get_instance().add_song_to_playlist(playlist_name, song)

    # ---------------- Device control ----------------
    def connect_audio_device(self, device_type: DeviceType):
        MusicPlayerFacade.get_instance().connect_device(device_type)

    # ---------------- Playback configuration ----------------
    def select_play_strategy(self, strategy_type: PlayStrategyType):
        MusicPlayerFacade.get_instance().set_play_strategy(strategy_type)

    def load_playlist(self, playlist_name: str):
        MusicPlayerFacade.get_instance().load_playlist(playlist_name)

    # ---------------- Playback controls ----------------
    def play_single_song(self, song_title: str):
        song = self.find_song_by_title(song_title)

        if song is None:
            raise RuntimeError(f"Song '{song_title}' not found.")

        MusicPlayerFacade.get_instance().play_song(song)

    def pause_current_song(self, song_title: str):
        song = self.find_song_by_title(song_title)

        if song is None:
            raise RuntimeError(f"Song '{song_title}' not found.")

        MusicPlayerFacade.get_instance().pause_song(song)

    def play_all_tracks_in_playlist(self):
        MusicPlayerFacade.get_instance().play_all_tracks()

    def play_previous_track_in_playlist(self):
        MusicPlayerFacade.get_instance().play_previous_track()

    def queue_song_next(self, song_title: str):
        song = self.find_song_by_title(song_title)

        if song is None:
            raise RuntimeError(f"Song '{song_title}' not found.")

        MusicPlayerFacade.get_instance().enqueue_next(song)