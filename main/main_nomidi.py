from threading import Thread
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
import time

#drum sound initialisation
hi_hat = AudioSegment.from_wav("sounds/hi_hat.wav")
kick = AudioSegment.from_wav("sounds/kick.wav")

drumloop0run = True
drumloop1run = True

startbar = False
kick_toggle = False
note = 0.0
volume_toggle = True
volume_1 = 0.75

bpm = 100 # beat per minute - tempo
bps = bpm / 60 # beat per second
spb = 1 / bps # seconds per beat

print("BPM: ", bpm)
print("BPS: ", bps)
print("SPB: ", spb)

semibreve = spb * 4 # 4 beats per bar
minim = spb * 2 # 2 beats per bar
crotchet = spb # 1 beat per bar
quaver = spb * 0.5 # 0.5 beats per bar
semiquaver = spb * 0.25 # 0.25 beats per bar

#################################################
# keeps drum loops in sync by setting "startbar" boolean to true at the start of each bar
class Barkeep:
	def __init__(self):
		self._running = True
	def terminate(self):
		self._running = False
	def run(self):
		print("Barkeep thread running")
		global startbar
		while True:
			startbar = True
			print("startbar True")
			time.sleep(0.005) # small window to accommodate poor raspi processing power
			startbar = False
			time.sleep(spb * 4)

#################################################
#first drum loop			
class DrumLoop0:
	def __init__(self):
		self._running = True
	def terminate(self):
		self._running = False
	def run(self):
		print("DrumLoop0 thread running")
		global kick_toggle
		global drumloop0run
		repeat = False
		
		def drumloop0():
			play(hi_hat)
			time.sleep(crotchet) # 1
			play(hi_hat)
			time.sleep(crotchet) # 1
		while True:
			if drumloop0run == True and startbar == True:
				drumloop0()
				if drumloop0run == True:
					repeat = True
			if drumloop0run == True and repeat == True:
				drumloop0()

#################################################	
#second drum loop
class DrumLoop1:
	def __init__(self):
		self._running = True
	def terminate(self):
		self._running = False
	def run(self):
		print("DrumLoop1 thread running")
		global kick_toggle
		global drumloop1run
		repeat = False
		
		def drumloop1():
			play(kick)
			time.sleep(quaver) # 1
			play(kick)
			time.sleep(crotchet + quaver) # 1
		while True:
			if drumloop1run == True and startbar == True:
				drumloop1()
				if drumloop1run == True:
					repeat = True
			if drumloop1run == True and repeat == True:
				drumloop1()

#################################################

# threads - barkeep, midi input, drum loops
BarkeepThread = Thread(target=Barkeep().run)
BarkeepThread.start()
	
DrumLoop0Thread = Thread(target=DrumLoop0().run)
DrumLoop0Thread.start()

DrumLoop1Thread = Thread(target=DrumLoop1().run)
DrumLoop1Thread.start()

#while loop for synthesiser
Exit = False
while Exit == False:
	try:
		if volume_toggle == False:
			volume_1 = 0.0
	except (KeyboardInterrupt, SystemExit):
		print("\n<!> Received KeyboardInterrupt, quitting.\n")
		Exit = True
		
DrumLoop0Thread().terminate()
DrumLoop1Thread().terminate()
ControllerInput().terminate()
print("Goodbye!")