import xml.etree.ElementTree as ET
import os


def tag(element):
	return element.tag.split("}")[1]

class Manifest(object):
	"""Helper class for reading and modifying a manifest.xml file"""

	ns = { "iq": "http://www.garmin.com/xml/connectiq" }

	def __init__(self, folder):
		super(Manifest, self).__init__()
		ET.register_namespace("iq",self.ns["iq"])
		self.path = os.path.expanduser(os.path.join(folder,"manifest.xml"))
		self.et = ET.parse(self.path)
		self.root = self.et.getroot()

	def get_type(self):
		return tag(self.root.getchildren()[0])

	def set_id(self, new_id):
		self.root.getchildren()[0].set('id',new_id)
		self.et.write(self.path)

	def devices(self):
		return [d.get("id") for d in self.root.findall(".//iq:product",self.ns)]
	def permissions(self):
		return [p.get("id") for p in self.root.findall(".//iq:uses-permission",self.ns)]
	def languages(self):
		return [l.get("id") for l in self.root.findall(".//iq:language",self.ns)]
	def barrels(self):
		return [b.get("id") for b in self.root.findall(".//iq:barrels",self.ns)]
