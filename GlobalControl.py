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
            ("stop", self.stop),
            ("overdub", self.toggle_overdub),
            ("metronome", self.toggle_metronome),
            ("undo", self.undo),
            ("redo", self.redo),
            ("session_automation_rec", self.toggle_session_automation_record),

            # Session
            ("prev_track", lambda value, mode, status: self.scroll_tracks(-1)),
            ("next_track", lambda value, mode, status: self.scroll_tracks(1)),

            # Device
            ("select_instrument", self.select_instrument),
            ("toggle_lock", self.toggle_lock),

            # Clip
            ("delete_clip", self.delete_clip),
            ("duplicate_clip", self.duplicate_clip),

            # Track
            ("arm", self.toggle_arm),
            ("solo", self.toggle_solo),
            ("mute", self.toggle_mute),
        )

    def scrub_by(self, value, mode, status):
        self.song.scrub_by(value)

    @ignore_cc_zero
    def play_pause(self, value, mode, status):
        if self.song.is_playing:
            self.song.stop_playing()
        else:
            self.song.continue_playing()

    @ignore_cc_zero
    def stop_playing(self, value, mode, status):
        self.song.stop_playing()

    @ignore_cc_zero
    def toggle_overdub(self, value, mode, status):
        self.song.overdub = not self.song.overdub

    @ignore_cc_zero
    def toggle_metronome(self, value, mode, status):
        self.song.metronome = not self.song.metronome

    @ignore_cc_zero
    def undo(self, value, mode, status):
        self.song.undo()

    @ignore_cc_zero
    def redo(self, value, mode, status):
        self.song.redo()

    def toggle_session_automation_record(self, value, mode, status):
        self.song.session_automation_record = not self.song.session_automation_record

    def scroll_tracks(self, value):
        self.song.view.selected_track = self.get_track_by_delta(value)

    def get_track_by_delta(self, delta):
        tracks = self.song.tracks + self.song.return_tracks + [self.song.master_track]
        current_index = tracks.index(self.song.view.selected_track)
        new_index = max(0, min(current_index + delta, len(tracks) - 1))
        return tracks[new_index]

    def select_instrument(self, value, mode, status):
        self.song.view.selected_track.view.select_instrument()

    def toggle_lock(self, value, mode, status):
        self.c_instance.toggle_lock()

    def delete_clip(self, value, mode, status):
        slot = self.song.view.highlighted_clip_slot
        if slot is not None and slot.has_clip:
            slot.delete_clip()

    def duplicate_clip_slot(self, value, mode, status):
        slot = self.song.view.highlighted_clip_slot
        if slot.has_clip:
            track = self.song.view.selected_track
            index = track.clip_slots.index(slot)
            next = track.duplicate_clip_slot(index)
            self.song.view.highlighted_clip_slot = track.clip_slots[next]

    @ignore_cc_zero
    def toggle_arm(self, value, mode, status):
        self.song.view.selected_track.arm = not self.song.view.selected_track.arm

    @ignore_cc_zero
    def toggle_mute(self, value, mode, status):
        self.song.view.selected_track.mute = not self.song.view.selected_track.mute

    @ignore_cc_zero
    def toggle_solo(self, value, mode, status):
        self.song.view.selected_track.solo = not self.song.view.selected_track.solo
