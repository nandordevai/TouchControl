import math

import MIDI
from Control import Control, ignore_cc_zero
from mappings import mappings

class GlobalControl(Control):
    def __init__(self, c_instance, selected_track_controller):
        Control.__init__(self, c_instance, selected_track_controller)
        self.show_message('Global controls initialized')
        self.track_buffer = 0
        self.scene_buffer = 0
        self.song.view.add_selected_track_listener(self.on_track_selected)

    def get_midi_bindings(self):
        return (
            ("scrub_by", self.scrub_by),
            ("midi_recording_quantization", self.midi_recording_quantization),
            ("play_pause", self.play_pause),
            ("scrub_by", self.scrub_by),
            ("stop", self.stop),
            ("overdub_on", self.toggle_overdub),
            ("overdub_off", self.toggle_overdub),
            ("metronome_on", self.toggle_metronome),
            ("metronome_off", self.toggle_metronome),
            ("undo", self.undo),
            ("redo", self.redo),
            ("session_automation_rec_on", self.toggle_session_automation_record),
            ("session_automation_rec_off", self.toggle_session_automation_record),
            ("fire_next_scene", self.fire_next_scene),

            # Session
            ("scroll_tracks", self.scroll_tracks),
            ("scroll_scenes", self.scroll_scenes),
            ("prev_track", self.select_prev_track),
            ("next_track", self.select_next_track),

            # Device
            ("macro_1", lambda value, mode, status: self.set_device_param(1, value)),
            ("macro_2", lambda value, mode, status: self.set_device_param(2, value)),
            ("macro_3", lambda value, mode, status: self.set_device_param(3, value)),
            ("macro_4", lambda value, mode, status: self.set_device_param(4, value)),
            ("macro_5", lambda value, mode, status: self.set_device_param(5, value)),
            ("macro_6", lambda value, mode, status: self.set_device_param(6, value)),
            ("macro_7", lambda value, mode, status: self.set_device_param(7, value)),
            ("macro_8", lambda value, mode, status: self.set_device_param(8, value)),
            ("select_instrument", self.select_instrument),
            ("toggle_lock", self.toggle_lock),

            # Clip
            ("delete_clip", self.delete_clip),
            ("duplicate_clip", self.duplicate_clip),

            # Track
            ("volume", self.set_volume),
            ("pan", self.set_pan),
            ("send_a", lambda value, mode, status: self.set_send(0, value)),
            ("send_b", lambda value, mode, status: self.set_send(1, value)),
            ("send_c", lambda value, mode, status: self.set_send(2, value)),
            ("send_d", lambda value, mode, status: self.set_send(3, value)),
            ("arm", self.toggle_arm),
            ("unarm", self.toggle_arm),
            ("solo", self.toggle_solo),
            ("unsolo", self.toggle_solo),
            ("mute", self.toggle_mute),
            ("unmute", self.toggle_mute),
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
    def stop(self, value, mode, status):
        self.song.stop_playing()

    @ignore_cc_zero
    def toggle_overdub(self, value, mode, status):
        self.song.overdub = not self.song.overdub

    @ignore_cc_zero
    def toggle_metronome(self, value, mode, status):
        self.song.metronome = bool(value)

    @ignore_cc_zero
    def undo(self, value, mode, status):
        self.song.undo()

    @ignore_cc_zero
    def redo(self, value, mode, status):
        self.song.redo()

    def toggle_session_automation_record(self, value, mode, status):
        self.song.session_automation_record = not self.song.session_automation_record

    def scroll_tracks(self, value, *args):
        # if the knob is turned to the other side than before, reset:
        if math.copysign(1, self.track_buffer) != math.copysign(1, value):
            self.track_buffer = 0
        self.track_buffer += value
        # if we reached the threshold, change track using the value (+/- 1) and reset
        if abs(self.track_buffer) == 5:
            self.song.view.selected_track = self.get_track_by_delta(value)
            self.track_buffer = 0

    def select_next_track(self, *args):
        self.song.view.selected_track = self.get_track_by_delta(1)

    def select_prev_track(self, *args):
        self.song.view.selected_track = self.get_track_by_delta(-1)

    def get_track_by_delta(self, delta):
        tracks = self.song.tracks + self.song.return_tracks + (self.song.master_track,)
        current_index = tracks.index(self.song.view.selected_track)
        new_index = max(0, min(current_index + delta, len(tracks) - 1))
        return tracks[new_index]

    def scroll_scenes(self, value, *args):
        if self.scene_buffer == 5:
            self.song.view.selected_scene = self.get_scene_by_delta(value)
            self.scene_buffer = 0
        else:
            self.scene_buffer += 1

    def get_scene_by_delta(self, delta):
        scene = self.song.view.selected_scene
        scenes = self.song.scenes
        current_index = list(scenes).index(scene)
        new_index = max(0, min(current_index + delta, len(scenes) - 1))
        return scenes[new_index]

    def select_instrument(self, value, mode, status):
        self.song.view.selected_track.view.select_instrument()

    def toggle_lock(self, value, mode, status):
        self.c_instance.toggle_lock()

    def delete_clip(self, value, mode, status):
        slot = self.song.view.highlighted_clip_slot
        if slot is not None and slot.has_clip:
            slot.delete_clip()

    def duplicate_clip(self, value, mode, status):
        slot = self.song.view.highlighted_clip_slot
        if slot.has_clip:
            track = self.song.view.selected_track
            next = track.duplicate_clip_slot(list(track.clip_slots).index(slot))
            self.song.view.highlighted_clip_slot = track.clip_slots[next]

    @ignore_cc_zero
    def toggle_arm(self, value, mode, status):
        self.song.view.selected_track.arm = bool(value)

    @ignore_cc_zero
    def toggle_mute(self, value, mode, status):
        self.song.view.selected_track.mute = bool(value)

    @ignore_cc_zero
    def toggle_solo(self, value, mode, status):
        self.song.view.selected_track.solo = bool(value)

    def set_volume(self, value, mode, status):
        current_value = self.song.view.selected_track.mixer_device.volume.value
        self.song.view.selected_track.mixer_device.volume.value = max(
            0.0,
            min(1.0, current_value + (value / 200.0))
        )

    def set_pan(self, value, mode, status):
        current_value = self.song.view.selected_track.mixer_device.panning.value
        self.song.view.selected_track.mixer_device.panning.value = max(
            -1.0,
            min(1.0, current_value + (value / 100.0))
        )

    def set_send(self, i, value):
        if i >= len(self.song.view.selected_track.mixer_device.sends):
            return
        param = self.song.view.selected_track.mixer_device.sends[i]
        if param:
            param.value = max(0.0, min(1.0, param.value + (value / 100.0)))

    def set_device_param(self, i, value):
        device = self.song.view.selected_track.view.selected_device
        if not device:
            return

        param = device.parameters[i]
        if not param:
            return

        param_range = param.max - param.min
        param.value = max(param.min, min(param.max, param.value + param_range * value / 127.0))

    def scrub_by(self, value, mode, status):
        self.song.scrub_by(value)

    @ignore_cc_zero
    def midi_recording_quantization(self, value, mode, status):
        q_labels = ["None", "1/4", "1/8", "1/8T", "1/8", "1/8T", "1/16", "1/16T", "1/16", "1/16T", "1/32"]
        self.song.midi_recording_quantization = self._get_quantization(value, mode, status)
        self.show_message(
            "MIDI recording quantization: %s" %
            q_labels[self.song.midi_recording_quantization]
        )

    def _get_quantization(self, value, mode, status):
        # 0: None
        # 1: 1/4
        # 2: 1/8
        # 3: 1/8T
        # 4: 1/8 + 1/8T
        # 5: 1/16
        # 6: 1/16T
        # 7: 1/16 + 1/16T
        # 8: 1/32
        next_index = range(9).index(self.song.midi_recording_quantization) + (value / abs(value))
        return min(max(0, next_index), 8)

    @ignore_cc_zero
    def fire_next_scene(self, value, mode, status):
        scene = self.get_scene_by_delta(1)
        scene.fire()
        self.song.view.selected_scene = scene

    def on_track_selected(self):
        # (note on: 144 | note off: 128, note, velocity)
        if self.song.view.selected_track.arm:
            msg = 144
            vel = 1
        else:
            msg = 128
            vel = 0
        midi_bytes = (msg, mappings["arm"].key, vel)
        self.c_instance.send_midi(midi_bytes)

        if self.song.view.selected_track.mute:
            msg = 144
            vel = 1
        else:
            msg = 128
            vel = 0
        midi_bytes = (msg, mappings["mute"].key, vel)
        self.c_instance.send_midi(midi_bytes)
        if self.song.view.selected_track.solo:
            msg = 144
            vel = 1
        else:
            msg = 128
            vel = 0
        # (note on: 144 | note off: 128, note, velocity)
        midi_bytes = (msg, mappings["solo"].key, vel)
        self.c_instance.send_midi(midi_bytes)
