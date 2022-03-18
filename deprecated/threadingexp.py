from threading import Thread
import time
import sys

global cycle
cycle = 0.0

class Hello5Program:
	def __init__(self):
		self._running = True
	def terminate(self):
		self._running = False
	def run(self):
		global cycle
		while self._running:
			time.sleep(5)
			cycle = cycle + 1.0
			print("5 Second Thread cycle + 1.0 - ", cycle)
	
FiveSecondThread = Thread(target=Hello5Program().run)
FiveSecondThread.start()

Exit = False
while Exit == False:
	try:
		cycle = cycle + 0.1
		print("Main Program increases cycle + 0.1 - ", cycle)
		time.sleep(1)
		if (cycle > 5): Exit = True
	except (KeyboardInterrupt, SystemExit):
		print("\n<!> Received KeyboardInterrupt, quitting threads.\n")
		Hello5Program().terminate()
		sys.exit()
		
Hello5Program().terminate()
print("Goodbye!")