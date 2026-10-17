import random
from typing import List

from strategies.play_strategy import PlayStrategy
from models.playlist import Playlist
from models.song import Song


class RandomPlayStrategy(PlayStrategy):

    def __init__(self):
        self._current_playlist: Playlist | None = None
        self._remaining_songs: List[Song] = []
        self._history: List[Song] = []
        self._random = random.Random()

    def set_playlist(self, playlist: Playlist):
        self._current_playlist = playlist

        if playlist is None or playlist.get_size() == 0:
            self._remaining_songs = []
            self._history = []
            return

        # copy songs (important: avoid mutating original playlist)
        self._remaining_songs = list(playlist.songs)
        self._history = []

    def has_next(self) -> bool:
        return self._current_playlist is not None and len(self._remaining_songs) > 0

    def next(self) -> Song:
        if self._current_playlist is None or self._current_playlist.get_size() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")

        if not self._remaining_songs:
            raise RuntimeError("No songs left to play.")

        idx = self._random.randint(0, len(self._remaining_songs) - 1)
        selected_song = self._remaining_songs[idx]

        # O(1) removal using swap-and-pop
        last_index = len(self._remaining_songs) - 1
        self._remaining_songs[idx] = self._remaining_songs[last_index]
        self._remaining_songs.pop()

        self._history.append(selected_song)
        return selected_song

    def has_previous(self) -> bool:
        return len(self._history) > 0

    def previous(self) -> Song:
        if not self._history:
            raise RuntimeError("No previous song available.")

        return self._history.pop()