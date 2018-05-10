import sublime
import sublime_plugin

import os

from MonkeyC.helpers.parsers import Manifest
from MonkeyC.helpers.run import Simulator, CommandBuilder, Compiler
from MonkeyC.helpers.inputs import DeviceInput
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
		self.get_settings()
		try:
			is_app = Manifest(self.vars['folder']).get_type() == "application"
		except FileNotFoundError:
			return False
		else:
			# barrels cannot be directly simulated. Only applications
			return is_app

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
		compile_cmd = CommandBuilder(build_args, self.vars["folder"], self.bin, self.key).build()
		
		print("about to run {}".format(compile_cmd,))

		proc = Compiler(self.vars["folder"]).compile(compile_cmd)
		ret = proc.wait()
		if ret != 0:
			stdout,stderr = proc.communicate()
			if stdout:
				print(stdout.decode("utf8"))
			if stderr:
				print(stderr.decode("utf8"))
			return

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


