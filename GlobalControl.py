import MIDI
from Control import Control


class GlobalControl(Control):
    def __init__(self, c_instance, selected_track_controller):
        Control.__init__(self, c_instance, selected_track_controller)
        self.show_message('Global controls initialized')

    def get_midi_bindings(self):
        return (
            ("play_pause", self.play_pause),
            ("scrub_by", self.scrub_by),
        )

    def scrub_by(self, value, mode, status):
        self.song.scrub_by(value)

    def play_pause(self, value, mode, status):
        if status == MIDI.CC_STATUS and not value:  # ignore 0 values from CC-pads
            return
        if self.song.is_playing:
            self.song.stop_playing()
        else:
            self.song.continue_playing()
