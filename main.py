#!/usr/bin/env python3

# http://stackoverflow.com/questions/892199/detect-record-audio-in-python

import matplotlib.pyplot as plt
import numpy as np
import signal_processing as sp
from plotter import plot
from sound import SoundSignal

filename = "output.wav"
filename = "camp_2_11hz_16_mono.wav"
filename = "boat_sample_11hz_16_mono_short.wav"

sound = SoundSignal().load(filename)
# sound = SoundSignal().record(5)
# sound.play()

# signal = sound.signal
# signal = sp.bandpass_filter(signal, sound.frequency, 50, 5000)
# signal = sp.highpass_filter(signal, sound.frequency, 2000)

sound.plot()
# sound.play()
