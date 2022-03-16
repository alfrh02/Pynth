import rtmidi
import pygame

pygame.init()
midiin = rtmidi.RtMidiIn()

width = 400
height = 400

pygame.display.set_caption("RGB Exp")
screen = pygame.display.set_mode((width,height))

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
		
		screen.fill(r,g,b)
else:
    print('NO MIDI INPUT PORTS!')
	