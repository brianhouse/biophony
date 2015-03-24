import matplotlib.pyplot as plt

def plot(signal, sampling_rate):

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
    plt.plot(signal, color=(1., 0., 0.))

    # show spectrogram
    plt.subplot(2, 1, 2, axisbg='#ffffff')

    block_overlap = block_size / 2 # power of two, default is 128
    Pxx, freqs, t, plot = plt.specgram(signal, NFFT=block_size, Fs=sampling_rate, noverlap=block_overlap)

    duration = len(signal) / sampling_rate
    plt.axis([0.0, duration, 0, sampling_rate/2])


    plt.show()

# try making a signal from freqs and t from the spectrogram
# the spectrogram isnt doing anything, right? youre really just remapping waveforms. right? no.


"""
Compute and plot a spectrogram of data in x. Data are split into NFFT length segments and the spectrum of each section is computed. The windowing function window is applied to each segment, and the amount of overlap of each segment is specified with noverlap. The spectrogram is plotted as a colormap (using imshow).

http://matplotlib.org/api/pyplot_api.html
"""

# do autocorrelation

#pylab.savefig("SIG.png",dpi=200)



# peak finding
# http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.find_peaks_cwt.html
