from core.audio_engine import AudioEngine
from models.song import Song

from enums.device_type import DeviceType
from enums.play_strategy_type import PlayStrategyType

from managers.device_manager import DeviceManager
from managers.playlist_manager import PlaylistManager
from managers.strategy_manager import StrategyManager

from device.audio_output_device import IAudioOutputDevice
from strategies.play_strategy import PlayStrategy


class MusicPlayerFacade:

    _instance = None

    def __init__(self):
        self._audio_engine = AudioEngine()
        self._loaded_playlist = None
        self._play_strategy: PlayStrategy | None = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = MusicPlayerFacade()
        return cls._instance

    # ---------------- Device ----------------
    def connect_device(self, device_type: DeviceType):
        DeviceManager.get_instance().connect(device_type)

    # ---------------- Strategy ----------------
    def set_play_strategy(self, strategy_type: PlayStrategyType):
        self._play_strategy = StrategyManager.get_instance().get_strategy(strategy_type)

    # ---------------- Playlist ----------------
    def load_playlist(self, name: str):
        self._loaded_playlist = PlaylistManager.get_instance().get_playlist(name)

        if self._play_strategy is None:
            raise RuntimeError("Play strategy not set before loading playlist.")

        self._play_strategy.set_playlist(self._loaded_playlist)

    # ---------------- Core Playback ----------------
    def play_song(self, song: Song):
        if not DeviceManager.get_instance().has_output_device():
            raise RuntimeError("No audio device connected.")

        device = DeviceManager.get_instance().get_output_device()
        self._audio_engine.play(device, song)

    def pause_song(self, song: Song):
        if self._audio_engine.get_current_song_title() != song.title:
            raise RuntimeError("Cannot pause a song that is not currently playing.")

        self._audio_engine.pause()

    # ---------------- Playlist Playback ----------------
    def play_all_tracks(self):
        if self._loaded_playlist is None:
            raise RuntimeError("No playlist loaded.")

        while self._play_strategy.has_next():
            song = self._play_strategy.next()
            device = DeviceManager.get_instance().get_output_device()
            self._audio_engine.play(device, song)

        print(f"Completed playlist: {self._loaded_playlist.playlist_name}")

    def play_next_track(self):
        if self._loaded_playlist is None:
            raise RuntimeError("No playlist loaded.")

        if self._play_strategy.has_next():
            song = self._play_strategy.next()
            device = DeviceManager.get_instance().get_output_device()
            self._audio_engine.play(device, song)
        else:
            print(f"Completed playlist: {self._loaded_playlist.playlist_name}")

    def play_previous_track(self):
        if self._loaded_playlist is None:
            raise RuntimeError("No playlist loaded.")

        if self._play_strategy.has_previous():
            song = self._play_strategy.previous()
            device = DeviceManager.get_instance().get_output_device()
            self._audio_engine.play(device, song)
        else:
            print(f"Start of playlist reached.")

    # ---------------- Queue injection ----------------
    def enqueue_next(self, song: Song):
        if self._play_strategy is None:
            raise RuntimeError("Strategy not set.")
        self._play_strategy.add_to_next(song)