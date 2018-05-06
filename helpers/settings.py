import sublime

def get_settings(window=False):

	settings = sublime.load_settings("MonkeyCBuild.sublime-settings")
	#@todo: override ^ with project settings

	window_vars = {}
	if window:
		window_vars = window.extract_variables()
		""" Looks like:
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

		project_data = window.project_data() # JSON from .sublime-project
		project_settings = (project_data or {}).get("monkeyc",{}) # should override setting with these

		view_settings = window.active_view().settings() # ???

	return settings,window_vars