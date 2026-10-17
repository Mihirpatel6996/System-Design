from collections import deque
from typing import List

from strategies.play_strategy import PlayStrategy
from models.playlist import Playlist
from models.song import Song


class CustomQueueStrategy(PlayStrategy):

    def __init__(self):
        self._current_playlist: Playlist | None = None
        self._current_index: int = -1

        self._next_queue: deque[Song] = deque()
        self._prev_stack: List[Song] = []

    def set_playlist(self, playlist: Playlist):
        self._current_playlist = playlist
        self._current_index = -1
        self._next_queue.clear()
        self._prev_stack.clear()

    def has_next(self) -> bool:
        if self._current_playlist is None:
            return False
        return (self._current_index + 1) < self._current_playlist.get_size()

    # ---------- internal sequential ----------
    def _next_sequential(self) -> Song:
        if self._current_playlist is None or self._current_playlist.get_size() == 0:
            raise RuntimeError("Playlist is empty.")

        self._current_index += 1
        return self._current_playlist.songs[self._current_index]

    def _previous_sequential(self) -> Song:
        if self._current_playlist is None or self._current_playlist.get_size() == 0:
            raise RuntimeError("Playlist is empty.")

        self._current_index -= 1
        return self._current_playlist.songs[self._current_index]

    # ---------- public API ----------
    def next(self) -> Song:
        if self._current_playlist is None or self._current_playlist.get_size() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")

        # 1. priority queue first
        if self._next_queue:
            song = self._next_queue.popleft()
            self._prev_stack.append(song)
            self._sync_index(song)
            return song

        # 2. fallback sequential
        song = self._next_sequential()
        self._prev_stack.append(song)
        return song

    def has_previous(self) -> bool:
        return len(self._prev_stack) > 0

    def previous(self) -> Song:
        if self._current_playlist is None or self._current_playlist.get_size() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")

        if self._prev_stack:
            song = self._prev_stack.pop()
            self._sync_index(song)
            return song

        return self._previous_sequential()

    def add_to_next(self, song: Song):
        if song is None:
            raise RuntimeError("Cannot enqueue null song.")
        self._next_queue.append(song)

    # ---------- helper ----------
    def _sync_index(self, song: Song):
        for i, s in enumerate(self._current_playlist.songs):
            if s == song:
                self._current_index = i
                break