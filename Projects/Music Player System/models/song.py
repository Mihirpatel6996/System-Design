
from dataclasses import dataclass


class Song:
    def __init__(self, title: str, artist: str, file_path: str):
        self._title = title
        self._artist = artist
        self._file_path = file_path

    @property  # preperty decorator allows us to access the title attribute as a property
    def title(self):
        return self._title

    @property
    def artist(self):
        return self._artist

    @property
    def file_path(self):
        return self._file_path



