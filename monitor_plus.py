#!/usr/bin/env python3

import threading, queue
import matplotlib.pyplot as plt
import numpy as np
from housepy import animation, config, log
from housepy.sound import Sound
import signal_processing as sp

# should I be using the new async?

THRESHOLD = 1000000

display_spectrums = queue.Queue()

class SoundPull(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        spectrum_sum = None
        num_spectrums = 0
        while True:
            # filename = "robin_chat_sample_11k_16_mono.wav"                        
            # sound = Sound().load(filename)            
            sound = Sound().record(10, keep_file=False)
            block_size = 512
            block_overlap = block_size / 2 # power of two, default is 128        
            spectrum, freqs, ts, image = plt.specgram(sound.signal, NFFT=block_size, Fs=sound.rate, noverlap=block_overlap)            
            log.info("--> freq bins %s" % len(freqs))
            log.info("--> time columns %s" % len(ts))

            spectrum = sp.normalize(np.sqrt(spectrum), 0.0, 100.0) # sqrt compresses, good for power. 200 is a clipping threshold.
            spectrum = sp.rescale(spectrum, 0, 255)

            s = np.sum(spectrum)
            log.info("--> SUM %s" % s)
            if s < THRESHOLD:
                continue

            num_spectrums += 1
            if spectrum_sum is None:
                spectrum_sum = spectrum
            else:
                sum_multiplier = (num_spectrums - 1) / num_spectrums
                spectrum_sum *= sum_multiplier
                add_multiplier = 1 / num_spectrums
                spectrum *= add_multiplier
                spectrum_sum += spectrum

            ds = np.copy(spectrum_sum).astype(np.uint32) # convert to uint32
            ds = ((ds & 0xFF) <<8) + ((ds & 0xFF) <<16) + ((ds & 0xFF)) # make white
            # print(ds[80])
            display_spectrums.put(ds)

SoundPull()

ctx = animation.Context(427, 257, background=(0, 0, 0, 1), fullscreen=False, smooth=False, screen=0)    
display_spectrum = None
def draw():
    global display_spectrum
    try:
        display_spectrum = display_spectrums.get_nowait()
        log.info("New spectrum: %sx%s" % (display_spectrum.shape[1], display_spectrum.shape[0]))
    except queue.Empty:
        pass
    if display_spectrum is None:
        return
    ctx.pixels(display_spectrum)
ctx.start(draw)


