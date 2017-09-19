import MIDI
from mappings import mappings


# ignore 0 values from CC pads
def ignore_cc_zero(func):
    def func_wrapper(*args):
        if not (args[3] == MIDI.CC_STATUS and not args[1]):
            func(args)

    return func_wrapper


class Control:
    def __init__(self, c_instance, selected_track_controller):
        self.c_instance = c_instance
        if c_instance:
            self.song = c_instance.song()
        self.selected_track_controller = selected_track_controller

        for key, callback in self.get_midi_bindings():
            if not key in mappings:
                continue

            mapping = mappings[key]
            # always make sure mapping is a tuple
            if isinstance(mapping, MIDI.MIDIMessage):
                mapping = (mapping,)

            for m in mapping:
                self.selected_track_controller.register_callback(callback, m.key, m.mode, m.status)

    def disconnect(self):
        pass

    def get_midi_bindings(self):
        return set()

    def show_message(self, msg):
        """ display msg in Live's status bar """
        assert isinstance(msg, (str, unicode))
        self.c_instance.show_message(msg)
