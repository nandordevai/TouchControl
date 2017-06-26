import Live

import MIDI
import config

from GlobalControl import GlobalControl


class MPD218:
    __module__ = __name__
    __doc__ = "MIDI Remote Script for Akai MPD218"
    __name__ = "MPD218 MIDI Remote Script"

    def __init__(self, c_instance):
        self.c_instance = c_instance
        self.callbacks = {}
        self.components = (
            GlobalControl(c_instance, self)
        )

    def disconnect(self):
        for c in self.components:
            c.disconnect()

    def refresh_state(self):
        pass

    def update_display(self):
        pass

    def connect_script_instances(self, instanciated_scripts):
        pass

    # called from Live to build the MIDI bindings
    def build_midi_map(self, midi_map_handle):
        script_handle = self.c_instance.handle()

        for channel in range(16):
            callbacks = self.callbacks.get(channel, {})

            for note in callbacks.get(MIDI.NOTEON_STATUS, {}).keys():
                Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, channel, note)

            for cc in callbacks.get(MIDI.CC_STATUS, {}).keys():
                Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, channel, cc)

    # called from Live when MIDI messages are received
    def receive_midi(self, midi_bytes):
        channel = (midi_bytes[0] & MIDI.CHANNEL_MASK)
        status = (midi_bytes[0] & MIDI.STATUS_MASK)
        key = midi_bytes[1]
        if status == MIDI.CC_STATUS:
            mode = MIDI.RELATIVE_TWO_COMPLEMENT
            value = MIDI.relative_two_complement_to_signed_int(midi_bytes[2])
        else:
            mode = MIDI.ABSOLUTE
            value = midi_bytes[2]

        callback = self.callbacks.get(channel, {}).get(status, {}).get(key)
        if callback is not None:
            callback(value, mode, status)

    def register_callback(self, callback, message):
        """
        callbacks:
        {
            channel: {
                status: {
                    key: callback
                }
            }
        }
        """
        if not channel in self.callbacks:
            self.callbacks[message.channel] = {}

        if not status in self.callbacks[message.channel]:
            self.callbacks[message.channel][message.status] = {
                key: callback
            }
        else:
            self.callbacks[message.channel][message.status][message.key] = callback
