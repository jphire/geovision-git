# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__ = "lassetyr"
__date__ = "$23.5.2011 15:12:48$"


class SampleRead:
	def __init__(self, readid, description, data):
		self.readid = readid.strip('\n')
		self.description = description.strip('\n')
		self.data = data

	def __str__(self):
		return str("Read id: " + self.readid + "\n" \
				   + "Description: " + self.description + "\n" \
				   + "Data: " + self.data + "\n")

class SamplefileParser:
	def __init__(self, source_file):
		try:
			self.textfile = open(source_file, 'r')
		except:
			print "fail"
			# TODO: fix
		self.nextline = self.textfile.readline()
		self.dnadata = ''
		self.infoline = []

	def next_read(self):
		if self.nextline is '':
			return None
		self.dnadata = ""
		self.infoline = self.nextline.strip('>').split(None, 1)
		if len(self.infoline) < 2:
			self.infoline.append('')
		self.nextline = self.textfile.readline()
		while (self.nextline[0] is not '>'):
			self.dnadata += self.nextline.strip()
			self.nextline = self.textfile.readline()
			if len(self.nextline) is 0:
				break
		return SampleRead(self.infoline[0], self.infoline[1], self.dnadata)