# https://www.noterepeat.com/articles/how-to/213-midi-basics-common-terms-explained

import Live

DEFAULT_CHANNEL = 0
STATUS_MASK = 0xF0
CHANNEL_MASK = 0x0F
CC_STATUS = 0xb0
NOTEON_STATUS = 0x90

ABSOLUTE = Live.MidiMap.MapMode.absolute
RELATIVE_TWO_COMPLEMENT = Live.MidiMap.MapMode.relative_two_complement


class MIDIMessage:
    def __init__(self, key, mode=ABSOLUTE, status=NOTEON_STATUS, channel=DEFAULT_CHANNEL):
        self.key = key
        self.mode = mode
        self.status = status
        self.channel = channel


class Note(MIDIMessage):
    def __init__(self, note, channel=DEFAULT_CHANNEL):
        MIDIMessage.__init__(self, note, ABSOLUTE, NOTEON_STATUS, channel)


class CC(MIDIMessage):
    def __init__(self, cc, mode=RELATIVE_TWO_COMPLEMENT, channel=DEFAULT_CHANNEL):
        MIDIMessage.__init__(self, cc, mode, CC_STATUS, channel)


def relative_two_complement_to_signed_int(value):
    if value > 64:
        return value - 128
    return value
