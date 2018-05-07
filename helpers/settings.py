import sublime

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