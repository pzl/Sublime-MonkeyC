
import sublime
import sublime_plugin

import subprocess
import threading
import os

import socket # for checking simulator tcp port

from MonkeyC.helpers.manifest import Manifest
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

		self.panel = Panel(self.window)
		self.panel.print("[{}]",*args)
		self.panel.print("[{}]",str(kwargs))


		# apps compile with monkeyc, barrels(modules) with barrelbuild
		# so we need to know which we are dealing with
		self.build_for = self.detect_app_vs_barrel()
		self.simulator = Simulator(self.bin)

		self.panel.print("recompiling for device")
		self.window.run_command("monkey_build",{"device":"{}_sim".format(kwargs["device"],)})

		self.panel.print("[running simulator]")
		cmd = self.simulator.simulate(os.path.join(self.vars["folder"],"build","App.prg"), kwargs["device"])
		if "tests" in kwargs and kwargs["tests"] == True:
			pass # run in test mode
		self.panel.print(cmd)
		
		self.window.run_command("exec",{
			"shell_cmd":cmd
		})

		self.panel.cleanup()

		sublime.status_message("Build Finished") # puts text at the bottom


		#self.window.show_input_panel("caption","initial text",noop,noop,noop)
		#sublime.message_dialog("thing")
		#self.panel.show_popup_menu(["foo","bar","baz"],noop)	
		#self.panel.show_popup("hey boss", sublime.COOPERATE_WITH_AUTO_COMPLETE, -1, 800, 800, noop, noop)
		#self.window.show_quick_panel(["a","b","c"],noop)


	def detect_app_vs_barrel(self):
		""" Reads manifest.xml and detects if it is an application or barrel """
		return Manifest(self.vars['folder']).get_type()
		# could also check the .project file, or .settings/IQ_IDE.prefs


class Panel(object):
	"""wrapper for build output panel"""

	"""Alternatively, call "exec" with args like file_regex, syntax, etc"""

	def __init__(self, window):
		super(Panel, self).__init__()
		self.window = window
		self.view = self.window.create_output_panel('exec')

		panel_settings = self.view.settings()
		panel_settings.set("file_regex",r"([^:\n ]*):([0-9]+):(?:([0-9]+):)? (.*)$")
		panel_settings.set("line_numbers", False)
		panel_settings.set("gutter",False)
		panel_settings.set("scroll_past_end",False)
		#panel_settings.set("syntax","MonkeyCBuild.sublime-syntax") # alternate way
		self.view.set_syntax_file("MonkeyCBuild.sublime-syntax")

		show = sublime.load_settings("Preferences.sublime-settings").get("show_panel_on_build",True)
		#show=True # while still debugging
		if show:
			self.window.run_command("show_panel",{"panel":"output.exec"})
		self.view.set_read_only(False)

		# Default/exec.py calls create_output_panel a second time
		# after settings changes, to get picked up as result buffer?
		self.view = self.window.create_output_panel('exec')


		# panel debugging
		#self.print("Panel syntax: {}",self.view.settings().get('syntax'))
		
	def cleanup(self):
		self.view.set_read_only(True)

	def print(self, string, *args):
		if len(args):
			self.view.run_command("append",{"characters": string.format(*args)})
		else:
			self.view.run_command("append",{"characters": string})			
		self.view.run_command("append",{"characters":"\n"})


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

	def simulate(self, app, device):
		if not self.is_running():
			self.start()

		attempts=0
		while not self.is_running():
			attempts+=1
			if attempts > 40:
				sublime.message_dialog("could not connect to simulator")
				return

		cmd = "{monkeydo} {app} {device}"
		cmd = cmd.format(
			monkeydo=os.path.join(self.sdk_path,"monkeydo"),
			app=app,
			device=device
		)
		return cmd

# Random idea: sniff the TCP traffic between simulator and monkeydo.. ?