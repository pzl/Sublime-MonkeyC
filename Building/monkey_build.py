import sublime
import sublime_plugin

import subprocess
import threading
import os

from MonkeyC.helpers.parsers import Manifest
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





class CommandBuilder(object):
	"""Constructs the compiler command"""
	def __init__(self, subl_args, curdir, sdk_path, private_key):
		super(CommandBuilder, self).__init__()
		self.curdir = curdir
		self.sdk_path = sdk_path
		self.private_key = private_key
		self.args = subl_args

		self.flags = subl_args["flags"] if "flags" in subl_args else []
		self.device = subl_args["device"] if "device" in subl_args and subl_args["device"] != "prompt" else False
		self.sdk = subl_args["sdk"].replace(".x",".0") if "sdk" in subl_args else False #todo: sdk string may be 1.4.x, need to match SDKTargets where x = .*
		self.do = subl_args["do"] if "do" in subl_args else "build"



	def build(self):
		# apps compile with monkeyc, barrels(modules) with barrelbuild
		# so we need to know which we are dealing with
		self.build_for = self.detect_app_vs_barrel()
		
		compiler_args = {
			"flags": self.flags,
			"name": self.output_name(self.args),
			"device": self.device
		}
		if self.sdk:
			compiler_args["flags"].append("-s {}".format(self.sdk,))

		if self.build_for == "application":
			if self.do == "release":
				compiler_args["flags"].extend(["-r","-e"])
				if not "name" in self.args:
					compiler_args["name"] = "App.iq"
			elif self.do == "test":
				compiler_args["flags"].append("-t")
			cmd = self.combine("monkeyc",**compiler_args)
		else:
			if self.do == "test":
				cmd = self.combine("barreltest", **compiler_args)
			else:
				cmd = self.combine("barrelbuild", **compiler_args)

		return cmd

	def combine(self, program, name="App.prg", device=None, flags=None):
		cmd = "{program} -w -o {output} -f {jungle} {key} {device} {flags}"
		cmd = cmd.format(
			program=os.path.join(self.sdk_path,program),
			output=os.path.join(self.curdir,"bin",name),
			jungle=os.path.join(self.curdir,"monkey.jungle"),
			key="-y {}".format(self.private_key,) if program in ["monkeyc","barreltest"] else "",
			device="-d {}".format(device,) if device else "",
			flags=" ".join(flags) if flags else ""
		)
		return cmd

	def output_name(self, subl_args):
		if "name" in subl_args:
			return subl_args["name"]
		elif self.build_for == "application" or "do" in subl_args and subl_args["do"] == "test":
			return "App.prg"
		else:
			return "App.barrel"


	def detect_app_vs_barrel(self):
		""" Reads manifest.xml and detects if it is an application or barrel """
		return Manifest(self.curdir).get_type()
		# could also check the .project file, or .settings/IQ_IDE.prefs


class Compiler(object):
	"""Generic wrapper class for compiling a monkeyc project"""

	def __init__(self, cwd, window=False):
		super(Compiler, self).__init__()
		self.cwd = cwd
		self.window = window
	
	# basically just run `cmd`.
	# if window was provided to constructor
	# run this through sublime's exec command (e.g. normal build)
	def compile(self, cmd):
		if self.window:
			self.window.run_command("exec", {
				"shell_cmd": cmd,
				"file_regex":r"([^:\n ]*):([0-9]+):(?:([0-9]+):)? (.*)$",
				# official: ([a-zA-Z]:)?((\\\\|/)[a-zA-Z0-9._-]+)+(\\\\|/)?:[0-9]+
				"syntax": "MonkeyCBuild.sublime-syntax"
			})
		else:
			return subprocess.Popen(cmd,shell=True,cwd=self.cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		""" @TODO: exit code message parsing with SDK/bin/compilerInfo.xml -> exitCodes """