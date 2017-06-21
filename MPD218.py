import Live
from consts import *
import sys
from MPD218MainController import MPD218MainController
from MPD218TrackController import MPD218TrackController
from MPD218ClipController import MPD218ClipController

"""
based on http://motscousus.com/stuff/2007-09_AKAI_MPD16_Ableton_Live_Scripts/

"""

class MPD218:
	__filter_funcs__ = ["update_display", "exec_commands", "log", "song"]
	__module__ = __name__
	__doc__ = 'Automap script for MPD218 controllers'
	__myDebug__ = False

	def __init__(self, c_instance):
		MPD218.realinit(self, c_instance)

	def realinit(self, c_instance):
		if self.__myDebug__:
			if sys.platform == "win32":
                # FIXME: create proper tempfile
				self.file = open("C:/MPD218.txt", "a")
				self.commandfile = "C:/MPD218-cmd.txt"
			else:
				self.file = open("/tmp/MPD218", "a")
				self.commandfile = "/tmp/MPD218-cmd"
			self.log("MPD218")

		self.c_instance = c_instance
		self.main_controller  = MPD218MainController(self)
		self.track_controller = MPD218TrackController(self)
		self.clip_controller  = MPD218ClipController(self)
		self.components = [self.main_controller,  self.track_controller, self.clip_controller]

		self.request_rebuild_midi_map()

	def exec_commands(self):
		if not self.__myDebug__:
			return
		filename = self.commandfile
		file = open(filename, "r")
		commands = file.readlines()
		for command in commands:
			command = command.strip()
			try:
				self.log("%s = %s" % (command, eval(command)))
			except Exception, inst:
				self.log("exception: %s" % inst)
			try:
				self.log("execing %s" % command)
			except Exception, inst:
				self.log("Exception while executing %s: %s" % (command, inst))
		file.close()
        # why?
		file = open(filename, "w")
		file.write("")
		file.close()

	def log(self, string):
		if self.__myDebug__:
			self.file.write(string + "\n")
			self.file.flush()

	def disconnect(self):
		for c in self.components:
			c.disconnect()

	def application(self):
		return Live.Application.get_application()

	def song(self):
		return self.c_instance.song()

	def suggest_input_port(self):
		return str('')

	def suggest_output_port(self):
		return str('')

	def can_lock_to_devices(self):
		return False

	def lock_to_device(self, device):
		pass

	def unlock_to_device(self, device):
		pass

	def set_appointed_device(self, device):
		pass

	def toggle_lock(self):
		self.c_instance.toggle_lock()

	def suggest_map_mode(self, cc_no):
		return Live.MidiMap.MapMode.absolute

	def restore_bank(self, bank):
		pass

	def show_message(self, message):
		self.c_instance.show_message(message)

	def instance_identifier(self):
		return self.c_instance.instance_identifier()

	def connect_script_instances(self, instanciated_scripts):
		pass

	def request_rebuild_midi_map(self):
		self.c_instance.request_rebuild_midi_map()

	def send_midi(self, midi_event_bytes):
		self.c_instance.send_midi(midi_event_bytes)

	def refresh_state(self):
		for c in self.components:
			c.refresh_state()

	def build_midi_map(self, midi_map_handle):
		script_handle = self.c_instance.handle()
		for c in self.components:
			c.build_midi_map(script_handle, midi_map_handle)

	def update_display(self):
		self.exec_commands()
		for c in self.components:
			c.update_display()

	def receive_midi(self, midi_bytes):
		channel = (midi_bytes[0] & CHAN_MASK)
		status = (midi_bytes[0] & STATUS_MASK)
		if (status == CC_STATUS):
			cc_no = midi_bytes[1]
			cc_value = midi_bytes[2]
			for c in self.components:
				c.receive_midi_cc(channel, cc_no, cc_value)
		elif (status == NOTEON_STATUS) or (status == NOTEOFF_STATUS):
			note_no = midi_bytes[1]
			note_vel = midi_bytes[2]
			for c in self.components:
				c.receive_midi_note(channel, status, note_no, note_vel)
		else:
			assert False, ('Unknown MIDI message %s' % str(midi_bytes))

	def on_tracks_changed(self):
		self.log("tracks changed")
