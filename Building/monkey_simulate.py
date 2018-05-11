import sublime
import sublime_plugin

import os

from MonkeyC.helpers.parsers import Manifest
from MonkeyC.helpers.run import Simulator, CommandBuilder, Compiler
from MonkeyC.helpers.inputs import DeviceInput
from MonkeyC.helpers.settings import get_settings, has_manifest_and_jungle

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

		has_files = has_manifest_and_jungle(self.vars["folder"])
		if not has_files:
			return False

		is_app = Manifest(self.vars['folder']).get_type() == "application"
		return is_app # barrels cannot be directly simulated. Only applications

	def is_visible(self, *args, **kwargs):
		if 'kill' in kwargs: # build system cancel check
			return False
		# being checked otherwise, e.g. through command palette
		return True

	def input(self, *args, **kwargs):
		self.get_settings()
		self.device_select.set_sdk(self.sdk_path)
		self.device_select.set_work_dir(self.vars["folder"])

		if len(self.device_select.list_items()) == 1:
			# skip selection when there's only one supported device
			self.device = self.device_select.list_items()[1]
			return None

		return self.device_select

	def get_settings(self):
		self.settings,self.vars = get_settings(self.window)
		self.sdk_path = self.settings.get("sdk","")
		self.bin = os.path.expanduser(os.path.join(self.sdk_path,"bin"))
		self.key = os.path.expanduser(self.settings.get("key",""))

	def run(self, *args, **kwargs):
		sublime.status_message("Starting...")

		self.get_settings()
		self.simulator = Simulator(self.bin)
		run_tests = "tests" in kwargs and kwargs["tests"] == True

		build_args = {
			"device": "{name}{sim}".format(name=kwargs["device"],sim="_sim" if run_tests else ""),
			"do": "test" if run_tests else "build"
		}
		compile_cmd = CommandBuilder(build_args, self.vars["folder"], self.bin, self.key).build()


		sublime.set_timeout_async(lambda: self.compile_and_sim(compile_cmd, kwargs["device"], run_tests))




		#self.window.show_input_panel("caption","initial text",noop,noop,noop)
		#sublime.message_dialog("thing")
		#self.panel.show_popup_menu(["foo","bar","baz"],noop)	
		#self.panel.show_popup("hey boss", sublime.COOPERATE_WITH_AUTO_COMPLETE, -1, 800, 800, noop, noop)
		#self.window.show_quick_panel(["a","b","c"],noop)


	def compile_and_sim(self, cmd, device, tests):
		sublime.status_message("Compiling for simulator")
		proc = Compiler(self.vars["folder"]).compile(cmd)
		ret = proc.wait()
		if ret != 0:
			stdout,stderr = proc.communicate()
			if stdout:
				print(stdout.decode("utf8"))
			if stderr:
				print(stderr.decode("utf8"))
			sublime.message_dialog("Compilation failed")
			return

		sublime.status_message("Simulating...")
		cmd = self.simulator.simulate(os.path.join(self.vars["folder"],"bin","App.prg"), device, test=tests)
		
		self.window.run_command("exec",{
			"shell_cmd":cmd,
			"syntax":"MonkeyDoTests.sublime-syntax"
		})

		sublime.status_message("Simulation Launched")