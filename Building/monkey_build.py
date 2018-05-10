import sublime
import sublime_plugin

import os

from MonkeyC.helpers.parsers import Manifest
from MonkeyC.helpers.run import CommandBuilder, Compiler
from MonkeyC.helpers.inputs import DeviceInput, SDKInput
from MonkeyC.helpers.settings import get_settings

noop = lambda *x, **y: None

"""
	TODO:
		- ability to include extra jungle files (for apps and barrels)
		- build using non-jungle style (-w -z resources, etc)
		- "IDE management"
			- project scaffolding/setup
				- see: SDK/bin/projectInfo.xml and templates/
			- manifest.xml management?
				- permissions
				- supported devices
				- min SDK ver
				- see: SDK/bin/projectInfo.xml
			- monkey.jungle setup?
"""


class MonkeyBuildCommand(sublime_plugin.WindowCommand):
	"""Builds ConnectIQ-based projects in sublime text"""

	def __init__(self, window):
		# for some reason this did NOT like the normal way
		sublime_plugin.WindowCommand.__init__(self,window)
		self.device_select = DeviceInput()

	"""
	encoding="utf-8"
	killed=False
	proc=None
	panel=None
	panel_lock=threading.Lock()
	"""

	def is_enabled(self, *args, **kwargs):
		"""Return true if the command can be CANCELLED or RUN at a given time"""
		if 'kill' in kwargs: # build system cancel check
			return False
		# being checked otherwise, e.g. through command palette
		if 'enabled' in kwargs:
			return kwargs['enabled']
		return True

	def is_visible(self, *args, **kwargs):
		if 'kill' in kwargs: # build system cancel check
			return False
		# being checked otherwise, e.g. through command palette
		return True

	def description(self, *args, **kwargs):
		"""Shown as caption in menu items when caption isn't present"""
		return "something something"

	def input(self, kwargs):
		if "device" in kwargs and kwargs["device"] == "prompt":
			# @todo: skip inputs if there is only one choice
			# e.g. only one supported device
			self.get_settings()
			self.device_select.set_sdk(self.sdk_path)
			self.device_select.set_work_dir(self.vars["folder"])

			if "sdk" in kwargs and kwargs["sdk"] == "prompt":
				self.device_select.set_next(SDKInput)

			return self.device_select

		return None

	def get_settings(self):
		self.settings,self.vars = get_settings(self.window)
		self.sdk_path = self.settings.get("sdk","")
		self.bin = os.path.expanduser(os.path.join(self.sdk_path,"bin"))
		self.key = os.path.expanduser(self.settings.get("key",""))


	def run(self, *args, **kwargs):
		self.get_settings()

		sublime.status_message("Building...")
		cmd = CommandBuilder(kwargs, self.vars["folder"], self.bin, self.key).build()
		self.compiler = Compiler(self.vars["folder"], self.window).compile(cmd)
		sublime.status_message("Build Finished") # puts text at the bottom

		#self.window.show_input_panel("caption","initial text",noop,noop,noop)
		#sublime.message_dialog("thing")
		#self.panel.show_popup_menu(["foo","bar","baz"],noop)	
		#self.panel.show_popup("hey boss", sublime.COOPERATE_WITH_AUTO_COMPLETE, -1, 800, 800, noop, noop)
		#self.window.show_quick_panel(["a","b","c"],noop)



