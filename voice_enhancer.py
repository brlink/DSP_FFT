import matplotlib.pyplot as plot
from scipy.io import wavfile
from scipy.fftpack import fft
import numpy as np
# import librosa.display
import wave


def time_amplitude(samplingFrequency,  signalData):
    duration = len(signalData)/samplingFrequency
    time_amplitude.time = np.arange(0, duration, 1/samplingFrequency)
    plot.plot(time_amplitude.time, signalData)
    plot.title('Time-Amplitude of the audio')
    plot.xlabel('Time [s]')
    plot.ylabel('Amplitude')

    time = np.arange(0, nframes) * (1.0 / framerate)
    plot.plot(time, waveData[0, :])
    plot.xlabel('time')
    plot.ylabel('am')
    plot.savefig('time domain.svg', dpi=900, format='svg')

    return plot.show()


def time_amplitude_analysis(samplingFrequency,  signalData):
    # Normalizing the value, bring them between -1 and 1.
    sampNormed = np.interp(signalData, (signalData.min(), signalData.max()), (-1, 1))
    plot.plot(time_amplitude.time, sampNormed)
    plot.title('Normalizing time-Amplitude of the audio')
    plot.xlabel('Normalizing time')
    plot.ylabel('Amplitude')
    plot.savefig('Normalizing time domain.svg', dpi=900, format='svg')

    return plot.show()

# Spec
"""
def fre_db(x, sr):
    x = librosa.stft(x)
    xdb = librosa.amplitude_to_db(abs(x))
    plot.figure()
    librosa.display.specshow(xdb, sr=sr, x_axis='time', y_axis='hz')
    plot.colorbar()
    plot.show()
"""


# ********FFT*********
def fft_plot():
    fftdata = np.fft.fft(waveData[0, :])
    len_fftdata = len(fftdata)
    fftdata = fftdata[:int(len_fftdata/2)]
    fft_plot.fftdata_copy = fftdata
    fftdata = abs(fftdata)
    hz_axis = np.arange(0, len(fftdata))
    plot.figure()
    plot.plot(hz_axis, fftdata)
    plot.title('Frequency domain')
    plot.xlabel('hz')
    plot.ylabel('am')
    plot.savefig('Frequency domain.svg', dpi=900, format='svg')
    plot.show()

    waveData_update = waveData
    for num in range(0, len(hz_axis)):
        if waveData_update[0, num] >= 6000 and waveData_update[0, num] <= 10000:
            waveData_update[0, num] = waveData_update[0, num] * 2
        else:
            waveData_update[0, num] = waveData_update[0, num] * 1.6

    for num in range(0, len(hz_axis)):
        if waveData_update[1, num] >= 6000 and waveData_update[1, num] <= 10000:
            waveData_update[1, num] = waveData_update[1, num] * 1.6
        else:
            waveData_update[1, num] = waveData_update[1, num] * 1.4

    fftdata_update = np.fft.fft(waveData_update[0, :])
    fft_plot.fftdata_update_copy = fftdata_update
    fftdata_update = fftdata_update[:int(len_fftdata / 2)]
    fftdata_update = abs(fftdata_update)
    hz_axis_update = np.arange(0, len(fftdata_update))
    plot.figure()
    plot.plot(hz_axis_update, fftdata_update)
    plot.title('Updated frequency domain')
    plot.xlabel('hz')
    plot.ylabel('am')
    plot.savefig('Update frequency domain.svg', dpi=900, format='svg')
    plot.show()

    return plot.show()


# **** Inverse FFT ****
def ifft_time_amplitude():
    ifft_signalData = np.fft.ifft(fft_plot.fftdata_update_copy).real
    plot.plot(time_amplitude.time, ifft_signalData)
    plot.title('Updated Time-Amplitude of the audio')
    plot.xlabel('Time [s]')
    plot.ylabel('Amplitude-update')
    plot.savefig('Update time domain.svg', dpi=900, format='svg')
    plot.show()

    ndatas = ifft_signalData.astype(np.int16)
    f = wave.open("improved.wav", "wb")

    # 配置声道数、量化位数和取样频率
    f.setnchannels(1)
    f.setsampwidth(sampwidth)
    f.setframerate(framerate)
    f.writeframes(ndatas.tobytes())
    f.close()


if __name__ == '__main__':
    # Read the wav file
    samplingFrequency, signalData = wavfile.read('original.wav')
    # x, sr = librosa.load('original.wav', sr=8000)

    path = 'original.wav'
    f = wave.open(path, 'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    voiceStrData = f.readframes(nframes)
    waveData = np.fromstring(voiceStrData, dtype=np.short)
    waveData = np.reshape(waveData, [nframes, nchannels]).T
    strData = f.readframes(nframes)
    waveData_0 = waveData
    f.close()

    time_amplitude(samplingFrequency, signalData)
    plot.show()

    time_amplitude_analysis(samplingFrequency, signalData)
    plot.show()

    # fre_db(x, sr)
    # plot.show()

    fft_plot()
    plot.show()

    ifft_time_amplitude()
    plot.show()

