#!/usr/bin/env python3

import pickle
from housepy import config, log, drawing, util, sound
import signal_processing as sp


ts = []
values = []

# log.info("Loading data...")
# with open("data.txt") as f:
#     for line in f:
#         tokens = line.split(',')
#         dt = util.parse_date(tokens[0].strip(), tz="America/Denver")
#         t = util.timestamp(dt)
#         value = float(tokens[1].strip())
#         ts.append(t)
#         values.append(value)
#         # print(t, value)
# log.info("--> done")

# util.save("data.pkl", {'ts': ts, 'values': values})

# exit()

data = util.load("data.pkl")
ts = data['ts']
values = data['values']


# http://www.usbr.gov/pn-bin/instant.pl?station=ABEI&year=2015&month=7&day=1&year=2016&month=6&day=1&pcode=OB

log.info("Converting to 0-1 signal...")
signal = sp.resample(ts, values)
signal = sp.normalize(signal)
log.info("--> done")

log.info("Drawing...")
ctx = drawing.Context(6000, 500)
ctx.plot(signal)
ctx.output("audification_signals/")
log.info("--> done")


signal = sp.make_audio(signal)


from spectrometer import spectrum

filename = "weather_test_44.wav"
sound.write_audio(signal, filename)

import subprocess
subprocess.call(["open", filename])


spectrum(signal, 11025)


"""

Learnings:

- audio data is phased pressure around a central axis. other linear data doesnt necessarily work that way

"""