import numpy as np
import sounddevice as sd
import time

sample_rate = 44100
duration = 100
frequency = 440.0

# linspace(start, stop, step)
x = np.linspace(0, duration * 2 * np.pi, int(duration * sample_rate))
sinewave_data = np.sin(frequency * x)

# best to attenuate it before playing, they can get very loud
sinewave_data = sinewave_data * 0.3 # volume

sd.play(sinewave_data, sample_rate)
sd.wait()