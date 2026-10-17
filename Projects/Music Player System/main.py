from enums.device_type import DeviceType
from enums.play_strategy_type import PlayStrategyType

from music_player_application import MusicPlayerApplication


def main():
    try:
        application = MusicPlayerApplication.get_instance()

        # ---------------- Populate Library ----------------
        application.create_song_in_library("Kesariya", "Arijit Singh", "/music/kesariya.mp3")
        application.create_song_in_library("Chaiyya Chaiyya", "Sukhwinder Singh", "/music/chaiyya_chaiyya.mp3")
        application.create_song_in_library("Tum Hi Ho", "Arijit Singh", "/music/tum_hi_ho.mp3")
        application.create_song_in_library("Jai Ho", "A. R. Rahman", "/music/jai_ho.mp3")
        application.create_song_in_library("Zinda", "Siddharth Mahadevan", "/music/zinda.mp3")

        # ---------------- Playlist Setup ----------------
        application.create_playlist("Bollywood Vibes")
        application.add_song_to_playlist("Bollywood Vibes", "Kesariya")
        application.add_song_to_playlist("Bollywood Vibes", "Chaiyya Chaiyya")
        application.add_song_to_playlist("Bollywood Vibes", "Tum Hi Ho")
        application.add_song_to_playlist("Bollywood Vibes", "Jai Ho")

        # ---------------- Device Connection ----------------
        application.connect_audio_device(DeviceType.BLUETOOTH)

        # ---------------- Single Song Playback ----------------
        application.play_single_song("Zinda")
        application.pause_current_song("Zinda")
        application.play_single_song("Zinda")  # resume behavior

        print("\n-- Sequential Playback --\n")
        application.select_play_strategy(PlayStrategyType.SEQUENTIAL)
        application.load_playlist("Bollywood Vibes")
        application.play_all_tracks_in_playlist()

        print("\n-- Random Playback --\n")
        application.select_play_strategy(PlayStrategyType.RANDOM)
        application.load_playlist("Bollywood Vibes")
        application.play_all_tracks_in_playlist()

        print("\n-- Custom Queue Playback --\n")
        application.select_play_strategy(PlayStrategyType.CUSTOM_QUEUE)
        application.load_playlist("Bollywood Vibes")
        application.queue_song_next("Kesariya")
        application.queue_song_next("Tum Hi Ho")
        application.play_all_tracks_in_playlist()

        print("\n-- Sequential Previous Track Demo --\n")
        application.select_play_strategy(PlayStrategyType.SEQUENTIAL)
        application.load_playlist("Bollywood Vibes")
        application.play_all_tracks_in_playlist()

        application.play_previous_track_in_playlist()
        application.play_previous_track_in_playlist()

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()