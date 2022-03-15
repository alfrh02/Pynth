from pyo import *
import time

s = Server().boot()

a = Sine(440, 0, 0.1).mix(2).out()

bpm = 125

s.start()

time.sleep(1)
s.stop()
