import Live

DEFAULT_CHANNEL = 0
STATUS_MASK = 0xF0
CHAN_MASK = 0x0F
CC_STATUS = 0xb0
NOTEON_STATUS = 0x90

ABSOLUTE = Live.MidiMap.MapMode.absolute  # 0 - 127
RELATIVE_TWO_COMPLEMENT = Live.MidiMap.MapMode.relative_two_compliment  # 001 - 064 / 127 - 65


def relative_two_complement_to_signed_int(value):
    if value > 64:
        return value - 128
    else:
        return value


class MIDIMessage:
    def __init__(self, key, mode=ABSOLUTE, status=NOTEON_STATUS):
        self.key = key
        self.mode = mode
        self.status = status
        self.channel = DEFAULT_CHANNEL


class Note(MIDIMessage):
    def __init__(self, note):
        MIDIMessage.__init__(self, note, status=NOTEON_STATUS)


class CC(MIDIMessage):
    def __init__(self, cc):
        MIDIMessage.__init__(self, cc, mode=RELATIVE_TWO_COMPLEMENT, status=CC_STATUS)
