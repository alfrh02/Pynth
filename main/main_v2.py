#############################################
#											#
#				Orbitron Mk1				#
#			Tested on AKAI MPK Mini			#
#											#
#############################################


from pydub.playback import _play_with_simpleaudio as play
from pydub import AudioSegment
from threading import Thread
import sounddevice as sd
import numpy as np
import rtmidi
import time
import math

sample_rate = 44100
duration = 20
frequency = -1

#for synth generation
x = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))

#midi initialisation
midiin = rtmidi.RtMidiIn()

synth_type = 0 
volume_1 = 1
volume_multiplier = 0
stop_playing = False

hi_hat = AudioSegment.from_wav("sounds/hi_hat.wav")
kick = AudioSegment.from_wav("sounds/kick.wav")

#midi input
class ControllerInput:
	def __init__(self):
		self._running = True
	def terminate(self):
		self._running = False
	def run(self):
		global volume_1
		global volume_multiplier
		global stop_playing
		global frequency
		global synth_type
		global duration
		global x
		
		def NoteToFrequency(note):
			notes = ["C4", "D4", "E4", "F4", "G4", "A4", "B4"]
			note_frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440, 493.88]
			notes_sharp = ["C#4", "D#4", "F#4", "G#4", "A#4"]
			note_frequencies_sharp = [277.18, 311.13, 369.99, 415.30, 466.16]
			
			octave_multiplier = 2 # an octave below A4/440Hz is A3/220Hz
						
			if len(note) == 3:
				note_octave = int(note[2])
				for i in range(5):
					if note[0] == notes_sharp[i][0]:
						note_freq = note_frequencies_sharp[i]
			else:
				note_octave = int(note[1])
				for i in range(7):
					if note[0] == notes[i][0]:
						note_freq = note_frequencies[i]
			
			if note_octave > 4:
				for i in range(note_octave - 4):
					note_freq = note_freq * 2
			else:
				for i in range((note_octave - 4)*-1):
					note_freq = note_freq / 2
					
			print(note + " = " + str(note_freq))
			return note_freq
			
					
					
		print("Opening port 1!") 
		midiin.openPort(1)
		NoteToFrequency("F2")
		note = "A4"
		while True:
			m = midiin.getMessage(0) # some timeout in ms
			if m:
				if m.isController():
					print('CONTROLLER', m.getControllerNumber(), m.getControllerValue())
					if m.getControllerNumber() == 1:
						volume_1 = m.getControllerValue() / 128
					if m.getControllerNumber() == 2:
						duration = m.getControllerValue() / 8 + 7
						print(duration)
				if m.isNoteOn():
					volume_multiplier = 1
					if m.getMidiNoteName(m.getNoteNumber()) == "C2":
						play(hi_hat)
					elif m.getMidiNoteName(m.getNoteNumber()) == "C#2":
						play(kick)
					elif m.getMidiNoteName(m.getNoteNumber()) == "D2":
						synth_type = 0 #square, default
						print("Synth changed to square")
					elif m.getMidiNoteName(m.getNoteNumber()) == "D#2":
						synth_type = 1 #sine
						print("Synth changed to sine")
					elif m.getMidiNoteName(m.getNoteNumber()) == "A#1":
						synth_type = 2 #sawtooth
						print("Synth changed to sawtooth")
					else:
						print(m.getMidiNoteName(m.getNoteNumber()))
						note = m.getMidiNoteName(m.getNoteNumber())
						frequency = NoteToFrequency(m.getMidiNoteName(m.getNoteNumber()))
						stop_playing = True
				elif m.isNoteOff() and m.getMidiNoteName(m.getNoteNumber()) == note:
					stop_playing = True
					frequency = -1
					volume_multiplier = 0
					
			x = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))

####

ControllerInputThread = Thread(target=ControllerInput().run)
ControllerInputThread.start()

def play_note(frequency):
	if synth_type == 0:#square
		synth_data = np.round(np.sin(frequency * x) / 2 + 0.5) - 0.5
	elif synth_type == 1: #sine
		synth_data = np.sin(frequency * x)
	elif synth_type == 2: #sawtooth
		synth_data = -2 / np.pi *np.arctan(np.tan(np.pi / 2 - (x * np.pi / (1 / frequency * 2 * np.pi))))
	synth_data = synth_data * ((volume_1 * 0.3) * volume_multiplier) # volume
	sd.play(synth_data, sample_rate)

Exit = False
while Exit == False:
	try:
		if stop_playing == True:
			sd.stop()
			stop_playing = False
		play_note(frequency)
	except (KeyboardInterrupt, SystemExit):
		print("\n<!> Received KeyboardInterrupt, quitting.\n")
		Exit = True
				
ControllerInput().terminate()
print("Goodbye!")
