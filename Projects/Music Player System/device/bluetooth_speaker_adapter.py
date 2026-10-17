from device.audio_output_device import IAudioOutputDevice
from models.song import Song
from external.bluetooth_speaker_api import BluetoothSpeakerAPI


class BluetoothSpeakerAdapter(IAudioOutputDevice):
    def __init__(self, bluetooth_api: BluetoothSpeakerAPI):
        self._bluetooth_api = bluetooth_api

    def play_audio(self, song: Song):
        payload = f"{song.title} by {song.artist}"
        self._bluetooth_api.play_sound_via_bluetooth(payload)