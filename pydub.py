from pyo import *
import time
s = Server().boot()
s.start()

C0 = 16.35
Cs0 = 17.32
D0 = 18.35
Ds0 = 19.45
E0 = 20.60
F0 = 21.83
Fs0 = 23.12
Fs0 = 23.12
G0 = 24.50
Gs0 = 25.96
A0 = 27.50
As0 = 29.14
B0 = 30.87
C1 = 32.70
Cs1 = 34.65
D1 = 36.71
Ds1 = 38.89
E1 = 41.20
F1 = 43.65
Fs1 = 46.25
G1 = 49.00
Gs1 = 51.91
A1 = 55.00
As1 = 58.27
B1 = 61.74
C2 = 65.41
Cs2 = 69.30
D2 = 73.42
Ds2 = 77.78
E2 = 82.41
F2 = 87.31
Fs2 = 92.50
G2 = 98.00
Gs2 = 103.83
A2 = 110.00
As2 = 116.54
B2 = 123.47
C3 = 130.81
Cs3 = 138.59
D3 = 146.83
Ds3 = 155.56
E3 = 164.81
F3 = 174.61
Fs3 = 185.00
G3 = 196.00
Gs3 = 207.65
A3 = 220.00
As3 = 233.08
B3 = 246.94
C4 = 261.63
Cs4 = 277.18
D4 = 293.66
Ds4 = 311.13
E4 = 329.63
F4 = 349.23
Fs4 = 369.99
G4 = 392.00
Gs4 = 415.30
A4 = 440.00
As4 = 466.16
B4 = 493.88
C5 = 523.25
Cs5 = 554.37
D5 = 587.33
Ds5 = 622.25
E5 = 659.25
F5 = 698.46
Fs5 = 739.99
G5 = 783.99
Gs5 = 830.61
A5 = 880.00
As5 = 932.33
B5 = 987.77
C6 = 1046.50

semibreve = 4
minim = 2
crotchet = 1
quaver = 0.5
semiquaver = 0.25

crazyFrog = [D4,F4,D4,D4,G4,D4,C4,D4,A4,D4,D4,As4,A4,F4,D4]
crazyFrogTiming = [crotchet, quaver*1.5, quaver, quaver*1.25, quaver, quaver, crotchet, quaver*1.5, quaver, quaver*1.25, quaver, quaver,quaver,quaver,quaver]

lfd = Sine([.4,.3], mul=.2, add=.5)
lf2 = Sine(freq=.25, mul=10, add=30)

for i in range(len(crazyFrog)):
	time.sleep(crazyFrogTiming[i])
	saw = SuperSaw(freq=crazyFrog[i],detune=lfd,bal=0.5,mul=0.2).out()

time.sleep(1)
s.stop()