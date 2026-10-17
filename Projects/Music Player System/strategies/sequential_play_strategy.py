from strategies.play_strategy import PlayStrategy
from models.playlist import Playlist
from models.song import Song


class SequentialPlayStrategy(PlayStrategy):

    def __init__(self):
        self._current_playlist: Playlist | None = None
        self._current_index: int = -1

    def set_playlist(self, playlist: Playlist):
        self._current_playlist = playlist
        self._current_index = -1

    def has_next(self) -> bool:
        if self._current_playlist is None:
            return False
        return (self._current_index + 1) < self._current_playlist.get_size()

    def next(self) -> Song:
        if self._current_playlist is None or self._current_playlist.get_size() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")

        self._current_index += 1
        return self._current_playlist.songs[self._current_index]

    def has_previous(self) -> bool:
        return self._current_playlist is not None and (self._current_index - 1 >= 0)

    def previous(self) -> Song:
        if self._current_playlist is None or self._current_playlist.get_size() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")

        self._current_index -= 1
        return self._current_playlist.songs[self._current_index]

