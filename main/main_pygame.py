from threading import Thread
from synthesizer import Player, Synthesizer, Waveform
from pydub import AudioSegment
from pydub.playback import play
import rtmidi
import sys
import time

bpm = 100 # beat per minute
bps = bpm / 60 # beat per second
spb = 1 / bps # seconds per beat

hi_hat = AudioSegment.from_wav("sounds/hi_hat.wav")
kick = AudioSegment.from_wav("sounds/kick.wav")

kick_toggle = False
drum_loop0 = False

kick_duration = kick.duration_seconds
hi_hat_duration = hi_hat.duration_seconds

kick_per_beat = spb - kick_duration
hi_hat_per_beat = spb - hi_hat_duration

midiin = rtmidi.RtMidiIn()

global note
note = 0.0

global volume_toggle
volume_toggle = True

global volume_1
volume_1 = 0.75

player = Player()
player.open_stream()

print("BPM: ", bpm)
print("BPS: ", bps)
print("SPB: ", spb)

print("KICK DURATION: ", kick_duration)
print("KICK_PER_BEAT: ", kick_per_beat)
print("HI_HAT DURATION: ", hi_hat_duration)
print("HI_HAT_PER_BEAT: ", hi_hat_per_beat)

class ControllerInput:
	def __init__(self):
		self._running = True
	def terminate(self):
		self._running = False
	def run(self):
		global note
		global kick_toggle
		global drum_loop0
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
					elif (m.getMidiNoteName(m.getNoteNumber()) == "C#2"):
						drum_loop0 = True
					else:
						note = m.getMidiNoteName(m.getNoteNumber())
						volume_toggle = True
				elif m.isNoteOff() and note == m.getMidiNoteName(m.getNoteNumber()):
					volume_toggle = False
					
ControllerInputThread = Thread(target=ControllerInput().run)
ControllerInputThread.start()

class DrumMachine:
	def __init__(self):
		self._running = True
	def terminate(self):
		self._running = False
	def run(self):
		print("DrumMachine thread running")
		global kick_toggle
		global drum_loop0
		while True:
			if drum_loop0 == True:
				print("drum loop 0")
				play(kick)
				time.sleep(kick_per_beat) #remainder of time after sound
				time.sleep(spb)
				play(hi_hat)
				time.sleep(hi_hat_per_beat)
				time.sleep(spb)
			if kick_toggle == True:
				play(kick)
				kick_toggle = False
			
DrumMachineThread = Thread(target=DrumMachine().run)
DrumMachineThread.start()

Exit = False
while Exit == False:
	try:
		if volume_toggle == False:
			volume_1 = 0.0
		synth = Synthesizer(osc1_waveform = Waveform.sine, osc1_volume = volume_1, use_osc2=False)
		player.play_wave(synth.generate_constant_wave(note,0.5))
	except (KeyboardInterrupt, SystemExit):
		print("\n<!> Received KeyboardInterrupt, quitting threads.\n")
		ControllerInput().terminate()
		DrumMachine().terminate()
		Exit = True
		
DrumMachine().terminate()
ControllerInput().terminate()
print("Goodbye!")