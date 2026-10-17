from abc import ABC, abstractmethod
from models.playlist import Playlist
from models.song import Song


class PlayStrategy(ABC):

    @abstractmethod
    def set_playlist(self, playlist: Playlist):
        pass

    @abstractmethod
    def next(self) -> Song:
        pass

    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def previous(self) -> Song:
        pass

    @abstractmethod
    def has_previous(self) -> bool:
        pass

    # Optional extension hook (default behavior)
    def add_to_next(self, song: Song):
        pass