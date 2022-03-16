import rtmidi
import pygame

pygame.init()
midiin = rtmidi.RtMidiIn()

width = 800
height = 800

pygame.display.set_caption("RGB Demo")
screen = pygame.display.set_mode((width,height))

player_img = pygame.image.load("player.png")
player_rect = player_img.get_rect()
player_location = [25,25]

r = 0
g = 0
b = 0

def print_message(midi):
	if midi.isNoteOn():
		print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
	elif midi.isNoteOff():
		print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
	elif midi.isController():
		print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())

ports = range(midiin.getPortCount())
if ports:
	for i in ports:
		print(midiin.getPortName(i))
	print("Opening port 1!") 
	midiin.openPort(1)
	while True: #loop
		m = midiin.getMessage(250) # some timeout in ms
		if m:
			print_message(m)
			if m.isController():
				if m.getControllerNumber() == 1:
					r = m.getControllerValue() * 2
				elif m.getControllerNumber() == 2:
					g = m.getControllerValue() * 2
				elif m.getControllerNumber() == 3:
					b = m.getControllerValue() * 2
		screen.fill((r,g,b))
		pygame.display.update()
else:
	print('NO MIDI INPUT PORTS!')
	