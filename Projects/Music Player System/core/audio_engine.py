from models.song import Song
from device.audio_output_device import IAudioOutputDevice


class AudioEngine:
    def __init__(self):
        self._current_song: Song | None = None
        self._is_paused: bool = False

    def get_current_song_title(self) -> str:
        if self._current_song:
            return self._current_song.title
        return ""

    def is_paused(self) -> bool:
        return self._is_paused

    def play(self, device: IAudioOutputDevice, song: Song):
        if song is None:
            raise ValueError("Cannot play a null song.")

        # Resume logic
        if self._is_paused and self._current_song == song:
            self._is_paused = False
            print(f"Resuming song: {song.title}")
            device.play_audio(song)
            return

        # Fresh play
        self._current_song = song
        self._is_paused = False
        print(f"Playing song: {song.title}")
        device.play_audio(song)

    def pause(self):
        if self._current_song is None:
            raise RuntimeError("No song is currently playing to pause.")

        if self._is_paused:
            raise RuntimeError("Song is already paused.")

        self._is_paused = True
        print(f"Pausing song: {self._current_song.title}")