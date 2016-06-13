import threading

TEMP = threading.Lock()

dummy = ["date", "?", "TeamA", "?", "?", "TeamB","url"]

details = []

def FileHandle(mode, lock = TEMP, args=None,):
	lock.acquire()
	print "file handling lock acquired in ",mode, " mode."

	if mode == 'w':
		# called from scrape.main()
		f = open('games.txt', 'w')
		# print "Writing objects to file."
		for obj in args:
			# print obj
			f.write(str(obj)+'\n')
		# print "objects are ready to be read."
		f.close()
	else:
		# called from gui.main()
		f = open('games.txt','r')
		# if it has something, read it
		if f.read():
			f.seek(0)
			for line in f.readlines():
				details.append(line.split(';'))
		else:
			# otherwise put some dummy data
			details.append(dummy)
		f.close()
	lock.release()
	print "lock released from ",mode," mode."

