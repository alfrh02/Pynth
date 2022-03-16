import rtmidi
from synthesizer import Player, Synthesizer, Waveform

midiin = rtmidi.RtMidiIn()

player = Player()
player.open_stream()

volume_1 = 0.75
note = "A4"

def print_message(midi):
	if midi.isNoteOn():
		print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
	elif midi.isNoteOff():
		print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
	elif midi.isController():
		print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())

swap = True
if True:
	print("Opening port 1!") 
	midiin.openPort(1)
	while True: #loop
		m = midiin.getMessage(100) # some timeout in ms
		if m:
			print_message(m)
			if m.isController():
				print('CONTROLLER', m.getControllerNumber(), m.getControllerValue())
				if m.getControllerNumber() == 1:
					volume_1 = m.getControllerValue() / 128
			elif m.isNoteOn():
				note = m.getMidiNoteName(m.getNoteNumber())
			elif m.isNoteOff() and note == m.getMidiNoteName(m.getNoteNumber()):
				note = 0.0
		synth = Synthesizer(osc1_waveform = Waveform.sine, osc1_volume = volume_1, use_osc2=False)
		#player.play_wave(synth.generate_constant_wave(note,0.01))
else:
	print('NO MIDI INPUT PORTS!')
	