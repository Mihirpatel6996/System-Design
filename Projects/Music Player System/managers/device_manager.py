from device.audio_output_device import IAudioOutputDevice
from enums.device_type import DeviceType
from factories.device_factory import DeviceFactory


class DeviceManager:
    _instance = None

    def __init__(self):
        self._current_output_device: IAudioOutputDevice | None = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DeviceManager()
        return cls._instance

    def connect(self, device_type: DeviceType):
        # Replace current device (old one will be garbage collected in Python)
        self._current_output_device = DeviceFactory.create_device(device_type)

        if device_type == DeviceType.BLUETOOTH:
            print("Bluetooth device connected")

        elif device_type == DeviceType.WIRED:
            print("Wired device connected")

        elif device_type == DeviceType.HEADPHONES:
            print("Headphones connected")

    def get_output_device(self) -> IAudioOutputDevice:
        if self._current_output_device is None:
            raise RuntimeError("No output device is connected.")
        return self._current_output_device

    def has_output_device(self) -> bool:
        return self._current_output_device is not None