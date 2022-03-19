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
frequency = 0

#sine wave initialisation
x = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))

#midi initialisation
midiin = rtmidi.RtMidiIn()

volume_1 = 1
stop_playing = False

#midi input
class ControllerInput:
	def __init__(self):
		self._running = True
	def terminate(self):
		self._running = False
	def run(self):
		global volume_1
		global stop_playing
		global frequency
		
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
		while True:
			m = midiin.getMessage(0) # some timeout in ms
			if m:
				if m.isController():
					print('CONTROLLER', m.getControllerNumber(), m.getControllerValue())
					if m.getControllerNumber() == 1:
						volume_1 = m.getControllerValue() / 128
				if m.isNoteOn():
					print(m.getMidiNoteName(m.getNoteNumber()))
					note = m.getMidiNoteName(m.getNoteNumber())
					frequency = NoteToFrequency(m.getMidiNoteName(m.getNoteNumber()))
					stop_playing = True
				elif m.isNoteOff() and m.getMidiNoteName(m.getNoteNumber()) == note:
					stop_playing = True
					frequency = 0

####

ControllerInputThread = Thread(target=ControllerInput().run)
ControllerInputThread.start()

def play_note(frequency):
	sinewave_data = np.sin(frequency * x)
	sinewave_data = sinewave_data * (volume_1 * 0.3) # volume
	sd.play(sinewave_data, sample_rate)

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
