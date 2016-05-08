import pyaudio, wave
import numpy as np
import matplotlib.pyplot as plt
from housepy import log, util

CHUNK = 1024

class SoundSignal(object):

    def __init__(self):
        self.signal = None
        self.bits = None
        self.rate = None
        self.size = None        
        self.path = None
        self.wf = None

    def load(self, path):
        log.info("SoundSignal.load")
        log.info("--> loading from %s" % path)
        self.path = path
        self.wf = wave.open(self.path, 'rb')
        self.bits = self.wf.getsampwidth() * 8
        if self.bits != 16:
            raise NotImplementedError
        self.signal = np.fromstring(self.wf.readframes(-1), 'Int16')
        self.wf.rewind()
        self.rate = self.wf.getframerate()
        self.size = len(self.signal)
        self.duration = self.size / self.rate        
        log.info("--> bits %s" % self.bits)
        log.info("--> rate %s" % self.rate)
        log.info("--> size %s" % self.size)
        log.info("--> duration %fs" % self.duration)
        return self

    def reload(self):
        return self.load(self.path)

    def record(self, duration, path=None, rate=11025):
        log.info("SoundSignal.record")
        if path is None:
            path = "%s.wav" % util.dt(util.timestamp(), tz="Africa/Johannesburg").strftime("%y%m%d-%H%M%S")    # needs to be local timezone
        log.info("--> recording to %s" % path)
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=rate,
                        input=True,
                        frames_per_buffer=CHUNK)
        log.info("* Recording...")
        frames = []
        for i in range(0, int(rate / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
        log.info("--> done")
        stream.stop_stream()
        stream.close()
        p.terminate()

        # write file
        wf = wave.open(path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        self.load(path)
        return self


    def play(self):
        log.info("SoundSignal.play")
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                        channels=self.wf.getnchannels(),
                        rate=self.wf.getframerate(),
                        output=True)
        data = self.wf.readframes(CHUNK)
        while data != '':
            stream.write(data)
            data = self.wf.readframes(CHUNK)
        stream.stop_stream()
        stream.close()
        p.terminate()
        self.wf.rewind()

    def plot(self):

        # 50-5000 hz
        # need a window @ 25 hz, 0.04 seconds
        # 0.04 / (1 / sampling_rate)
        # at 11025, that's 441
        # so at that sampling_rate and higher, 512 is good        
        block_size = 512

        # set up plot
        plt.rcParams['toolbar'] = 'None'
        plt.figure(frameon=True, figsize=(15, 8), dpi=80, facecolor=(1., 1., 1.), edgecolor=(1., 1., 1.))
        
        # show amplitude domain
        plt.subplot(2, 1, 1, axisbg=(1., 1., 1.))
        plt.plot(self.signal, color=(1., 0., 0.))        
        plt.axis([0.0, self.duration * self.rate, 0-(2**self.bits/2), 2**self.bits/2]) # go to bitrate
        # plt.xlabel("Samples")
        # plt.ylabel("Amplitude")
        
        # show spectrogram
        plt.subplot(2, 1, 2, axisbg='#ffffff')
        # plt.subplot(1, 1, 1, axisbg='#ffffff')
        block_overlap = block_size / 2 # power of two, default is 128
        spectrum, freqs, t, image = plt.specgram(self.signal, NFFT=block_size, Fs=self.rate, noverlap=block_overlap)
        plt.axis([0.0, self.duration, 0, self.rate/2])
        # plt.xlabel("Seconds")
        # plt.ylabel("Frequency")

        # plt.suptitle(self.path)
        fig = plt.gcf()
        fig.canvas.set_window_title(self.path)        

        plt.show()

        print("spectrum", spectrum)
        print(len(spectrum[0]))         # 257 rows of 4154 columns. 
        print()
        print("freqs", freqs)
        print(len(freqs))
        print()
        print("t", t)
        print(len(t))


"""
http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.specgram

Returns the tuple (spectrum, freqs, t, im):

spectrum: 2-D array
columns are the periodograms of successive segments (ie, the value/color)

freqs: 1-D array
The frequencies corresponding to the rows in spectrum (ie, the rows, evenly spaced, which vary based on sample rate)

t: 1-D array
The times corresponding to midpoints of segments (ie the columns, evenly spaced (not logarithmic?, vary on length)


im: instance of class AxesImage
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