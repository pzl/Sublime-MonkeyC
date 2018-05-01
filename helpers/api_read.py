from pathlib import Path
from bs4 import BeautifulSoup
import sys
import re

"""
	This is not part of the runnable plugin.
	Rather, this file parses an SDK's doc/ folder to pull out all the classes,
	methods, constants, etc. Makes it easier for diff-ing newly added methods
	between SDKs, and adding things to the syntax files.
"""

file_ignore_list = [
	"class_list.html",
	"frames.html",
	"index.html",
	"_index.html",
	"method_list.html",
	"top-level-namespace.html",
]

def print_thing(thing,indent=0):
	for key,val in thing.items():
		if key == "_type":
			continue
		print("{}{}: {}".format(indent*2*" ",key,val["_type"]))
		if type(val) is dict:
			print_thing(val,indent+1)

def _get_types(thing, t):
	match=[]
	for key,val in thing.items():
		if key == "_type":
			continue

		if val["_type"] == t:
			match.append(key)
		if type(val) is dict:
			match.extend(get_types(val,t))
	return match

def get_types(thing, t):
	types = _get_types(thing, t)
	types = list(set(types))
	types.sort()
	return types


def parse_title(html):
	title = html.title.string
	title = title.replace("\n"," ").split("—")[0] # note, not a normal dash -
	title = title.strip()
	thing_type, path = title.split(":",maxsplit=1)
	path = path.strip().split("::")
	return thing_type,path

def parse_constants(html):
	constants = html.find("dl",class_="constants")
	if constants:
		return [c["id"].replace("-constant","") for c in constants.find_all("dt")]
	else:
		return []

def instance_method(href):
	return href and href.endswith("-instance_method")
def parse_methods(html):
	methods = html.select(".summary .summary_signature > a[href$=-instance_method] > strong")
	return [m.string for m in methods]

	summary = html.find(class_="summary")
	if summary:
		sigs = summary.find_all(class_="summary_signature")
		if sigs:
			methods = sigs.find_all(href=re.compile("-instance_method$"))
			if methods:
				for m in methods:
					try:
						m.strong.string.strip()
					except AttributeError:
						print(m)
						raise
	return []


def main():
	if len(sys.argv) < 2:
		print("SDK path required as an argument")
		sys.exit(1)
	else:
		sdk = Path(sys.argv[1])

	ns = {}

	files = sdk.glob("doc/**/*.html")
	for file in files:
		if file.name in file_ignore_list:
			continue

		content = BeautifulSoup(file.read_text(), 'html.parser')

		thing_type,path = parse_title(content)
		constants = parse_constants(content)
		methods = parse_methods(content)



		current = ns
		for element in path:
			if element not in current:
				current[element] = {}
			current = current[element]

		for const in constants:
			current[const] = {"_type": "Constant"}
		for method in methods:
			current[method] = {"_type": "Method"}
		current["_type"] = thing_type

	#print_thing(ns)
	modules = get_types(ns,"Module")
	print("Modules")
	print(modules)

	classes = get_types(ns, "Class")
	print("Classes")
	print(classes)

	methods = get_types(ns, "Method")
	print("Methods")
	print(methods)

	constants = get_types(ns, "Constant")
	print("Constants")
	print(constants)



if __name__ == "__main__":
	main()