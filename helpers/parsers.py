import xml.etree.ElementTree as ET
import os


def tag(element):
	return element.tag.split("}")[1]

class Manifest(object):
	"""Helper class for reading and modifying a manifest.xml file"""

	ns = { "iq": "http://www.garmin.com/xml/connectiq" }

	#@todo: read manifest.xml file name from monkey.jungle, whatever THAT filename might be too
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


class SDK(object):
	"""Helper wrapper for reading things from a provided SDK"""
	def __init__(self, path):
		super(SDK, self).__init__()
		self.path = os.path.expanduser(path)

	""" Things attained from compilerInfo.xml """
	def compilerInfo(self):
		et = ET.parse(os.path.join(self.path,"bin","compilerInfo.xml"))
		return et.getroot()

	def version(self):
		compilerInfo = self.compilerInfo()
		return compilerInfo.find('version').text

	def exitCodeMessage(self, code):
		compilerInfo = self.compilerInfo()
		matches = compilerInfo.findall("./exitCodes/code[@value='"+str(code)+"']")
		return matches[0].get("meaning") if len(matches) else None

	def targetSDKs(self):
		compilerInfo = self.compilerInfo()
		versions = compilerInfo.findall("./targetSdkVersions/version")
		return [v.text for v in versions]


	""" Things attained from projectInfo.xml """
	def projectInfo(self):
		et = ET.parse(os.path.join(self.path,"bin","projectInfo.xml"))
		return et.getroot()

	def permissionInfo(self):
		projectInfo = self.projectInfo()
		perms = projectInfo.findall("./appPermissions/permission")
		return [p.attrib for p in perms]

	def getInfoForPermission(self, permission):
		projectInfo = self.projectInfo()
		matches = projectInfo.findall("./appPermissions/permission[@id='"+permission+"']")
		return matches[0].attrib if len(matches) else None
		
	def availablePermissionsForAppType(self, app):
		projectInfo = self.projectInfo()
		perms = projectInfo.findall("./permissionMaps/permissionMap[@appType='"+app+"']//permission")
		return [p.attrib for p in perms] if len(perms) else None

	def appTypes(self):
		projectInfo = self.projectInfo()
		types = projectInfo.findall("./appTypes/appType")
		return [t.attrib for t in types]


	""" Things attained from devices.xml """
	def deviceInfo(self):
		et = ET.parse(os.path.join(self.path,"bin","devices.xml"))
		return et.getroot()

	def getDevices(self):
		deviceInfo = self.deviceInfo()
		devices = deviceInfo.findall("./devices/device")
		return [Device(d) for d in devices]

	def getDevice(self, identifier):
		deviceInfo = self.deviceInfo()
		device = deviceInfo.findall("./devices/device[@id='"+identifier+"']")
		return Device(device[0]) if device else None

class Device(object):
	"""Wrapper class for device info, as defined in devices.xml"""
	def __init__(self, element):
		super(Device, self).__init__()
		self.element = element
		self.id = self.element.get("id")
		self.name = self.element.get("name")
		self.bpp = self.element.find("bpp").text
		self.resolution = self.element.find("resolution").attrib
		parts = self.element.findall(".//part_number")
		self.ciq_versions = [p.get("connectIQVersion") for p in parts]

		# many ignored fields including: languages, launcher icon, orientation, image, palette, datafieldlayouts, app types