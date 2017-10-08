import Live

import MIDI
from GlobalControl import GlobalControl


class MPD218:
    def __init__(self, c_instance):
        self.c_instance = c_instance
        self.callbacks = {}
        self.components = (
            GlobalControl(c_instance, self),
        )

    def disconnect(self):
        [_.disconnect() for _ in self.components]

    # called from Live to build the MIDI bindings
    def build_midi_map(self, midi_map_handle):
        script_handle = self.c_instance.handle()

        for note in self.callbacks.get(MIDI.NOTEON_STATUS, {}).keys():
            Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, MIDI.DEFAULT_CHANNEL, note)

        for note in self.callbacks.get(MIDI.NOTEOFF_STATUS, {}).keys():
            Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, MIDI.DEFAULT_CHANNEL, note)

        for cc in self.callbacks.get(MIDI.CC_STATUS, {}).keys():
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, MIDI.DEFAULT_CHANNEL, cc)

    # called from Live when MIDI messages are received
    def receive_midi(self, midi_bytes):
        channel = (midi_bytes[0] & MIDI.CHAN_MASK)
        status = (midi_bytes[0] & MIDI.STATUS_MASK)
        key = midi_bytes[1]
        callbacks = self.callbacks.get(status, {}).get(key, [])
        if status == MIDI.CC_STATUS:
            mode = MIDI.RELATIVE_TWO_COMPLEMENT
            value = MIDI.relative_two_complement_to_signed_int(midi_bytes[2])
        else:
            value = midi_bytes[2]
            mode = MIDI.ABSOLUTE

        [_(value, mode, status) for _ in callbacks]

    def register_callback(self, callback, key, mode, status):
        if not status in self.callbacks:
            self.callbacks[status] = {
                key: [callback, ]
            }
        else:
            if key in self.callbacks[status]:
                self.callbacks[status][key].append(callback)
            else:
                self.callbacks[status][key] = [callback, ]

    def update_display(self):
        pass

    def refresh_state(self):
        pass

    def can_lock_to_devices(self):
        return True

    def connect_script_instances(self, instanciated_scripts):
        pass

    def lock_to_device(self, *args):
        pass

    def unlock_from_device(self, *args):
        pass
