from pathlib import Path
from bs4 import BeautifulSoup
import sys

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

def get_types(thing, t):
	match=[]
	for key,val in thing.items():
		if key == "_type":
			continue

		if val["_type"] == t:
			match.append(key)
		if type(val) is dict:
			match.extend(get_types(val,t))
	return match

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
		title = content.title.string
		title = title.replace("\n"," ").split("—")[0] # note, not a normal dash -
		title = title.strip()

		thing_type,path = title.split(":",maxsplit=1)

		path = path.strip().split("::")

		current = ns
		for element in path:
			if element not in current:
				current[element] = {}
			current = current[element]

		current["_type"] = thing_type

	#print_thing(ns) 
	modules = get_types(ns,"Module")
	modules.sort()
	print("Modules")
	print(modules)

	classes = get_types(ns, "Class")
	classes.sort()
	print("Classes")
	print(classes)




if __name__ == "__main__":
	main()