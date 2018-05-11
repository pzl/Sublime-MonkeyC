import sublime

import os
import subprocess
import time
import socket # for checking simulator tcp port

from MonkeyC.helpers.parsers import Manifest, SDK


class Simulator(object):
	"""Proxy for running CIQ apps in the simulator"""

	port=1234 # known connectiq simulator port
	#@todo: can be between 1234 - 1238

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
		subprocess.Popen(["./connectiq"],shell=True,cwd=self.sdk_path)

	def simulate(self, app, device, test=False):
		if not self.is_running():
			self.start()
			time.sleep(1)

		attempts=0
		while not self.is_running():
			attempts+=1
			time.sleep(0.3)
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
		self.do = subl_args["do"] if "do" in subl_args else "build"

		if "sdk" in subl_args:
			target_sdks = SDK(os.path.dirname(sdk_path)).targetSDKs()
			match = [x for x in target_sdks if subl_args["sdk"].replace(".x","") == ".".join(x.split(".")[:2])]
			if len(match):
				self.sdk = match[0]
			else:
				self.sdk = False
				sublime.message_dialog("unsupported SDK target: {}".format(subl_args["sdk"],))
		else:
			self.sdk = False



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