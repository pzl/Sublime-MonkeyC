import sublime
import sublime_plugin

import os
import uuid
from MonkeyC.helpers.manifest import Manifest

class MonkeyGenerateCommand(sublime_plugin.WindowCommand):
	"""Automating creating some simple things, uuids and private keys"""

	def get_settings(self):
		self.vars = self.window.extract_variables()

	def run(self, *args, **kwargs):
		self.get_settings()
		getattr(self, kwargs["gen"])(**kwargs)

	def key(self, *args, **kwargs):
		self.window.run_command("exec",{
			"shell_cmd": "openssl genrsa 4096 | openssl pkcs8 -topk8 -inform PEM -outform DER -out ~/tmp/ciq_new_key -nocrypt"
		})
		self.settings.set("key","~/tmp/ciq_new_key")
		sublime.status_message("Key generated")

	def uuid(self, *args, **kwargs):
		app_id = uuid.uuid4().hex
		manifest = Manifest(self.vars["folder"])
		manifest.set_id(app_id)