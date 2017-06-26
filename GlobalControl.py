import MIDI


class GlobalControl:

    def __init__(self, c_instance, mpd218):
        self.c_instance = c_instance
        if c_instance:
            self.song = c_instance.song()
        self.mpd218 = mpd218
        self.mpd218.register_callback(self.play_pause, MIDI.Note(1))

    def play_pause(self, value, mode, status):
        if self.song.is_playing:
            self.song.stop_playing()
        else:
            self.song.continue_playing()
