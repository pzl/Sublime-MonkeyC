import sublime
import sublime_plugin

import os
import uuid
from MonkeyC.helpers.parsers import Manifest
from MonkeyC.helpers.settings import get_settings

class MonkeyGenerateCommand(sublime_plugin.WindowCommand):
	"""Automating creating some simple things, uuids and private keys"""

	def run(self, *args, **kwargs):
		self.settings,self.vars = get_settings(self.window)
		getattr(self, kwargs["gen"])(**kwargs)

	def key(self, *args, **kwargs):
		self.window.run_command("exec",{
			"shell_cmd": "openssl genrsa 4096 | openssl pkcs8 -topk8 -inform PEM -outform DER -out ciq_key.der -nocrypt",
			"working_dir": self.vars["folder"]
		})
		settings = sublime.load_settings("MonkeyCBuild.sublime-settings")
		settings.set("sdk",settings.get("sdk","")) # make sure the key continues to exist
		settings.set("key",os.path.join(self.vars["folder"],"ciq_key.der"))
		sublime.save_settings("MonkeyCBuild.sublime-settings")
		sublime.status_message("Key generated")

	def uuid(self, *args, **kwargs):
		app_id = uuid.uuid4().hex
		manifest = Manifest(self.vars["folder"])
		manifest.set_id(app_id)
		sublime.status_message("App ID updated")
