import sublime
import sublime_plugin

import subprocess
import threading
import os

from MonkeyC.helpers.manifest import Manifest
from MonkeyC.helpers.inputs import DeviceInput, SDKInput

noop = lambda *x, **y: None

"""
	TODO:
		- SDK Path management
		- change output panel syntax based on used command
		- ability to include extra jungle files (for apps and barrels)
		- build using non-jungle style (-w -z resources, etc)
		- build for device
			- device
			- release ver y/n
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
		self.settings = sublime.load_settings("MonkeyCBuild.sublime-settings")
		# @todo: override with project settings

		self.sdk_path = self.settings.get("sdk","")
		self.bin = os.path.expanduser(os.path.join(self.sdk_path,"bin"))
		self.key = os.path.expanduser(self.settings.get("key",""))

		project_data = self.window.project_data() # JSON from sublime project
		project_settings = (project_data or {}).get("monkeyc",{}) # {} should override setting with these

		view_settings = self.window.active_view().settings()
		self.vars = self.window.extract_variables()
		"""
		{
			'project': '/home/dan/dev/sub-projects/monkeyc.sublime-project',
			'project_extension': 'sublime-project',
			'file': '/home/dan/dev/Sublime-MonkeyC/monkey_build.py',
			'file_path': '/home/dan/dev/Sublime-MonkeyC',
			'platform': 'Linux',
			'folder': '/home/dan/dev/Sublime-MonkeyC',
			'packages': '/home/dan/.config/sublime-text-3/Packages',
			'file_name': 'monkey_build.py',
			'file_base_name': 'monkey_build',
			'project_name': 'monkeyc.sublime-project',
			'file_extension': 'py',
			'project_base_name': 'monkeyc',
			'project_path': '/home/dan/dev/sub-projects'
		}
		"""



	def run(self, *args, **kwargs):

		sublime.status_message("Building...")

		self.get_settings()

		#self.panel = Panel(self.window)
		#self.panel.print("[{}]",*args)
		#self.panel.print("[{}]",str(kwargs))


		# apps compile with monkeyc, barrels(modules) with barrelbuild
		# so we need to know which we are dealing with
		self.build_for = self.detect_app_vs_barrel()
		self.compiler = Compiler(self.bin,self.vars["folder"],self.key)


		compiler_args = {
			"flags": kwargs["flags"] if "flags" in kwargs else [],
			"name": kwargs["name"] if "name" in kwargs else "App.prg",
			"device": kwargs["device"] if "device" in kwargs and kwargs["device"] != "prompt" else False
		}
		if "sdk" in kwargs:
			compiler_args["flags"].append("-s {}".format(kwargs["sdk"].replace(".x",".0"),))
			#todo: sdk string may be 1.4.x, need to match SDKTargets where x = .*

		if self.build_for == "application":
			if "do" in kwargs and kwargs["do"] == "release":
				compiler_args["flags"].extend(["-r","-e"])
				if not "name" in kwargs:
					compiler_args["name"] = "App.iq"
			elif "do" in kwargs and kwargs["do"] == "test":
				compiler_args["flags"].append("-t")
			cmd = self.compiler.compile("monkeyc",**compiler_args)
		else:
			if "do" in kwargs and kwargs["do"] == "test":
				device = kwargs["device"] if "device" in kwargs else "fenix5"
				cmd = self.compiler.compile("barreltest", device=device)
			else:
				cmd = self.compiler.compile("barrelbuild")

		#self.panel.print(cmd)
		self.window.run_command("exec",{
			"shell_cmd": cmd,
			"file_regex":r"([^:\n ]*):([0-9]+):(?:([0-9]+):)? (.*)$",
			"syntax": "MonkeyCBuild.sublime-syntax"
		})


		if "tests" in kwargs and kwargs["tests"] == True:
			self.window.run_command("monkey_simulate",{ "tests":True })


		#self.panel.cleanup()

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

class Compiler(object):
	"""Generic wrapper class for compiling a monkeyc project"""


	""" @TODO: exit code message parsing with SDK/bin/compilerInfo.xml -> exitCodes """
	def __init__(self, sdk_path, project_path, key):
		super(Compiler, self).__init__()
		self.sdk_path = sdk_path
		self.project_path = project_path
		self.key=key
		
	def compile(self, compiler, name="App.prg", device=None, flags=None):
		cmd = "{compiler} -w -o {output} -f {jungle} {key} {device} {flags}"
		cmd = cmd.format(
			compiler=os.path.join(self.sdk_path,compiler),
			output=os.path.join(self.project_path,"build",name),
			jungle=os.path.join(self.project_path,"monkey.jungle"),
			key="-y {}".format(self.key,) if compiler in ["monkeyc","barreltest"] else "",
			device="-d {}".format(device,) if device else "",
			flags=" ".join(flags) if flags else ""
		)
		return cmd
