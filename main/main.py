from threading import Thread
from synthesizer import Player, Synthesizer, Waveform
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio as play
import rtmidi
import time

#midi initialisation
midiin = rtmidi.RtMidiIn()

#synth initialisation
player = Player()
player.open_stream()

#drum sound initialisation
hi_hat = AudioSegment.from_wav("sounds/hi_hat.wav")
kick = AudioSegment.from_wav("sounds/kick.wav")

drumloop0run = False
drumloop1run = False

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
			time.sleep(0.025) # small window to accommodate poor raspi processing power
			startbar = False
			time.sleep(spb * 4)

#################################################
#midi input
class ControllerInput:
	def __init__(self):
		self._running = True
	def terminate(self):
		self._running = False
	def run(self):
		global note
		global kick_toggle
		global drumloop0run
		global drumloop1run
		global volume_toggle
		global volume_1
		
		print("Opening port 1!") 
		midiin.openPort(1)
		while True:
			m = midiin.getMessage(0) # some timeout in ms
			if m:
				#if m.isController():
				#	print('CONTROLLER', m.getControllerNumber(), m.getControllerValue())
				#	if m.getControllerNumber() == 1:
				#		volume_1 = m.getControllerValue() / 128
				if m.isNoteOn():
					print(m.getMidiNoteName(m.getNoteNumber()))
					if (m.getMidiNoteName(m.getNoteNumber()) == "C2"):
						play(hi_hat)
					elif (m.getMidiNoteName(m.getNoteNumber()) == "A1"):
						drumloop0run = not drumloop0run
					elif (m.getMidiNoteName(m.getNoteNumber()) == "A#1"):
						drumloop1run = not drumloop1run
					else:
						note = m.getMidiNoteName(m.getNoteNumber())
						volume_toggle = True
				elif m.isNoteOff() and note == m.getMidiNoteName(m.getNoteNumber()):
					volume_toggle = False

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
			print("DrumLoop0 looping")
			play(kick)
			time.sleep(quaver) # 0.5
			play(kick)
			time.sleep(quaver) # 0.5
			play(hi_hat)
			time.sleep(crotchet) # 1
			play(kick)
			# bar 1
			time.sleep(quaver)
			play(kick)
			time.sleep(quaver) 
			play(hi_hat)
			time.sleep(crotchet)
			play(kick)
			# bar 2
			time.sleep(quaver)
			play(kick)
			time.sleep(quaver)
			play(hi_hat)
			time.sleep(crotchet)
			play(hi_hat)
			# bar 3
			time.sleep(crotchet)
			play(kick)
			time.sleep(quaver)
			play(hi_hat)
			time.sleep(quaver)
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
		print("DrumLoop0 thread running")
		global kick_toggle
		global drumloop1run
		repeat = False
		
		def drumloop1():
			play(hi_hat)
			time.sleep(semiquaver) #0.25
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
		
ControllerInputThread = Thread(target=ControllerInput().run)
ControllerInputThread.start()

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
		synth = Synthesizer(osc1_waveform = Waveform.sine, osc1_volume = volume_1, use_osc2=False)
		#player.play_wave(synth.generate_constant_wave(note,0.5))
	except (KeyboardInterrupt, SystemExit):
		print("\n<!> Received KeyboardInterrupt, quitting.\n")
		Exit = True
		
DrumLoop0Thread().terminate()
DrumLoop1Thread().terminate()
ControllerInput().terminate()
print("Goodbye!")