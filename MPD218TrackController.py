import Live
from MPD218Component import MPD218Component

from consts import *


class MPD218TrackController(MPD218Component):
    __module__ = __name__
    __doc__ = "Track controller for MPD218 remote control surface"
    __filter_funcs__ = ["update_display", "log"]

    def __init__(self, parent):
        MPD218Component.realinit(self, parent)

    def build_midi_map(self, script_handle, midi_map_handle):
        def forward_cc(chan, cc):
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, chan, cc)

        def forward_note(chan, note_no):
            Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, chan, note_no)

        for channel_no in TRACK_FUNCTIONS_CHANNELS:
            forward_cc(channel_no, TRACK_VOL_CC)
            for note_no in TRACK_FUNCTIONS_NOTES:
                forward_note(channel_no, note_no)

    def receive_midi_note(self, channel, status, note_no, note_vel):
        if (channel in TRACK_FUNCTIONS_CHANNELS and status == NOTEON_STATUS):
            if note_no == TRACK_TOGGLE_ARM:
                self.toggle_arm_selected_track()
            elif note_no == TRACK_TOGGLE_SOLO:
                self.toggle_solo_selected_track()
            elif note_no == TRACK_TOGGLE_MUTE:
                self.toggle_mute_selected_track()
            elif note_no == TRACK_ARM:
                self.arm_selected_track()
            elif note_no == TRACK_UNARM:
                self.unarm_selected_track()
            elif note_no == TRACK_VOL_INC:
                self.inc_volume_selected_track()
            elif note_no == TRACK_VOL_DEC:
                self.dec_volume_selected_track()

    def receive_midi_cc(self, channel, cc_no, cc_value):
        if (channel in TRACK_FUNCTIONS_CHANNELS):
            if (cc_no == TRACK_VOL_CC):
                self.set_volume_selected_track(cc_value)

    def set_volume_selected_track(self, cc_value):
        self.selected_track().mixer_device.volume.value = (self.selected_track().mixer_device.volume.max -
                                                           self.selected_track().mixer_device.volume.min) * cc_value / 127 + self.selected_track().mixer_device.volume.min

    def inc_volume_selected_track(self):
        pass

    def dec_volume_selected_track(self):
        pass

    def toggle_solo_selected_track(self):
        self.toggle_solo_track(self.selected_track())

    def toggle_solo_track(self, track):
        if track.solo:
            track.solo = 0
        else:
            track.solo = 1

    def toggle_mute_selected_track(self):
        self.toggle_mute_track(self.selected_track())

    def toggle_mute_track(self, track):
        if track.mute:
            track.mute = 0
        else:
            track.mute = 1

    def toggle_arm_selected_track(self):
        self.toggle_arm_track(self.selected_track())

    def unarm_selected_track(self):
        self.unarm_track(self.selected_track())

    def arm_selected_track(self):
        self.arm_track(self.selected_track())

    def toggle_arm_track(self, track):
        if track.arm:
            self.unarm_track(track)
        else:
            self.arm_track(track)

    def unarm_track(self, track):
        track.arm = 0

    def arm_track(self, track):
        tracks = self.song().tracks
        for t in tracks:
            if t.can_be_armed and t.arm:
                t.arm = 0
        track.arm = 1

    def disconnect(self):
        pass
