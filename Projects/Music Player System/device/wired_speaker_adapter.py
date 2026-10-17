from device.audio_output_device import IAudioOutputDevice
from models.song import Song
from external.wired_speaker_api import WiredSpeakerAPI


class WiredSpeakerAdapter(IAudioOutputDevice):
    def __init__(self, wired_api: WiredSpeakerAPI):
        self._wired_api = wired_api

    def play_audio(self, song: Song):
        payload = f"{song.title} by {song.artist}"
        self._wired_api.play_sound_via_cable(payload)