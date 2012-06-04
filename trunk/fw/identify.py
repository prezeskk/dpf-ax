import struct
import struct
import sys
import time
import binascii

# Nedded for fulldump
sys.path.append("../Debug")
import dpf
import detect

# DPF profiles
import knowndpfs

# Set this to 1 to get additional infos
dev_mode = 0

JUMPTABLE_OFFSET_BUILDWIN = 0x80
JUMPTABLE_OFFSET_COBY = 0x180

jumptable_offset = 0

############################################################################

bswap = lambda x: ( (x >> 8) & 0xff ) | ((x << 8) & 0xff00)

def find_dpf_by_version_string(buf):
	version = (buf[0x50:0x58], buf[0x60: 0x70], buf[jumptable_offset:jumptable_offset+8])
	for i in knowndpfs.KNOWN_DPFS:
		if len(i[0]) > 0:
			v = i[0]
			if v[0] == str(version[0]) and v[1] == str(version[1]) and v[2] == str(version[2]):
				return i
	return None

def get_module(buf, n):
	global jumptable_offset
	n *= 8
	n += jumptable_offset
	start, end, flashaddr = struct.unpack("<HHI", buf[n:n+8])

	start = bswap(start)
	end = bswap(end)

	return start, end, flashaddr

def isBuildwinFw(buf):
	global jumptable_offset
	version = (buf[0x50:0x58], buf[0x60: 0x70], buf[JUMPTABLE_OFFSET_BUILDWIN:JUMPTABLE_OFFSET_BUILDWIN+8], buf[JUMPTABLE_OFFSET_COBY:JUMPTABLE_OFFSET_COBY+8])
	if version[0] == "20120101":
		return -1
	if version[0].isdigit():
		if version[1][3] == " " and version[1][6] == " " and version[1][7:10].isdigit():
			if version[2].startswith("ProcTbl"):
				jumptable_offset = JUMPTABLE_OFFSET_BUILDWIN
			elif version[3].startswith("ProcTbl"):
				jumptable_offset = JUMPTABLE_OFFSET_COBY
			if jumptable_offset != 0:
				i = 1
				p = jumptable_offset + 8

				while buf[p:p+8] != "-EndTbl-" and i < 60:
					p += 8
					i += 1
				if i > 10 and i < 60:
					return i
	return 0

val = lambda x: ord(x)

scan_locate_displaysize = [
0xE4, 0xF5, val, 0xF5, val, 0xF5, val, 0xF5, val,
0x75, val, val, 0x75, val, val, 0x75, val, val, 0x75, val, val, 
0x12, val, val,
0xE4, 0xFB, 0xFC, 0xE4, 0xFD, 0xFE, 0xE5
]
scan_locate_lcdinit = [
0x75, 0xEC, 0x00, 0x53, 0xEA, 0xE8,
]
scan_locate_stdlcdinit = [
0x75, 0xEC, 0x00, 0x53, 0xEA, 0xE8, 0x53, 0xEB, 0xFD, 0x53, 0xA0, 0xFD,
0x12, val, val, 0x12, val, val, 0x12, val, val, 0x12, val, val, 0x12, val, val,
0x53, 0x90, 0xFE,
0x12, val, val, 0x12, val, val, 0x12, val, val, 0x12, val, val, 0x12, val, val, 0x12, val, val, 0x12, val, val, 0x12, val, val,
0x43, 0x90, 0x01, 0x7F
]
scan_locate_initbl = [
0x70, 0x01, 0x22, 0x90, val, val, 0xC0, 0xF0, 0xF5, 0xF0, 0xE4, 0x93, 0xC3, 0x25, 0x82, 0xC5, 0x82
]
scan_locate_openwin = [
0x90, 0x0a, 0x80, 0x7b, val, 0x7c, val, 0x7d, 0x00, 0x7e, val, 0x7f, val, 0x12
]

# Stolen from dump.py, stolen from scantool:
class Scanner:
	def __init__(self, data, seq):
		self.data = data
		self.args = []
		self.scansequence = seq

	def scan(self, context, cb):
		p = 0
		n = 0
		while p < len(self.data):
			if type(self.scansequence[n]) == type(val):
				self.args.append(val(self.data[p]))
				n += 1
			elif chr(self.scansequence[n]) == self.data[p]:
				n += 1
			else:
				n = 0
				self.args = []

			if n == len(self.scansequence):
				cb(context, self.args, p - len(self.scansequence) + 1)
				n = 0
				self.args = []

			p += 1


def add_offs(context, args, p):
	e, offset = context
	e.append(p)
	for i in range(len(args) / 2):
		off = args[i*2] << 8 | args[i*2 + 1]
		e.append(off)

def add_vals(context, args, p):
	e, offset = context
	e.append(p)
	for i in range(len(args)):
		e.append(args[i])

def dump_tables(tbls):
	outf = open("lcdinitbl_tmp.txt", "w")
	for tbl in tbls:
		outf.write(tbl[0])
		outf.write("::")
		for  i in range(0, len(tbl[1])):
			if (i % 10) == 0:
				outf.write("\n  .db  ")
			else:
				outf.write(", ")
			outf.write("0x%02x" % struct.unpack("B", tbl[1][i])[0])
		outf.write("\n%s_len::  .db  %d" % (tbl[0], len(tbl[1])))
		outf.write("\n\n")
	outf.close()


lcdinit_found = False

def find_initbl(buf, module):
	global lcdinit_found
	tbls = []
	start, end, flashaddr = get_module(buf, module)
	l = end - start
	start += 0x800
	data = buf[flashaddr : flashaddr + l]

	if dev_mode > 1:
		initbloffs = []
		scanner = Scanner(data, scan_locate_stdlcdinit)
		scanner.scan((initbloffs, start), add_offs)
		if len(initbloffs) > 0:
			p = initbloffs[0]
			print
			print "Module %d:" % module
			print "LcdInit (Tbl)   at 0x%04x (0x%06x)" % (p + start, p + flashaddr)
			lcdinit_found = True
		else:
			initbloffs = []
			scanner = Scanner(data, scan_locate_lcdinit)
			scanner.scan((initbloffs, start), add_offs)
			if len(initbloffs) > 0:
				p = initbloffs[0]
				print
				print "Module %d:" % module
				print "LcdInit !NOTBL! at 0x%04x (0x%06x)" % (p + start, p + flashaddr)
				lcdinit_found = True
		
	initbloffs = []
	c = 0
	scanner = Scanner(data, scan_locate_initbl)
	scanner.scan((initbloffs, start), add_offs)
	if len(initbloffs) == 2:
	    try:
		p = initbloffs[1] - start
		i = struct.unpack("B", data[p])[0]
		if dev_mode:
			if not lcdinit_found:
				print
			print "Module %d:" % module
			print "LcdScheduleTbl  at 0x%04x (0x%06x), len 0x%02x" % (p + start, p + flashaddr, i)
			#tbls.append(["_custom_scheduletbl", data[p+1:p+i+1]])
		p += i + 1
		i = struct.unpack("B", data[p])[0]
		if dev_mode:
			print "LcdContrastTbl  at 0x%04x (0x%06x), len 0x%02x" % (p + start, p + flashaddr, i)
			tbls.append(["_custom_lcdcontrasttbl", data[p+1:p+i+1]])
		p += i + 1
		i = struct.unpack("B", data[p])[0]
		if dev_mode:
			print "LcdContrastTb2  at 0x%04x (0x%06x), len 0x%02x" % (p + start, p + flashaddr, i)
			tbls.append(["_custom_contrasttbl2", data[p+1:p+i+1]])
		p += i + 1
		i = struct.unpack("B", data[p])[0]
		if dev_mode:
			  print "LcdBacklightTbl at 0x%04x (0x%06x), len 0x%02x" % (p + start, p + flashaddr, i)
			  tbls.append(["_custom_backlighttbl", data[p+1:p+i+1]])
		p += i + 1
		j = i
		i = struct.unpack("B", data[p])[0]
		if (i == j):   		# seems to have two LcdBackLightTbls...
			if dev_mode:
				print "LcdBacklightTb2 at 0x%04x (0x%06x), len 0x%02x" % (p + start, p + flashaddr, i)
				tbls.append(["_custom_backlighttbl2", data[p+1:p+i+1]])
			p += i + 1
		else:
			tbls.append(["_custom_backlighttbl2", ""])

		l = struct.unpack("<H", data[p : p+2])[0]
		p += 2
		if (p + l) < len(data):
		    lcdinitbl = data[p:p+l]
		    if dev_mode:
			print "LcdIniTbl       at 0x%04x (0x%06x), len 0x%02x," % (p + start, p + flashaddr, l),
			tbls.append(["_custom_initseq", data[p:p+l] + "\xFF"])
		    c = binascii.crc32(lcdinitbl) & 0xffffffff
		    if dev_mode:
				print "CRC = 0x%x" % c
			        if dev_mode > 1:
				    dump_tables(tbls)
				    print "Written to lcdinitbl_tmp.txt."
	    except:
		if dev_mode:
			print "Invalid LcdIniTbl!"

	return c

def find_openwin(buf):
	openwinoffs = []
	c = 0
	b = buf[:7]
	xmem, code, dummy, offset = struct.unpack(">HHBH", b)
	scanner = Scanner(buf[offset:0x10000], scan_locate_openwin)
	scanner.scan((openwinoffs, offset), add_offs)
	if len(openwinoffs) == 3:
		openwin_found = True
		p = openwinoffs[2]
		l = openwinoffs[1] - 0xa80
		if dev_mode:
			print
			print "OpenWin        at 0x1280 (0x%06x), len 0x%02x," %  (p, l),
		openwin = buf[p:p+l]
		if dev_mode > 1:
			outf = open("openwin_tmp.bin", "wb")
			outf.write(openwin)
			outf.close()
		c = binascii.crc32(openwin) & 0xffffffff
		if dev_mode:
			print "CRC = 0x%x" % c
			if dev_mode > 1:
				print "Written to openwin_tmp.bin."
	else:
		c = 0
		if len(openwinoffs) > 3:
			print "More than one match!"
			if dev_mode:
				for i in range(len(openwinoffs) / 3):
					print "Match %d at flashoffset 0x%06x, adr 0x%06x len 0x%04x" % (i, openwinoffs[i*3], openwinoffs[i*3 + 2], (openwinoffs[i*3 + 1]) - 0xa80)
		else:
			print "Not found."

	return c

def match_crc(crc, checksums):
	#if crc != 0:
	j = 0
	try:
		j = checksums.index(crc)
	except ValueError:
		j = -1
	if j != -1:
		return True
	return False

def recognize_dpf(dump):
	global jumptable_offset
	partial_match = []

	# Check if its a buildwin fw
	print "Looking for firmware.............:",
	num_modules = isBuildwinFw(dump)
	if num_modules > 0:
		w, h = struct.unpack("<HH", dump[0x23:0x27])
		mfg = "buildwin"
		if jumptable_offset == JUMPTABLE_OFFSET_COBY:
			mfg = "coby"
		print "Found (%s, %dx%d px)." % (mfg, w, h)
	else:
		print "Not found."
		print
		if num_modules == -1:
			print "This is already a custom firmware!"
		else:
			print "This in no known firmware!"
		return None, partial_match

	# Look for display known by their fw and build-date (old way)
	print "Looking for known version info...:",
	dpf = find_dpf_by_version_string(dump)
	if dpf:
		print "Found."
		return dpf, partial_match
	print "None."

	# Try to find OpenWin and LcdIniTbl
	print "Looking for Openwin..............:",
	crc_openwin = find_openwin(dump)
	if crc_openwin == 0:
		print "WARNING: This is no \"standard\" buildwin software!"
	elif not dev_mode:
		print "Found."

	print "Looking for LcdIniTbl............:",
	initbl_count = 0
	crc_initbl = 0
	for i in range(1, num_modules):
		c = find_initbl(dump, i)
		if c != 0:
			crc_initbl = c
			initbl_count += 1
	if initbl_count == 0:
		print "None."
	elif initbl_count > 1:
		print "%d matches." % initbl_count
	elif not dev_mode:
		print "Found."
	if not crc_initbl:
		print "WARNING: This is no \"standard\" buildwin software!"
			

	# Now look for display known by their signatur of LcdIniTbl and OpenWin (new way)
	print "Looking for known signatures.....:",
	if dev_mode:
		print
	for i in knowndpfs.KNOWN_DPFS:
		record = i[3]
		if len(record) > 0:
			has_initbl = match_crc(crc_initbl, record[0])
			has_openwin = match_crc(crc_openwin, record[1])
			if has_initbl and has_openwin:
				if not dev_mode:
					print "Found."
				return i, None
			if has_initbl and record[0][0] != 0 and i[1][1] == "yes":
				partial_match.append(i[1][0])
				if dev_mode:
					print "LcdIniTbl: match at model %s" % i[1][0]
			if has_openwin and i[1][1] == "yes":
				partial_match.append(i[1][0])
				if dev_mode:
					print "OpenWin:   match at model %s" % i[1][0]
	print "None."
	return None, partial_match
	
#
#
# MAIN

if len(sys.argv) != 2:
	print "Usage: python %s dumpfile|dpf-devicenode" % sys.argv[0]
	sys.exit(-1)

dumpfile = sys.argv[1]
if dumpfile.startswith("/dev/"):
#
# copy of fulldump.py
#
	print "Detecting & reading dpf flash..."
	d = dpf.open(sys.argv[1])
	size = detect.detect_flash(d)
	# Offset, size
	print "Reading %x bytes..." % size
	buf = d.readFlash(0x00, size)
	f = open("full.bin", "wb")
	f.write(buf)
	f.close()
	d.close()
	print "Flash written to file 'full.bin'."
	print
	dumpfile = "full.bin"
	
f = open(dumpfile, "rb")
data = f.read()
f.close()
dpf, pm = recognize_dpf(data)

print
    
if dpf:
	if dpf[1][1] == "yes":
		print "Your dpf is compatible with model %s." % dpf[1][0]
	elif dpf[1][1] == "no":
		print "Your dpf is compatible with unsupported model %s." % dpf[1][0]
		print "Sorry, this dpf in NOT supported by dpf-ax."
	elif dpf[1][1] == "wip":
		print "Your dpf is compatible with currently unsupported model %s." % dpf[1][0]
		print "Sorry, this dpf in NOT supported by dpf-ax at the moment."
		print "Work in progress. Check back later."
else:
	print "Sorry, no matching dpf found."
	if len(pm) > 0:
		print "But following models have a partial signature match:",
		print pm
print