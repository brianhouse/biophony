import pyaudio, wave
import numpy as np
import matplotlib.pyplot as plt
from housepy import log, util

"""
    Does this need to be 96khz?

"""

CHUNK = 1024

class SoundSignal(object):

    def __init__(self, bits=16):
        self.signal = None
        self.bits = bits
        if self.bits != 16 and self.bits != 24:
            raise NotImplementedError
        self.size = None
        self.frequency = None
        self.path = None
        self.wf = None

    def load(self, path):
        log.info("SoundSignal.load")
        log.info("--> loading from %s" % path)
        self.path = path
        self.wf = wave.open(self.path, 'rb')
        self.signal = np.fromstring(self.wf.readframes(-1), 'Int24' if self.bits == 24 else 'Int16')
        self.wf.rewind()
        self.frequency = self.wf.getframerate()
        self.size = len(self.signal)
        self.duration = self.size / self.frequency        
        log.info("--> frequency %s" % self.frequency)
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

        # show spectrogram
        plt.subplot(2, 1, 2, axisbg='#ffffff')

        block_overlap = block_size / 2 # power of two, default is 128
        Pxx, freqs, t, plot = plt.specgram(self.signal, NFFT=block_size, Fs=self.frequency, noverlap=block_overlap)

        plt.axis([0.0, self.duration, 0, self.frequency/2])

        plt.show()
