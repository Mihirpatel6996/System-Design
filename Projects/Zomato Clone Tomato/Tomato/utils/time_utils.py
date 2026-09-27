from datetime import datetime


class TimeUtils:
    @staticmethod
    def get_current_time() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")