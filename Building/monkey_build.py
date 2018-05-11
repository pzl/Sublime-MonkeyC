import sublime
import sublime_plugin

import os

from MonkeyC.helpers.parsers import Manifest
from MonkeyC.helpers.run import CommandBuilder, Compiler
from MonkeyC.helpers.inputs import DeviceInput, SDKInput
from MonkeyC.helpers.settings import get_settings, has_manifest_and_jungle

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

	def is_enabled(self, *args, **kwargs):
		"""Return true if the command can be CANCELLED or RUN at a given time"""
		if 'kill' in kwargs: # build system cancel check
			return False
		# being checked otherwise, e.g. through command palette
		self.get_settings()
		return has_manifest_and_jungle(self.vars["folder"])



	def is_visible(self, *args, **kwargs):
		if 'kill' in kwargs: # build system cancel check
			return False
		# being checked otherwise, e.g. through command palette
		return True

	def input(self, kwargs):
		ask_for_device = "device" in kwargs and kwargs["device"] == "prompt"
		ask_for_sdk = "sdk" in kwargs and kwargs["sdk"] == "prompt"
		self.get_settings()

		if ask_for_device:
			self.device_select.set_sdk(self.sdk_path)
			self.device_select.set_work_dir(self.vars["folder"])

			# Only one device, so don't make a picker for it, just use it
			if len(self.device_select.list_items()) == 1:
				self.device = self.device_select.list_items()[0]
				if ask_for_sdk:
					return SDKInput(self.sdk_path, self.device)

			if ask_for_sdk:
				self.device_select.set_next(SDKInput)

			return self.device_select
		elif ask_for_sdk and "device" in kwargs and kwargs["device"]:
			return SDKInput(self.sdk_path, kwargs["device"])

		return None

	def get_settings(self):
		self.settings,self.vars = get_settings(self.window)
		self.sdk_path = self.settings.get("sdk","")
		self.bin = os.path.expanduser(os.path.join(self.sdk_path,"bin"))
		self.key = os.path.expanduser(self.settings.get("key",""))


	def run(self, *args, **kwargs):
		self.get_settings()

		sublime.status_message("Building...")
		cmd = CommandBuilder(kwargs, self.vars["folder"], self.sdk_path, self.key).build()
		Compiler(self.vars["folder"], self.window).compile(cmd)
		
		sublime.status_message("Build Finished") # puts text at the bottom

		#self.window.show_input_panel("caption","initial text",noop,noop,noop)
		#sublime.message_dialog("thing")
		#self.panel.show_popup_menu(["foo","bar","baz"],noop)	
		#self.panel.show_popup("hey boss", sublime.COOPERATE_WITH_AUTO_COMPLETE, -1, 800, 800, noop, noop)
		#self.window.show_quick_panel(["a","b","c"],noop)



