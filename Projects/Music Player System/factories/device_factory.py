from enums.device_type import DeviceType

from device.bluetooth_speaker_adapter import BluetoothSpeakerAdapter
from device.wired_speaker_adapter import WiredSpeakerAdapter
from device.headphones_adapter import HeadphonesAdapter

from external.bluetooth_speaker_api import BluetoothSpeakerAPI
from external.wired_speaker_api import WiredSpeakerAPI
from external.headphones_api import HeadphonesAPI

from device.audio_output_device import IAudioOutputDevice


class DeviceFactory:

    @staticmethod
    def create_device(device_type: DeviceType) -> IAudioOutputDevice:

        if device_type == DeviceType.BLUETOOTH:
            return BluetoothSpeakerAdapter(BluetoothSpeakerAPI())

        elif device_type == DeviceType.WIRED:
            return WiredSpeakerAdapter(WiredSpeakerAPI())

        elif device_type == DeviceType.HEADPHONES:
            return HeadphonesAdapter(HeadphonesAPI())

        else:
            raise ValueError(f"Unsupported device type: {device_type}")