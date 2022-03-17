from threading import Thread
from synthesizer import Player, Synthesizer, Waveform
from pydub import AudioSegment
from pydub.playback import play
import rtmidi
import sys

hi_hat = AudioSegment.from_wav("sounds/hi_hat.wav")
kick = AudioSegment.from_wav("sounds/kick.wav")

midiin = rtmidi.RtMidiIn()

global note
note = 0.0

global volume_toggle
volume_toggle = True

global volume_1
volume_1 = 0.75

player = Player()
player.open_stream()

class ControllerInput:
	def __init__(self):
		self._running = True
	def terminate(self):
		self._running = False
	def run(self):
		global note
		global volume_toggle
		global volume_1
		print("Opening port 1!") 
		midiin.openPort(1)
		while True:
			m = midiin.getMessage(100) # some timeout in ms
			if m:
				if m.isController():
					print('CONTROLLER', m.getControllerNumber(), m.getControllerValue())
					if m.getControllerNumber() == 1:
						volume_1 = m.getControllerValue() / 128
				elif m.isNoteOn():
					print(m.getMidiNoteName(m.getNoteNumber()))
					if (m.getMidiNoteName(m.getNoteNumber()) == "C2"):
						play(hi_hat)
					else:
						note = m.getMidiNoteName(m.getNoteNumber())
						volume_toggle = True
				elif m.isNoteOff() and note == m.getMidiNoteName(m.getNoteNumber()):
					volume_toggle = False
	
ControllerInputThread = Thread(target=ControllerInput().run)
ControllerInputThread.start()

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
		Exit = True
		
ControllerInput().terminate()
print("Goodbye!")