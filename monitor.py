#!/usr/bin/env python3

import threading, queue
import matplotlib.pyplot as plt
import numpy as np
from housepy import animation, config, log
from housepy.sound import Sound
import signal_processing as sp

# should I be using the new async?

spectrums = queue.Queue()

class SoundPull(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            # filename = "robin_chat_sample_11k_16_mono.wav"                        
            # sound = Sound().load(filename)            
            sound = Sound().record(10)
            block_size = 512
            block_overlap = block_size / 2 # power of two, default is 128        
            spectrum, freqs, ts, image = plt.specgram(sound.signal, NFFT=block_size, Fs=sound.rate, noverlap=block_overlap)            
            log.info("--> freq bins %s" % len(freqs))
            log.info("--> time columns %s" % len(ts))

            spectrum = sp.normalize(np.sqrt(spectrum), 0.0, 100.0) # sqrt compresses, good for power. 200 is a clipping threshold.
            spectrum = sp.rescale(spectrum, 0, 255).astype(np.uint32) # convert to uint32
            spectrum = ((spectrum & 0xFF) <<8) + ((spectrum & 0xFF) <<16) + ((spectrum & 0xFF))

            print(spectrum[80])
            spectrums.put(spectrum)

SoundPull()

ctx = animation.Context(427, 257, background=(0, 0, 0, 1), fullscreen=True, smooth=False, screen=0)    
pixel_width = 1
pixel_height = 1

spectrum = None

def draw():
    global spectrum
    try:
        spectrum = spectrums.get_nowait()
        log.info("New spectrum: %sx%s" % (spectrum.shape[1], spectrum.shape[0]))
    except queue.Empty:
        pass
    if spectrum is None:
        return
    ctx.pixels(spectrum)
ctx.start(draw)


