#!/usr/bin/env python3

import matplotlib.pyplot as plt
import json, pickle, gzip
import numpy as np
from housepy import drawing, log
from housepy.sound import Sound
# from scipy.signal import spectrogram




def spectrum(signal, rate):

    block_size = 512
    block_overlap = block_size / 2 # power of two, default is 128        

    # freqs, ts, spectrum = spectrogram(sound.signal, fs=sound.rate, noverlap=block_overlap, nfft=block_size, detrend='constant', return_onesided=True, scaling='density', axis=-1, mode='psd', window=('tukey', 0.25), nperseg=block_overlap*2)       
    spectrum, freqs, ts, image = plt.specgram(signal, NFFT=block_size, Fs=rate, noverlap=block_overlap)

    # (plt is 3k smaller)

    # print("spectrum", spectrum) # freq rows of time columns. 
    # print()
    # print(freqs)
    # print()
    # print(ts)

    log.info("--> freq bins %s" % len(freqs))
    log.info("--> time columns %s" % len(ts))


    # with gzip.open("spectrum.pklz", 'wb') as f:
    #     f.write(pickle.dumps(spectrum))

    ctx = drawing.Context(len(ts) * 1, len(freqs) * 1, relative=True)           # if it's not an even multiple, artifacts happen

    pixel_width = ctx.width / len(spectrum[0])
    pixel_height = ctx.height / len(spectrum)

    # for y, row in enumerate(spectrum):
    #     for x, value in enumerate(row):
    #         v = min(value / (allmax / 500), 1.0)
    #         v = 1 - v
    #         # print((x * pixel_width) / ctx.width, (y * pixel_height) / ctx.height, pixel_width / ctx.width, pixel_height / ctx.height)
    #         ctx.rect((x * pixel_width) / ctx.width, (y * pixel_height) / ctx.height, pixel_width / ctx.width, pixel_height / ctx.height, fill=(v, v, v, 1.), stroke=(1., 0., 0., 0.), thickness=0.0)

    for y, row in enumerate(spectrum):
        for x, value in enumerate(row):
            # v = min(value / (allmax / 1000), 1.0)
            v = np.sqrt(value.max()) 
            # v = v if v > 20 else 0
            v /= 100      ## really out of 100? "The peak height in the power spectrum is an estimate of the RMS amplitude."
            # v = value.max() / (100 * 100)           ## less compression
            # v = 1 - v
            ctx.line((x * pixel_width) / ctx.width, (y * pixel_height) / ctx.height, ((x * pixel_width) + pixel_width) / ctx.width, (y * pixel_height) / ctx.height, stroke=(v, v, v, 1.), thickness=pixel_height)

    ctx.output("charts/")


if __name__ == "__main__":
    filename = "robin_chat_sample_11k_16_mono.wav"
    sound = Sound().load(filename)
    spectrum(sound.signal, sound.rate)


"""
ok, so. 

robin_chat_sample_11k_16_mono.wav

11kz mono audio file:     244kb
compressed spectrum data: 936kb
1-pixel image:             75kb  (70kb if black) 300p compression

so the image is the greatest compression. basically because it's only 256 values of resolution. (2^8 / byte)

"""





"""
http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.specgram

Returns the tuple (spectrum, freqs, t, im):

spectrum: 2-D array
columns are the periodograms of successive segments (ie, the value/color)

freqs: 1-D array
The frequencies corresponding to the rows in spectrum (ie, the rows, evenly spaced, which vary based on sample rate)

t: 1-D array
The times corresponding to midpoints of segments (ie the columns, evenly spaced (not logarithmic?, vary on length)


image: instance of class AxesImage
The image created by imshow containing the spectrogram




so... just need the spectrum to plot. what's the range of the values?



could use this instead:
http://scipy.github.io/devdocs/generated/scipy.signal.spectrogram.html


so what's the goal?

for a given time period, get the density and entropy 


amount (how much)
density (how clumpy)
entropy (how organized the clumps)
markov (the linear relationships)

but all of this assumes the fundamentals are detectable.

for listening box, we want to find holes. 

so the output would just be a strip of frequencies, with the average intensity in each.

for the piano strings project, it's the same.  (that piece is kind of like physical convolution)

need to have a time based model. so what is that? just distribution

"""        