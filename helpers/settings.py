import sublime
from os.path import expanduser, join, exists


def get_settings(window=False):

	plugin_settings = sublime.load_settings("MonkeyCBuild.sublime-settings")

	settings = {
		"sdk": plugin_settings.get("sdk",""),
		"key": plugin_settings.get("key","")
	}

	window_vars = {}
	if window:
		window_vars = window.extract_variables() # get project path, folder, etc

		# config from .sublime-project. Check for "monkeyc" key.
		project_settings = (window.project_data() or {}).get("monkeyc",{})
		settings.update(project_settings) # override plugin settings with project-specific

	return settings,window_vars


#@todo: read manifest.xml path/name from monkey.jungle. Could be named something else.
#@todo: monkey.jungle is also an assumptive file name
def has_manifest_and_jungle(project_dir):
	"""Verify that both files exist at the project root"""
	curdir = expanduser(project_dir)
	return exists(join(curdir,"manifest.xml")) and exists(join(curdir,"monkey.jungle"))
