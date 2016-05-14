#!/usr/bin/env python3

# http://stackoverflow.com/questions/892199/detect-record-audio-in-python

import matplotlib.pyplot as plt
import numpy as np
import signal_processing as sp
from housepy.sound import Sound

filename = "output.wav"
filename = "camp_2_11khz_16_mono.wav"
filename = "boat_sample_11khz_16_mono_short.wav"
# filename = "boat_sample_96khz_24_mono_short.wav"
filename = "robin_chat_sample_11k_16_mono.wav"
# filename = "robin_chat_sample_96k_16_mono.wav"
# # filename = "robin_chat_sample_96k_24_mono.wav"
# filename = "reeds_11khz_16_mono.wav"
# filename = "lores_bounce_mono_short.wav"
# filename = "reeds_22khz_16_mono.wav"
# filename = "reeds_short_22khz_16_mono.wav"
# filename = "reeds_shorter_22khz_16_mono.wav"

sound = Sound().load(filename)
# sound = SoundSignal().record(5)
# sound.play()

# signal = sound.signal
# signal = sp.bandpass_filter(signal, sound.frequency, 50, 5000)
# signal = sp.highpass_filter(signal, sound.frequency, 2000)

# sound.plot()
# sound.play()
