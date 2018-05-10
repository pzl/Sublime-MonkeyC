
import sublime
import sublime_plugin

import subprocess
import threading
import os

import socket # for checking simulator tcp port

from MonkeyC.helpers.parsers import Manifest
from MonkeyC.helpers.inputs import DeviceInput, SDKInput
from MonkeyC.helpers.settings import get_settings

noop = lambda *x, **y: None



class MonkeySimulateCommand(sublime_plugin.WindowCommand):
	"""Runs ConnectIQ Simulator"""

	def __init__(self, window):
		# for some reason this did NOT like the normal way
		sublime_plugin.WindowCommand.__init__(self,window)
		self.device_select = DeviceInput()

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

	def input(self, *args, **kwargs):
		# @todo: skip inputs if there is only one choice
		# e.g. only one supported device
		self.get_settings()
		self.device_select.set_sdk(self.sdk_path)
		self.device_select.set_work_dir(self.vars["folder"])
		return self.device_select

	def get_settings(self):
		self.settings,self.vars = get_settings(self.window)
		self.sdk_path = self.settings.get("sdk","")
		self.bin = os.path.expanduser(os.path.join(self.sdk_path,"bin"))
		self.key = os.path.expanduser(self.settings.get("key",""))

	def run(self, *args, **kwargs):
		sublime.status_message("Running Simulator")

		self.get_settings()

		self.simulator = Simulator(self.bin)

		run_tests = "tests" in kwargs and kwargs["tests"] == True

		build_args = {
			"device": "{name}{sim}".format(name=kwargs["device"],sim="_sim" if run_tests else ""),
			"do": "test" if run_tests else "build"
		}
		self.window.run_command("monkey_build",build_args)

		cmd = self.simulator.simulate(os.path.join(self.vars["folder"],"bin","App.prg"), kwargs["device"], test=run_tests)
		
		self.window.run_command("exec",{
			"shell_cmd":cmd,
			"syntax":"MonkeyDoTests.sublime-syntax"
		})

		sublime.status_message("Simulation Finished")


		#self.window.show_input_panel("caption","initial text",noop,noop,noop)
		#sublime.message_dialog("thing")
		#self.panel.show_popup_menu(["foo","bar","baz"],noop)	
		#self.panel.show_popup("hey boss", sublime.COOPERATE_WITH_AUTO_COMPLETE, -1, 800, 800, noop, noop)
		#self.window.show_quick_panel(["a","b","c"],noop)


class Simulator(object):
	"""Proxy for running CIQ apps in the simulator"""

	port=1234 # known connectiq simulator port

	def __init__(self, sdk_path):
		super(Simulator, self).__init__()
		self.sdk_path = sdk_path

	@classmethod
	def is_running(cls):
		""" Checks port 1234 to see if the simulator is running """
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			try:
				sock.bind(("0.0.0.0",cls.port))
			except OSError:
				return True
			else:
				return False

	def start(self):
		pass
		# run `connectiq` from the sdk_path
		# in another thread

	def simulate(self, app, device, test=False):
		if not self.is_running():
			self.start()

		attempts=0
		while not self.is_running():
			attempts+=1
			if attempts > 40:
				sublime.message_dialog("could not connect to simulator")
				return

		cmd = "{monkeydo} {app} {device} {test}"
		cmd = cmd.format(
			monkeydo=os.path.join(self.sdk_path,"monkeydo"),
			app=app,
			device=device,
			test="-t" if test else ""
		)
		return cmd

# Random idea: sniff the TCP traffic between simulator and monkeydo.. ?