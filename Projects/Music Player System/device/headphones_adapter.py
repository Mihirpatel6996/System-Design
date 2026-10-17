from device.audio_output_device import IAudioOutputDevice
from models.song import Song
from external.headphones_api import HeadphonesAPI


class HeadphonesAdapter(IAudioOutputDevice):
    def __init__(self, headphones_api: HeadphonesAPI):
        self._headphones_api = headphones_api

    def play_audio(self, song: Song):
        payload = f"{song.title} by {song.artist}"
        self._headphones_api.play_sound_via_jack(payload)