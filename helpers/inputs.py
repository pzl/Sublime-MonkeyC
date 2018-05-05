import sublime
import sublime_plugin

from MonkeyC.helpers.manifest import Manifest
from MonkeyC.helpers.sdk import SDK

class SDKInput(sublime_plugin.ListInputHandler):

	def __init__(self, sdk_path, device):
		super(sublime_plugin.ListInputHandler, self).__init__()
		self.sdk_path= sdk_path
		self.selected_device = device

	def description(self, value, text):
		return text

	def name(self):
		"""argument keyname sent to command"""
		return "sdk"

	def placeholder(self):
		""" appears in command palette"""
		return "SDK Target"

	def confirm(self, value):
		pass

	def preview(self,item):
		""" appears at bottom of list, happens onChange """
		return sublime.Html("<b>"+item+"</b>")

	def list_items(self):
		# supported CIQ versions for device
		ciqs = SDK(self.sdk_path).getDevice(self.selected_device).ciq_versions
		# turn 1.3.2 into 1.3.x and remove duplicates with 'set'
		ciqs = list(set([".".join(c.split(".")[:2])+".x" for c in ciqs]))
		return ciqs

class DeviceInput(sublime_plugin.ListInputHandler):
	def __init__(self, sdk_path=None, path=None):
		super(sublime_plugin.ListInputHandler, self).__init__()
		self.device = ""
		self.next = None
		if sdk_path:
			self.sdk_path = sdk_path
		if path:
			self.path = path

	def set_sdk(self, path):
		self.sdk_path = path
	def set_work_dir(self, path):
		self.path = path
	def set_next(self, cls):
		self.next = cls

	def description(self, value, text):
		""" when stacking inputs, this is shown as the "selected" text"""
		return text

	def name(self):
		"""argument keyname sent to command"""
		return "device"

	def initial_text(self):
		""" pre-populate response """
		return self.device

	def placeholder(self):
		""" appears in command palette"""
		return "Garmin Device"

	def confirm(self, value):
		self.device = value

	def preview(self,item):
		""" appears at bottom of list, happens onChange """
		device = SDK(self.sdk_path).getDevice(item)
		return sublime.Html("<b>{}</b>: {}".format(device.name,device.id))

	def list_items(self):
		""" values to choose from """
		return Manifest(self.path).devices()

	def next_input(self, args):
		if self.next:
			return self.next(self.sdk_path, self.device)
		return None
