#!/usr/bin/env python3

# http://stackoverflow.com/questions/892199/detect-record-audio-in-python

import pyaudio, wave
import matplotlib.pyplot as plt
import numpy as np
import signal_processing as sp
from plotter import plot

# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 11025
# RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "output.wav"

# # record
# p = pyaudio.PyAudio()
# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input=True,
#                 frames_per_buffer=CHUNK)
# print("* recording")
# frames = []
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)
# print("* done recording")
# stream.stop_stream()
# stream.close()
# p.terminate()

# # write file
# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()

# WAVE_OUTPUT_FILENAME = "okavango_test_mono_11hz_shorter.wav"
WAVE_OUTPUT_FILENAME = "camp_2_11hz_16_mono.wav"
# WAVE_OUTPUT_FILENAME = "okavango_test_mono_44hz_shorter.wav"
# WAVE_OUTPUT_FILENAME = "output.wav"

# load file
wf = wave.open(WAVE_OUTPUT_FILENAME, 'r')
signal = wf.readframes(-1)
signal = np.fromstring(signal, 'Int16')

# signal = sp.normalize(signal)

# # load direct
# signal = np.fromstring(signal, 'Int16')

print("SAMPLE SIZE: %s" % len(signal))
print("FREQ %s" % wf.getframerate())
print("SAMPWIDTH %s" % (wf.getsampwidth() * 8))

sampling_rate = wf.getframerate()

# signal = sp.bandpass_filter(signal, sampling_rate, 50, 5000)
# signal = sp.highpass_filter(signal, sampling_rate, 2000)


plot(signal, sampling_rate)

wf.close()
