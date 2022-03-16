from pyo import *
import time
s = Server(duplex=0).boot()
s.start()

lfd = Sine([.4,.3], mul=.2, add=.5)
lf2 = Sine(freq=.25, mul=10, add=30)

while True:
    lfd.out()
